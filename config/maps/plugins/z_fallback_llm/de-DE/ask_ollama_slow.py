# ask_ollama_slow.py

try:
    # 1. VERSUCH: Relativer Import (für python -m ... Aufruf)
    from . import normalizer

    from . import cache_core
    from . import utils

except ImportError:
    # 2. FALLBACK: Einfacher Import (für Plugin-Lader)
    # WICHTIG: Dies funktioniert nur, wenn die Dateien
    # normalizer.py, cache_core.py, utils.py
    # alle im selben Ordner wie ask_ollama.py liegen.

    import normalizer
    import cache_core
    import utils

import re
import json
# import os
import sys
import logging
# import inspect
import sqlite3
import hashlib
# import datetime
# import random
from pathlib import Path
# import yake


import time

from urllib.error import HTTPError, URLError

import urllib.request

# https://ollama.com/download


# --- KONFIGURATION ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# GLOBAL_NORMALIZED_KEY = ""


SESSION_COUNT = 0

LOG_FILE = "/tmp/aura_ollama_debug.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# --- AUDIO SETUP ---
create_bent_sine_wave_sound = True
try:
    project_root = Path(__file__).resolve().parents[5]
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))
except ImportError:
    pass


# def utils.log_debug2(message: str):
#     caller_info = "UNKNOWN:0"
#     stack = inspect.stack()
#     if len(stack) > 1:
#         try:
#             filename = os.path.basename(stack[1].filename)
#             line_number = stack[1].lineno
#             caller_info = f"{filename}:{line_number}"
#         except Exception:
#             pass
#
#     t = f"⏱️{secDauerSeitExecFunctionStart()}s"
#
#     print(f"{t}:[DEBUG_LLM] {caller_info}: {message}", file=sys.stderr)
#     logging.info(f"{t}:{caller_info}: {message}")


# def normalize_for_hashing(text):
#     return extreme_standardize_prompt_text(text)
#     # text = text.lower()
#     # text = re.sub(r'\s+', ' ', text).strip()
#     # return text


# Sehr aggressive Liste deutscher Stoppwörter (aus der nltk-Bibliothek)
# Hier könnten Sie Ihre eigene, noch längere Liste definieren




# --- INSTANT MODE MATCHING ---
def get_instant_match(user_text):
    """
    Sucht in der DB nach Keywords, die dem User-Text am ähnlichsten sind.
    Nutzt Python Set-Intersection (Schnittmenge) statt LLM.
    """
    utils.init_db()

    # 1. User Text in Worte zerlegen (einfache Normalisierung)
    # EXAMPLE: x s
    user_words = set(re.sub(r'[^\w\s]', '', user_text.lower()).split())
    # Entferne Füllwörter für besseres Matching (optional, aber hilfreich)
    stop_words = {"computer", "aura", "bitte", "danke", "und", "oder", "wie", "was", "ist", "der", "die", "das",
                  "sofort", "schnell", "instant"}
    user_relevant = user_words - stop_words

    if not user_relevant:
        return None

    # utils.log_debug(f"🚀 INSTANT MODE: Suche Match für {user_relevant}...")

    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # Lade alle Prompts, die Keywords haben
        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        best_hash = None
        best_score = 0

        for row in rows:
            db_hash = row[0]
            db_keywords_str = row[1]
            if not db_keywords_str: continue

            db_keywords = set(db_keywords_str.split())

            # Zähle Übereinstimmungen (Intersection)
            matches = user_relevant.intersection(db_keywords)
            score = len(matches)

            if score > best_score:
                best_score = score
                best_hash = db_hash

        # Entscheidung: Wir brauchen mindestens 1 signifikantes Wort als Treffer
        if best_score >= 1:
            utils.log_debug(f"🚀 Instant Match gefunden! Score: {best_score} (Hash: {best_hash[:8]})")

            # Lade eine Antwort zu diesem Hash (bevorzuge gut bewertete)
            c.execute(
                "SELECT response_text FROM responses WHERE prompt_hash=? ORDER BY rating DESC, created_at DESC LIMIT 1",
                (best_hash,))
            resp_row = c.fetchone()
            conn.close()

            if resp_row:
                utils.play_cache_hit_sound()
                # return f"[SOFORT-MODUS]: {resp_row[0]}"
                return f"{resp_row[0]}"
        else:
            utils.log_debug("🚀 Kein ausreichender Match im Instant Modus.")
            conn.close()

        return None

    except Exception as e:
        utils.log_debug(f"Instant Mode Error: {e}")
        return None



