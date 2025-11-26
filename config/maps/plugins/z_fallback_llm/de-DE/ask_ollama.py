import subprocess
import re
import json
import os
import sys
import logging
import inspect
import sqlite3
import hashlib
import datetime
import random
from pathlib import Path

# --- KONFIGURATION ---
PLUGIN_DIR = Path(__file__).parent
MEMORY_FILE = PLUGIN_DIR / "conversation_history.json"
BRIDGE_FILE = Path("/tmp/aura_clipboard.txt")
DB_FILE = PLUGIN_DIR / "llm_cache.db"

MAX_HISTORY_ENTRIES = 2
CACHE_TTL_DAYS = 7
MAX_VARIANTS = 5
DEFAULT_RATING = 5

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- AUDIO SETUP (NEU) ---
create_bent_sine_wave_sound = None
try:
    # Wir navigieren 6 Ebenen hoch zum Projekt-Root (STT/)
    project_root = Path(__file__).resolve().parents[5]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))

    # Import aus deinem existierenden Audio-Manager
    from scripts.py.func.audio_manager import create_bent_sine_wave_sound
except ImportError:
    # Kein Crash, wenn Audio fehlt (z.B. im Docker oder CI)
    # logging.warning(f"Audio Manager nicht gefunden: {e}")
    pass

def log_debug(message: str):
    caller_info = "UNKNOWN:0"
    stack = inspect.stack()
    if len(stack) > 1:
        try:
            filename = os.path.basename(stack[1].filename)
            line_number = stack[1].lineno
            caller_info = f"{filename}:{line_number}"
        except Exception:
            pass
    print(f"[DEBUG_LLM] {caller_info}: {message}", file=sys.stderr)
    logging.info(f"{caller_info}: {message}")

# --- SOUND FUNKTION ---
def play_cache_hit_sound():
    """Spielt einen 'Happy Sound' (Ping) bei Cache-Treffer."""
    if create_bent_sine_wave_sound:
        try:
            # Start: 880Hz, Ende: 1200Hz (Aufsteigend = Positiv)
            # Sehr kurz: 80ms
            sound = create_bent_sine_wave_sound(
                start_freq=880,
                end_freq=1200,
                duration_ms=80,
                volume=0.15 # Leise, nicht erschrecken
            )
            sound.play()
        except Exception as e:
            log_debug(f"Sound Error: {e}")

