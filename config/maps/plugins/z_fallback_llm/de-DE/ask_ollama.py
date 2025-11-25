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

MAX_HISTORY_ENTRIES = 6
CACHE_TTL_DAYS = 7     # Nach 7 Tagen gilt der Prompt als "alt" -> Neu generieren
MAX_VARIANTS = 5       # Maximale Anzahl an Varianten pro Frage

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

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

# --- DATABASE LAYER (RELATIONAL) ---
def init_db():
    """Erstellt zwei Tabellen: Eine für Prompts, eine für Antwort-Varianten."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS prompts (
                        hash TEXT PRIMARY KEY,
                        prompt_text TEXT,
                        last_used TIMESTAMP
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        prompt_hash TEXT,
                        response_text TEXT,
                        created_at TIMESTAMP,
                        FOREIGN KEY(prompt_hash) REFERENCES prompts(hash)
                    )''')
        conn.commit()
        conn.close()
    except Exception as e:
        log_debug(f"DB Init Error: {e}")

def normalize_for_hashing(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_cached_response(full_prompt_str):
    """
    Holt eine ZUFÄLLIGE Variante aus dem Cache.
    """
    # Sicherstellen, dass DB existiert
    init_db()

    normalized_prompt = normalize_for_hashing(full_prompt_str)
    prompt_hash = hashlib.sha256(normalized_prompt.encode('utf-8')).hexdigest()

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # 1. Prüfen wann zuletzt genutzt (TTL)
        c.execute("SELECT last_used FROM prompts WHERE hash=?", (prompt_hash,))
        row = c.fetchone()

        if not row:
            conn.close()
            return None, False # Gar nicht im Cache

        last_used_str = row[0]
        try:
            last_used = datetime.datetime.fromisoformat(last_used_str)
            age = datetime.datetime.now() - last_used
            if age.days > CACHE_TTL_DAYS:
                log_debug(f"Cache EXPIRED (Alter: {age.days} Tage). Generiere neue Variante...")
                conn.close()
                return None, True
        except Exception: pass

        # 2. Varianten laden
        c.execute("SELECT response_text FROM responses WHERE prompt_hash=?", (prompt_hash,))
        rows = c.fetchall()
        conn.close()

        if rows:
            variant_count = len(rows)

            # Active Variation: 20% Chance auf Neuberechnung bei wenigen Varianten
            if variant_count < 3 and random.random() < 0.2:
                log_debug(f"♻️ Active Variation: Habe erst {variant_count} Varianten. Generiere proaktiv eine neue...")
                return None, True

            chosen_response = random.choice(rows)[0]
            log_debug(f"⚡ CACHE HIT! Wähle zufällige Variante aus {variant_count} verfügbaren.")

            update_prompt_stats(prompt_hash)
            return chosen_response, False

        return None, False

    except Exception as e:
        log_debug(f"DB Read Error: {e}")
        return None, False

def cache_response(full_prompt_str, response_text):
    """Speichert neue Antwort und löscht die älteste, wenn Limit erreicht."""
    # Sicherstellen, dass DB existiert
    init_db()

    normalized_prompt = normalize_for_hashing(full_prompt_str)
    prompt_hash = hashlib.sha256(normalized_prompt.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().isoformat()

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        c.execute("INSERT OR REPLACE INTO prompts (hash, prompt_text, last_used) VALUES (?, ?, ?)",
                  (prompt_hash, full_prompt_str, now))

        c.execute("INSERT INTO responses (prompt_hash, response_text, created_at) VALUES (?, ?, ?)",
                  (prompt_hash, response_text, now))

        # Limit prüfen
        c.execute("SELECT count(*) FROM responses WHERE prompt_hash=?", (prompt_hash,))
        count = c.fetchone()[0]

        if count > MAX_VARIANTS:
            c.execute(f'''
                DELETE FROM responses
                WHERE id IN (
                    SELECT id FROM responses
                    WHERE prompt_hash=?
                    ORDER BY created_at ASC
                    LIMIT {count - MAX_VARIANTS}
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
    except Exception:
        pass

# --- HELPER FUNCTIONS ---
def clean_text_for_typing(text):
    # Erlaubt URLs, Pfade und Satzzeichen
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
        log_debug("WARNUNG: Keine README.md gefunden.")
        return None
    except Exception:
        return None

def get_clipboard_content():
    if not BRIDGE_FILE.exists():
        log_debug(f"FAIL: Bridge-Datei {BRIDGE_FILE} fehlt.")
        return None
    try:
        content = BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content:
            preview = content.replace('\n', ' ')[:50]
            log_debug(f"SUCCESS: Clipboard: '{preview}...' ({len(content)} Zeichen)")
            return content
        return None
    except Exception:
        return None

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

        # --- TRIGGER ANALYSE ---
        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "kopierter text", "zusammenfassung"]
        trigger_readme = [
            "hilfe", "dokumentation", "readme", "read me", "redmi", "lies mich",
            "wie installiere", "wie funktioniert", "projekt", "features", "was kannst du"
        ]
        no_cache_keywords = ["witz", "spruch", "zufall", "überrasch", "random"]

        context_data = ""
        system_role = "Du bist Aura. Antworte auf Deutsch. Kurz (max 2 Sätze)."
        use_history = True
        input_lower = user_input_raw.lower()
        bypass_cache = False

        if any(w in input_lower for w in no_cache_keywords):
            bypass_cache = True
            log_debug("Cache BYPASS: Zufallswort erkannt.")

        # Fall 1: Clipboard
        if any(w in input_lower for w in trigger_clipboard):
            log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten in der Zwischenablage."
                use_history = False
            else:
                return "Die Zwischenablage ist leer."

        # Fall 2: Readme
        elif any(w in input_lower for w in trigger_readme):
            log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                context_data = f"\nPROJEKT DOKUMENTATION (README.md - Auszug):\n'''{readme_content}'''\n"
                system_role = "Du bist der Support-Bot für 'SL5 Aura'. Nutze die Doku."
                use_history = False
            else:
                return "Ich konnte die Readme nicht finden."

        # --- PROMPT BAUEN ---
        full_prompt = f"{system_role}\n"

        if use_history:
            history = load_history()
            if history:
                full_prompt += "\nVerlauf:\n"
                for entry in history:
                    role = "User" if entry['role'] == "user" else "Aura"
                    full_prompt += f"{role}: {entry['content']}\n"

        full_prompt += f"{context_data}\nUser: {user_input_raw}\nAura:"

        # --- CACHE CHECK ---
        if not bypass_cache:
            cached_resp, expired = get_cached_response(full_prompt)
            if cached_resp:
                if use_history:
                    save_to_history(user_input_raw, cached_resp)
                return cached_resp
            if expired:
                log_debug("♻️ Cache Entry EXPIRED.")

        # --- OLLAMA CALL ---
        log_debug("Cache MISS. Rufe Ollama...")
        cmd = ["ollama", "run", "llama3.2"]

        # STDIN für große Inputs!
        result = subprocess.run(
            cmd,
            input=full_prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=90
        )

        if result.returncode != 0:
            return f"Fehler: {result.stderr.strip()}"

        response = clean_text_for_typing(result.stdout.strip())

        if not bypass_cache:
            cache_response(full_prompt, response)

        if use_history:
            save_to_history(user_input_raw, response)

        return response

    except Exception as e:
        log_debug(f"FATAL: {e}")
        return f"Fehler: {str(e)}"