# --- HELPER ---
def clean_text_for_typing(text):
    # EXAMPLE: x s . - VAR äöüÄÖÜß
    allowed_chars = r'[^\w\s\.,!\?\-\(\)\[\]\{\}<>äöüÄÖÜß:;\'"\/\\@\+\=\~\#\%]'
    text = re.sub(allowed_chars, '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_readme_content():
    try:
        current_path = Path(__file__).resolve()
        for _ in range(6):
            current_path = current_path.parent
            readme_path = current_path / "README_AI-delang.md"
            if readme_path.exists():
                utils.log_debug(f"README gefunden: {readme_path}")
                content = readme_path.read_text(encoding='utf-8').strip()
                return content[:6000]
        return None
    except Exception as e:
        utils.log_debug(f"{e}")
        return None


def get_clipboard_content():
    if not utils.BRIDGE_FILE.exists(): return None
    try:
        content = utils.BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content: return content
        return None
    except Exception as e:
        utils.log_debug(f"{e}")
        return None


def load_history():
    if not utils.MEMORY_FILE.exists(): return []
    try:
        with open(utils.MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        utils.log_debug(f"{e}")
        return []


def save_to_history(user_text, ai_text):
    history = load_history()
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": ai_text})
    if len(history) > utils.MAX_HISTORY_ENTRIES * 2:
        history = history[-(utils.MAX_HISTORY_ENTRIES * 2):]
    try:
        with open(utils.MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception as e:
        utils.log_debug(f"{e}")
        pass


def secDauerSeitExecFunctionStart(reset=False):
    # Wenn reset=True ist ODER die Funktion zum allerersten Mal läuft: Zeit setzen
    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Differenz berechnen
    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def check_static_guardrails(text_raw):
    """
    Fängt Fragen ab, die auf falschen Annahmen basieren,
    bevor sie teure AI-Zeit verschwenden.
    """
    text = text_raw.lower()

    user_keywords_stict = ["benutzer", "user", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    # Wenn "Benutzer" UND eine "Aktion" vorkommt -> Blocken.
    if any(k in text for k in user_keywords_stict):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter, Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    forbidden_terms = ["account erstellen", "passwort ändern", "login", "neuer benutzer"]
    if any(term in text.lower() for term in forbidden_terms):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts, Passwörter und Logins . "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 1. Benutzerverwaltung (Gibt es nicht)
    user_keywords = ["benutzer", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    user_actions = ["entfernen", "löschen", "erstellen", "hinzufügen", "ändern", "wechseln", "neu"]

    # Wenn "Benutzer" UND eine "Aktion" vorkommt -> Blocken.
    if any(k in text for k in user_keywords) and any(a in text for a in user_actions):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts oder Passwörter, Logins. "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 2. Trigger-Datei Missverständnisse
    # Wenn nach Konfiguration IN der Trigger-Datei gefragt wird
    if "trigger" in text and ("konfigurier" in text or "schreib" in text or "inhalt" in text or "make update" in text):
        return (
            "Die Datei '.sl5_record.trigger' ist eine reine Steuerdatei (Toggle). "
            "Erstellen = Aufnahme Start/Stop. "
            "Konfigurationen gehören ausschließlich nach 'config/'."
        )

    return None


def execute(match_data):
    # play_cache_hit_sound()

    secDauerSeitExecFunctionStart(reset=True)  # <--- Startschuss!

    utils.SESSION_COUNT += 1

    global GLOBAL_NORMALIZED_KEY

    # 1. KANONISCHEN SCHLÜSSEL EINMAL BERECHNEN

    try:
        match_obj = match_data['regex_match_obj']

        # --- FIX START ---
        # Statt match_obj.lastindex zu prüfen (was im Mock fehlt),
        # prüfen wir einfach die Länge des groups()-Tuples.
        # Das funktioniert in Python re UND in Mock-Objekten.
        groups = match_obj.groups()

        user_input_raw = (match_obj.group(2) if len(groups) >= 2 else
                          match_obj.group(1) if len(groups) >= 1 else
                          match_obj.group(0)).strip()
        user_input_raw = user_input_raw.lower()

        # utils.log_debug(f"⏱️{secDauerSeitExecFunctionStart()}s")
        # utils.log_debug(f"Input: {user_input_raw}:'{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        GLOBAL_NORMALIZED_KEY = normalizer.create_ultimate_cache_key(user_input_raw)
        hash_of_normalized_key = cache_core.prompt_key_to_hash(GLOBAL_NORMALIZED_KEY)

        # utils.log_debug(f"GLOBAL_NORMALIZED_KEY: {GLOBAL_NORMALIZED_KEY}")
        # utils.log_debug(f"hash_of_normalized_key: {hash_of_normalized_key}")

        keywords_str = GLOBAL_NORMALIZED_KEY

        # Fängt Unsinn sofort ab (0.00s)
        static_reply = check_static_guardrails(user_input_raw)
        if static_reply:
            utils.log_debug(f"🛡️ Guardrail ausgelöst: '{user_input_raw}'")
            return static_reply

        if "vergiss alles" in user_input_raw.lower():
            if utils.MEMORY_FILE.exists():
                try:
                    utils.MEMORY_FILE.unlink()
                except Exception as e:
                    utils.log_debug(f"{e}")
                    pass
            return "Gedächtnis gelöscht."

        # --- INSTANT MODE CHECK ---
        # Wenn der User "sofort", "schnell" oder "instant" sagt,
        # suchen wir NUR in der DB nach dem besten Keyword-Match.
        instant_triggers = ["sofort", "schnell", "instant"]
        if any(w in user_input_raw.lower() for w in instant_triggers):
            utils.log_debug("Mode: INSTANT REQUEST")
            instant_response = get_instant_match(user_input_raw)
            if instant_response:
                return instant_response
            else:
                return "Dazu habe ich noch keine schnelle Antwort gespeichert."

        AURA_NORMAL_PROFILE = (
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte normal ausführlich und hilfreich. "
            "Deine Antworten dürfen freundlicher sein und mehr Kontext liefern, aber bleibe präzise. "
            "Du bist NICHT an die EXTREM-Kürze des Tech-Modus gebunden.\n\n"

            "REGELN:\n"
            "1. Sei hilfreich und informativ. Liefere eine komplette Antwort.\n"
            "2. Wenn der Benutzer eine Konfiguration oder Regel erstellen will, antworte wie im Tech-Profil (Dateiname und Code-Block), aber füge eine kurze Erklärung hinzu.\n"
            "3. Bei allgemeinen Fragen antworte in ganzen Sätzen und einem angenehmen Ton.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Du hast Zugriff auf Config und Code-Logik. Siehe Tech-Profil für Details.\n"

            "MUSTER-ANTWORTEN:\n"
            "User: Was ist ein Haus?\n"
            "Aura: Ein Haus ist ein dauerhaftes, überdachtes Bauwerk, das als Unterkunft oder Schutz dient.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "Aura: Gerne, hier ist die Regel für Stern:\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n"
        )

        AURA_TECH_PROFILE = (  # noqa: F841
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte EXTREM kurz.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk' (Keine Einleitungen, kein 'Hier ist der Code').\n"
            "2. Wenn du etwas nicht weißt oder es nicht zu Aura gehört: Sage 'Dazu habe ich keine Infos.' (Nicht leer bleiben!).\n"
            "3. Bei BEFEHLEN (Erstelle Regel): Antworte NUR mit dem Dateinamen und dem Regel-Tupel.\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            "- Logik: Regex Listen als Tupel.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (PUNCTUATION_MAP.py)  > Maps (...pre.py) > LanguageTool (Opt.) > Maps (...post.py) > Output (Text & TTS).\n"
            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Umgebung: Headless (Keine GUI). Offline.\n\n"

            "SYSTEM-WISSEN:\n"
            
            # --- RegEx-Verarbeitung (Top-Down & Stopp-Logik) ---
            "- RegEx-Tupel: (`Name`, `RegEx`, **`Value_Ignored`**, `Flags`)\n" # <--- Klares Label für den IGNORIERTEN WERT
            "- RegEx-Regeln werden strikt **Top-Down** im Code verarbeitet (keine Prioritäts-Sortierung).\n"
            "- WICHTIG: Ein RegEx-Match, der den gesamten Text ersetzt (Full-Match), **stoppt** die weitere Verarbeitung.\n"
            
            # --- Fuzzy-Logik (Threshold) ---
            "- Fuzzy-Tupel: (`Ersetzung`, `Match-Phrase`, **`Threshold`**, ...)\n" # <--- Klares Label für den AKTIVEN WERT
            "- Die **Fuzzy-Suche** (verwendet 'fuzzywuzzy' und 'token_set_ratio') wird nur als **letzter Fallback** ausgeführt, wenn KEINE RegEx gefunden wurde.\n"
            "- Der **`Threshold`** (0-100) im Fuzzy-Tupel ist der Mindest-Score, den das Fuzzy-Matching erreichen muss. Er hat **KEINE** Funktion im RegEx-Tupel.\n"
            
            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine PUNCTUATION-Regel für Stern.\n"
            "```python\n"
            "# PUNCTUATION-Tupel: (Suchwort, neues Wort)\n"
            "'stern': '*'\n"
            "```\n\n"

            "User: Erstelle eine Regex-Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Ersetzung, Regex, Priorität, Flags)\n"
            # EXAMPLE: Bundeskanzlerin
            "('Angela Merkel', r'^(Bundeskanzlerin|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: catch_all.py\n"
            "```python\n"
            "('Ersetzung', r'^.*$', 10, {})\n"
            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki ...
            "('Ersetzung', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"

        )























        ollama_normal_params = {
            "temperature": 0.3,
            "mirostat": 2,
            "num_predict": 512,  # Wert für gründliche Antworten
        }







        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]
        trigger_readme = ["hilfe", "dokumentation", "readme", "read me", "wie funktioniert", "was kannst du"]
        no_cache_keywords = ["witz", "spruch", "zufall", "random"]

        # --- Modus-Initialisierung (FEST auf NORMAL setzen) ---
        mode_prefix = "NORMAL"
        system_role = AURA_NORMAL_PROFILE  # Immer den Normal-Prompt verwenden
        ollama_params = ollama_normal_params  # Immer die Normal-Params verwenden
        use_history = True  # History beibehalten, da es Kontext ist


        context_data = ""
        input_lower = user_input_raw.lower()
        bypass_cache = True
        context_prefix = ""


        # --- MODE DETECTION & KONTEXT LADEN ---
        # Hier bestimmen wir nur: Welcher Modus ist aktiv? Welcher Kontext wird geladen?

        # utils.log_debug(f"Input: {user_input_raw}:'{user_input_raw}'")
        # utils.log_debug(f"Input: {input_lower}:'{input_lower}'")

        if any(w in input_lower for w in no_cache_keywords):
            bypass_cache = True
            utils.log_debug("Cache BYPASS: Zufallswort erkannt.")

        # 1. CLIPBOARD CHECK
        elif any(w in input_lower for w in trigger_clipboard):
            utils.log_debug("Mode: CLIPBOARD")
            content = get_clipboard_content()
            if content:
                content_preview = content[:50] + str(len(content))
                # Hash des Inhalts wird Teil des Prefix -> Inhalt ändert sich = Cache ändert sich
                clip_hash = hashlib.md5(content_preview.encode()).hexdigest()
                mode_prefix = f"CLIP_{clip_hash}"

                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten."
                use_history = False
            else:
                return "Zwischenablage ist leer."

        # 2. README CHECK
        elif any(w in input_lower for w in trigger_readme):
            utils.log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                # Hash der Readme wird Teil des Prefix -> Doku ändert sich = Cache ändert sich
                readme_hash = hashlib.md5(readme_content.encode()).hexdigest()
                mode_prefix = f"README_{readme_hash}"

                context_data = f"\nPROJEKT DOKUMENTATION:\n'''{readme_content}'''\n"
                system_role = (f"Support-Bot für 'SL5 Aura'. Fakten:\n{AURA_TECH_PROFILE}\nErfinde nichts.")
                use_history = False
            else:
                return "Readme nicht gefunden."

        # 3. STANDARD (Fallback ist "STD", wie oben initialisiert)

        # --- HASH BERECHNUNG ---

        # 1. Keywords IMMER sofort generieren (für Cache-Key UND DB-Speicherung)
        # Das macht den Cache "fuzzy" -> "Erstelle Regel" und "Regel erstellen" landen im selben Cache!

        # utils.log_debug(f"Keywords<execute 🔎 {keywords_str} 🔍")

        # Fallback: Wenn keine Keywords gefunden wurden (z.B. nur Füllwörter), nimm den Raw Text
        if not keywords_str:
            base_for_hash = user_input_raw
        else:
            base_for_hash = keywords_str

        # 2. Den Hash-String bauen
        if "CLIP" in mode_prefix or "README" in mode_prefix:
            # Bei Clipboard/Readme muss der Inhalt (Prefix) Teil des Hashes sein
            hash_input_string = f"{mode_prefix}|{base_for_hash}"
        else:
            # Im Standard-Modus zählt nur das Keyword-Set
            # Frage: "Aura wie spät" -> Key: "STD|spät"
            # Frage: "Wie spät ist es" -> Key: "STD|spät" -> TREFFER!
            hash_input_string = f"STD|{base_for_hash}"

        context_prefix = context_prefix if 'context_prefix' in locals() else ""
        hash_input_string = f"{mode_prefix}|{context_prefix}|{base_for_hash}"

        # utils.log_debug(f"🔑 base_for_hash: '{base_for_hash}'")
        # utils.log_debug(f"🔑 hash_input_string: '{hash_input_string}'")

        # Full Prompt für die AI (bleibt wie es war, für Context)
        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"
        if use_history:
            hist = load_history()
            full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(hist)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- CACHE CHECK ---

            # --- AI GENERIERUNG (OLLAMA API) ---
        # utils.log_debug("Cache MISS. Sende API-Request an Ollama...")

            # --- AI GENERIERUNG (OLLAMA API) ---
            utils.log_debug("Cache BYPASS (Slow Mode). Sende API-Request an Ollama...")

        payload = {
            "model": "llama3.2:latest",
            "prompt": full_prompt_for_generation,
            "stream": False,
            "options": ollama_params
        }


        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})

            # Timeout erhöht auf 120s für Sicherheit
            with urllib.request.urlopen(req, timeout=120) as response:
                api_response = json.loads(response.read().decode('utf-8'))

            utils.SUM_PER_CACHE = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
            utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()

            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            utils.log_debug(
                f"Nr. {utils.SESSION_COUNT} | CACHE_HITS:{utils.SESSION_CACHE_HITS} 📊 CacheHITs/Nr.: {sum_per_cache_str} | "
                f"⌚ Gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")

            raw_text = api_response.get("response", "")

            answer_for_all_fallback = (
                "Aura Status: Offline-System, Single-User (Keine Logins/Accounts).\n"
                "Pfade: Configs in 'config/', Regeln in 'config/maps/'.\n\n"

                "FORMAT 1: Einfache Ersetzung (z.B. PUNCTUATION_MAP)\n"
                "Synatx: 'Wort': 'Ersatz'\n"
                "Beispiel: 'stern': '*'\n\n"

                "FORMAT 2: Logik-Regeln (z.B. FUZZY_MAP)\n"
                "Syntax: (Name, Regex, Prio, Flags)\n"
                # EXAMPLE: Kanzlerin
                "Beispiel: ('Merkel', r'^(Kanzlerin|Angie)$', 100, {'flags': re.IGNORECASE})\n"
                # EXAMPLE: Wiki ...
                "Beispiel: ('Wiki', r'^Wiki (.*)$', 50, {'on_match_exec': 'wiki_search'})\n\n"

                "Doku: https://SL5.de/Aura"
            )

            if not raw_text:
                response = answer_for_all_fallback

            response = clean_text_for_typing(raw_text)

            response.replace('sl5_config.py', ' settings_local.py ')
            response.replace(' sl5_record_trigger.py ', ' /tmp/sl5_record.trigger ')

            response = response.replace('JSON', 'Python')
            response = response.replace('YAML', 'Python')
            response = response.replace('json', 'Python')
            response = response.replace('Aurah ', 'Aura ')
            response = response.replace('config/maps/Ordner', 'config/maps Ordner')

            # Dazu habe ich keine Infos
            if 'Dazu habe ich keine Info' in response or 'sl5_record_trigger.py' in response:
                response = answer_for_all_fallback

            if (False  # noqa: E129
                or "r'/tmp" in response # noqa: E127
                or 'user_map.py' in response # noqa: E127
                or 'user_regeln.py' in response): # noqa: E127 E129
                response = answer_for_all_fallback # noqa: E127

            if 'Fehler:' in response or '.json' in response:
                response = answer_for_all_fallback

            # --- SPEICHERN ---
            if not bypass_cache:
                # utils.log_debug(f"bypass_cache: {bypass_cache}")
                # WICHTIG: Wir nutzen hier denselben hash_input_string (basierend auf Keywords),
                # den wir oben zum Lesen benutzt haben!
                # cache_response(hash_input_string, response, user_input_raw, keywords=keywords_str)

                cache_core.cache_response(
                    tag_keyword=hash_input_string,
                    response_text=response,
                    clean_user_input=user_input_raw,
                    hash_of_normalized_key=hash_of_normalized_key
                )

            if use_history:
                save_to_history(user_input_raw, response)

            return response


        # --- FEHLER BEHANDLUNG ---
        except HTTPError as e:
            # Hier fangen wir den "Server response: 500" ab
            if e.code == 500:
                utils.log_debug(f"❌ OLLAMA SERVER ERROR (500). Ignoriere Fehlertext für User.")
                # Wenn du NICHT willst, dass der User den Fehler sieht:
                return "Ich habe kurz den Faden verloren. Kannst du das wiederholen?"
            else:
                utils.log_debug(f"API HTTP Error: {e.code}")
                return f"Server Fehler: {e.code}"

        except URLError as e:
            # Wenn Ollama gar nicht läuft (Connection refused)
            utils.log_debug(f"API Connection Error: {e.reason}")
            return "Fehler: Keine Verbindung zu Ollama."

        except Exception as e:
            # Alle anderen Fehler
            utils.log_debug(f"API General Error: {e}")
            # return "Ein interner Fehler ist aufgetreten."
            return (
                "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
                "Es gibt keine Logins, Accounts. "
                "Du bist der einzige Nutzer (Besitzer des Geräts). "
                "Bitte lese Details in der Dokumentation: https://SL5.de/Aura"
            )







    except Exception as e:
        utils.log_debug(f"API Error: {e}")
        return f"Interner Fehler: {str(e)}"