# --- DATABASE LAYER ---
def init_db():
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS prompts (
                        hash TEXT PRIMARY KEY,
                        prompt_text TEXT,
                        clean_input TEXT,
                        keywords TEXT,
                        last_used TIMESTAMP
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt_hash TEXT,
                        response_text TEXT,
                        created_at TIMESTAMP,
                        rating INTEGER DEFAULT 5,
                        comment TEXT,
                        usage_count INTEGER DEFAULT 0,
                        FOREIGN KEY(prompt_hash) REFERENCES prompts(hash)
                    )''')

        # MIGRATIONEN
        try: c.execute("ALTER TABLE responses ADD COLUMN rating INTEGER DEFAULT 5")
        except Exception: pass
        try: c.execute("ALTER TABLE responses ADD COLUMN comment TEXT")
        except Exception: pass
        try: c.execute("ALTER TABLE responses ADD COLUMN usage_count INTEGER DEFAULT 0")
        except Exception: pass
        try: c.execute("ALTER TABLE prompts ADD COLUMN clean_input TEXT")
        except Exception: pass
        try: c.execute("ALTER TABLE prompts ADD COLUMN keywords TEXT")
        except Exception: pass

        c.execute(f"UPDATE responses SET rating = {DEFAULT_RATING} WHERE rating = 0 AND comment IS NULL")

        # VIEWS
        c.execute("DROP VIEW IF EXISTS overview_readable")
        c.execute('''
            CREATE VIEW overview_readable AS
            SELECT
                r.id,
                r.rating,
                r.usage_count,
                p.clean_input AS User_Frage,
                p.keywords AS Schlagworte,
                r.response_text,
                r.comment,
                r.created_at
            FROM responses r
            LEFT JOIN prompts p ON r.prompt_hash = p.hash
            ORDER BY r.created_at DESC
        ''')

        c.execute("DROP VIEW IF EXISTS stats_most_asked")
        c.execute('''
            CREATE VIEW stats_most_asked AS
            SELECT
                clean_input,
                COUNT(*) as context_variations,
                SUM(r.usage_count) as total_answers_served
            FROM prompts p
            JOIN responses r ON p.hash = r.prompt_hash
            GROUP BY clean_input
            ORDER BY total_answers_served DESC
        ''')

        conn.commit()
        conn.close()
    except Exception as e:
        log_debug(f"DB Init Error: {e}")

def normalize_for_hashing(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_semantic_keywords(user_question):
    log_debug(f"🔍 Extrahiere Keywords aus: '{user_question}'")
    prompt = (
        "Extrahiere den Kern der folgenden Frage in maximal 3 Schlagworten.\n"
        "Regeln: Nur die Schlagworte. Keine Sätze. Kleinschreibung. Deutsch.\n"
        f"Frage: \"{user_question}\"\n"
        "Schlagworte:"
    )
    try:
        cmd = ["ollama", "run", "llama3.2"]
        result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8', timeout=5)
        if result.returncode == 0:
            raw_output = result.stdout.strip().lower()
            clean_text = re.sub(r'[^\w\s]', ' ', raw_output)
            words = clean_text.split()
            words.sort()
            sorted_keywords = " ".join(words)
            log_debug(f"🗝️  Keywords (Sorted): '{sorted_keywords}'")
            return sorted_keywords
        return user_question
    except Exception as e:
        log_debug(f"Keyword extraction failed: {e}")
        return user_question

def get_cached_response(hash_input_str):
    init_db()
    normalized_prompt = normalize_for_hashing(hash_input_str)
    prompt_hash = hashlib.sha256(normalized_prompt.encode('utf-8')).hexdigest()

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute("SELECT last_used FROM prompts WHERE hash=?", (prompt_hash,))
        row = c.fetchone()
        if not row:
            conn.close()
            return None, False

        last_used_str = row[0]
        try:
            last_used = datetime.datetime.fromisoformat(last_used_str)
            age = datetime.datetime.now() - last_used
            if age.days > CACHE_TTL_DAYS:
                conn.close()
                return None, True
        except Exception: pass

        c.execute("SELECT id, response_text FROM responses WHERE prompt_hash=?", (prompt_hash,))
        rows = c.fetchall()

        if rows:
            variant_count = len(rows)
            if variant_count < 3 and random.random() < 0.2:
                log_debug(f"♻️ Active Variation: {variant_count} Varianten. Generiere neu...")
                conn.close()
                return None, True

            chosen_row = random.choice(rows)
            c.execute("UPDATE responses SET usage_count = usage_count + 1 WHERE id = ?", (chosen_row[0],))
            conn.commit()
            conn.close()

            log_debug(f"⚡ CACHE HIT! Variante ID {chosen_row[0]} gewählt.")

            # --- HIER KOMMT DER HAPPY SOUND ---
            play_cache_hit_sound()
            # ----------------------------------

            update_prompt_stats(prompt_hash)
            return chosen_row[1], False

        conn.close()
        return None, False

    except Exception as e:
        log_debug(f"DB Read Error: {e}")
        return None, False

def cache_response(hash_input_str, response_text, clean_user_input, keywords=None):
    init_db()
    normalized_prompt = normalize_for_hashing(hash_input_str)
    prompt_hash = hashlib.sha256(normalized_prompt.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().isoformat()

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO prompts (hash, prompt_text, clean_input, keywords, last_used) VALUES (?, ?, ?, ?, ?)",
                  (prompt_hash, hash_input_str, clean_user_input, keywords, now))
        c.execute('''INSERT INTO responses
                     (prompt_hash, response_text, created_at, rating, usage_count)
                     VALUES (?, ?, ?, ?, 1)''',
                  (prompt_hash, response_text, now, DEFAULT_RATING))
        c.execute("SELECT count(*) FROM responses WHERE prompt_hash=?", (prompt_hash,))
        count = c.fetchone()[0]
        if count > MAX_VARIANTS:
            excess = count - MAX_VARIANTS
            c.execute(f'''
                DELETE FROM responses WHERE id IN (
                    SELECT id FROM responses WHERE prompt_hash=?
                    ORDER BY rating ASC, usage_count ASC, created_at ASC LIMIT {excess}
                )
            ''', (prompt_hash,))
        conn.commit()
        conn.close()
        log_debug(f"Cache saved. Hash: {prompt_hash[:8]}")
    except Exception as e:
        log_debug(f"DB Write Error: {e}")

def update_prompt_stats(prompt_hash):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        now = datetime.datetime.now().isoformat()
        c.execute("UPDATE prompts SET last_used = ? WHERE hash = ?", (now, prompt_hash))
        conn.commit()
        conn.close()
    except Exception: pass

# --- HELPER FUNCTIONS ---
def clean_text_for_typing(text):
    allowed_chars = r'[^\w\s\.,!\?\-\(\)\[\]\{\}<>äöüÄÖÜß:;\'"\/\\@\+\=\~\#\%]'
    text = re.sub(allowed_chars, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_readme_content():
    try:
        current_path = Path(__file__).resolve()
        for _ in range(6):
            current_path = current_path.parent
            readme_path = current_path / "README.md"
            if readme_path.exists():
                log_debug(f"README gefunden: {readme_path}")
                content = readme_path.read_text(encoding='utf-8').strip()
                return content[:6000]
        return None
    except Exception: return None

def get_clipboard_content():
    if not BRIDGE_FILE.exists(): return None
    try:
        content = BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content: return content
        return None
    except Exception: return None

def load_history():
    if not MEMORY_FILE.exists(): return []
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f: return json.load(f)
    except Exception: return []

def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > MAX_HISTORY_ENTRIES * 2:
        history = history[-(MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception: pass

def execute(match_data):
    try:
        match_obj = match_data['regex_match_obj']
        if len(match_obj.groups()) >= 2:
            user_input_raw = match_obj.group(2).strip()
        else:
            user_input_raw = match_obj.group(1).strip()

        log_debug(f"Input: '{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        if "vergiss alles" in user_input_raw.lower():
            if MEMORY_FILE.exists():
                try: MEMORY_FILE.unlink()
                except Exception: pass
            return "Gedächtnis gelöscht."

        # --- AURA TECH PROFILE (Grounding) ---
        # Das verhindert Halluzinationen über GUIs, JSON oder falsche Sprachen.
        # --- AURA TECH PROFILE (Grounding & Facts) ---
        # Optimiert auf Token-Effizienz (Telegram-Stil), um Latenz zu verringern.
        AURA_TECH_PROFILE = (
            "SYSTEM-FAKTEN (Strict Grounding):\n"
            "About: Offline, privacy-first voice assistant framework. Transform speech into commands via scriptable rule engine.\n"
            "1. Tech Stack: Python (87%), Shell (9%), PowerShell (2%), Vosk (4GB/Sprache), LanguageTool. KEIN Java/C++, KEINE .exe, KEIN PDF-Support.\n"
            "2. Interface: 100% CLI & Voice. KEINE GUI, KEIN Web-UI, KEINE Maus/Buttons. Nur Tastatur/Sprache.\n"
            "3. Logik & Config: KEIN JSON/YAML! Regeln sind reine Python-Dateien (z.B. 'FUZZY_MAP_pre.py') mit Regex-Listen.\n"
            "   - Ablauf: Hierarchisch, kumulativ, alphabetisch sortiert (bei gleichem Ordner). Top-Down Exekution. Full-Match stoppt.\n"
            "   - Phasen: Pre-Processing (vor LanguageTool) und Post-Processing.\n"
            "4. Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins (z.B. Wiki, Translate, SQLite-Booksearch, ollama AI) erhalten Daten, verarbeiten sie kreativ und geben Text zurück in die Pipe.\n"
            "5. Security & Tools: \n"
            "   - Dateisuche: NUR via 'git ls-files | fzf'.\n"
            "   - Secrets: Findet Aura eine versteckte '.secret.py', nutzt es deren Passwort zum Entpacken von '_privat.zip' im selben Ordner.\n"
            "6. OS: Linux, Windows, macOS. (Kein Smartphone).\n"
            "7. Verhalten: Erfinde keine visuellen Elemente. Halte dich strikt an diese Architektur.\n"
        )

        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "zusammenfassung"]
        trigger_readme = [
            "hilfe", "dokumentation", "readme", "read me", "redmi", "lies mich",
            "wie installiere", "wie funktioniert", "projekt", "features", "was kannst du",
            "erkläre", "bedeutet", "warum", "wieso", "ist es möglich", "unterstützt"
        ]
        no_cache_keywords = ["witz", "spruch", "zufall", "überrasch", "random"]

        context_data = ""
        # Wir fügen das Tech-Profil standardmäßig zur Rolle hinzu
        system_role = f"Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze). {AURA_TECH_PROFILE}"

        use_history = True
        input_lower = user_input_raw.lower()
        bypass_cache = False
        use_semantic_hashing = False

        # Längen-Trigger
        if len(user_input_raw) > 50:
            use_semantic_hashing = True
            log_debug(f"Mode: LONG INPUT ({len(user_input_raw)} chars) -> Semantic Hashing ON")

        if any(w in input_lower for w in no_cache_keywords):
            bypass_cache = True
            log_debug("Cache BYPASS: Zufallswort erkannt.")

        if any(w in input_lower for w in trigger_clipboard):
            log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                # Bei Clipboard-Analysen ist das Tech-Profil weniger wichtig, aber schadet nicht.
                system_role = "Du bist ein Assistent. Analysiere die Daten in der Zwischenablage."
                use_history = False
                use_semantic_hashing = True
            else:
                return "Die Zwischenablage ist leer."

        elif any(w in input_lower for w in trigger_readme):
            log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                context_data = f"\nPROJEKT DOKUMENTATION (README.md - Auszug):\n'''{readme_content}'''\n"
                # Hier ist das Tech-Profil besonders wichtig, um Lücken in der Readme zu füllen
                system_role = (
                    f"Du bist der Support-Bot für 'SL5 Aura'. Nutze die Doku und folgende Fakten:\n"
                    f"{AURA_TECH_PROFILE}\n"
                    "Wenn etwas nicht in der Doku steht, nutze die Fakten. Erfinde nichts."
                )
                use_history = False
                use_semantic_hashing = True
            else:
                return "Ich konnte die Readme nicht finden."

        # --- HASH BERECHNUNG ---
        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # ... (Rest der Funktion bleibt EXAKT gleich wie vorher) ...
        hash_input = full_prompt_for_generation
        keywords = None

        if use_semantic_hashing:
            keywords = get_semantic_keywords(user_input_raw)
            hash_input = f"{system_role}\n{context_data}\nKEYWORDS: {keywords}"

        if use_history:
            history = load_history()
            if history:
                full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(history)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- CACHE CHECK ---
        if not bypass_cache:
            cached_resp, expired = get_cached_response(hash_input)
            if cached_resp:
                if use_history: save_to_history(user_input_raw, cached_resp)
                return cached_resp
            if expired:
                log_debug("♻️ Cache Entry EXPIRED.")

        log_debug("Cache MISS. Rufe Ollama für Antwort...")
        cmd = ["ollama", "run", "llama3.2"]
        result = subprocess.run(
            cmd, input=full_prompt_for_generation, capture_output=True, text=True, encoding='utf-8', timeout=90
        )

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response = clean_text_for_typing(result.stdout.strip())

        if not bypass_cache:
            cache_response(hash_input, response, user_input_raw, keywords)

        if use_history:
            save_to_history(user_input_raw, response)

        return response

    except Exception as e:
        log_debug(f"FATAL: {e}")
        return f"Fehler: {str(e)}"


