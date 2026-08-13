# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py

# ask_ollama.py

import datetime
import os
# import torch


try:
    # 1. TRY: Relative import (for python -m ... call)

    from . import normalizer

    from . import cache_core
    from . import utils

except ImportError:
    # 2. FALLBACK: Easy import (for plugin loaders)

    # IMPORTANT: This only works if the files

    # normalizer.py, cache_core.py, utils.py

    # are all in the same folder as ask_ollama.py.


    import normalizer
    import cache_core
    import utils

import re
import json
# import os

import sys
import logging
# import inspection

import sqlite3
import hashlib
# import datetime

# import random

from pathlib import Path
# import yake



import time

from urllib.error import HTTPError, URLError

import urllib.request


# from sentence_transformers import SentenceTransformer, util



# https://ollama.com/download



# --- CONFIGURATION ---

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

# caller_info = "UNKNOWN:0"

# stack = inspect.stack()

# if len(stack) > 1:

# try:

# filename = os.path.basename(stack[1].filename)

# line_number = stack[1].lineno

# caller_info = f"{filename}:{line_number}"

# except Exception:

# passport

#
# t = f"⏱️{secDurationSinceExecFunctionStart()}s"

#
# print(f"{t}:[DEBUG_LLM] {caller_info}: {message}", file=sys.stderr)

# logging.info(f"{t}:{caller_info}: {message}")



# def normalize_for_hashing(text):

# return extreme_standardize_prompt_text(text)

# # text = text.lower()

# # text = re.sub(r'\s+', ' ', text).strip()

# # return text



# Very aggressive list of German stop words (from the nltk library)

# Here you could define your own, even longer list



# def extreme_standardize_prompt_text(text):

# global STOP_WORDS_DE_EXTREME

#
# # Initialize the German stemmer

# stemmer = GermanStemmer()

#
#
# #1. All lowercase

# text = text.lower()

#
# #2. Replace ALL numbers, times and currency symbols with wildcards

# text = re.sub(r'\d+([.,]\d+)?', ' [NUMBER] ', text) # E.g. '10', '10.5'

# text = re.sub(r'[€$£%]', ' ', text)

#
# #3. Radical removal of almost all special characters and punctuation marks

# text = re.sub(r'[^a-zäöüß\s]', ' ', text)

#
# #4. Reduce whitespace to a single space and trim

# text = re.sub(r'\s+', ' ', text).strip()

#
# #5. Tokenization (separating words)

# words = text.split()

#
# #6. Stop word removal and stemming

# stemmed_words = []

# for word in words:

# if word not in STOP_WORDS_DE_EXTREME:

# # Reduce the word to its stem (stemming)

# stemmed_words.append(stemmer.stem(word))

#
# #7. Reassemble words into a string

# text = ' '.join(stemmed_words)

#
# utils.log_debug(f"keywords<lastLine<extreme_standardize_prompt_text: 🔎 {text.strip()} 🔍")

#
# return text.strip()



# --- Example test ---

# Prompt 1: “How many houses do we have to choose from in the area?”

# Stemmed: "we have a choice of area in the house"

# Extreme Stemmed: "wiel haus hab area wahl" (after stop word removal)


# Prompt 2: "The house is expensive, but very nice."

# Extreme Stemmed: "house expensive beautiful"


# Prompt 3: “How many houses are in the area?”

# Extreme Stemmed: "how much house area"


# 1. Load model (locally, approx. 80MB, very fast)

# 'all-MiniLM-L6-v2' is the industry standard for fast local searches

# model = SentenceTransformer('all-MiniLM-L6-v2')


_model = None  # Globaler Cache für das Modell

def get_embedding_model():
    """
    Lazy loader for the embedding model.
    Only loads torch and the model into RAM when actually needed.
    """
    global _model
    if _model is None:
        utils.log_debug("🚀 Loading Embedding Model (Lazy Load)…")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model


# config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:153


log = logging.getLogger("simulate_conversation")
GITHUB_BASE = "https://github.com/sl5net/SL5-aura-service/blob/master"

def get_github_url(file_path):
    """Erstellt den passenden GitHub-Link aus dem lokalen Pfad."""
    rel_path = ""
    if "STT/" in str(file_path):
        rel_path = str(file_path).split("STT/")[1]
    elif "SL5-aura-service/" in str(file_path):
        rel_path = str(file_path).split("SL5-aura-service/")[1]
    if rel_path:
        url = f"{GITHUB_BASE}/{rel_path}"
        log.debug(f"get_github_url: {file_path} -> {url}")
        return url
    log.warning(f"get_github_url: kein STT/ oder SL5-aura-service/ in Pfad: {file_path}")
    return None


def save_to_aura_db(question, answer, file_path, use_semantics=False):
    """
    Version 1.2.0: Saves dialogue pairs including a semantic vector embedding.
    Enables the 'Self-Learning' loop for the interactive chat.
    """
    prompt_hash = hashlib.md5(question.encode('utf-8')).hexdigest()
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    clean_input = question.lower().replace("?", "").strip()

    embedding_blob = None
    if use_semantics: # Nur für den interaktiven Chat aktivieren
        import pickle
        model = get_embedding_model()
        embedding = model.encode(question)
        embedding_blob = pickle.dumps(embedding)

    github_link = get_github_url(file_path)

    try:
        # conn = sqlite3.connect(DB_PATH)

        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        conn.execute("PRAGMA journal_mode=WAL;")

        cursor = conn.cursor()

        # 1. Save to 'prompts' - now including EMBEDDING

        cursor.execute("""
            INSERT OR IGNORE INTO prompts (hash, prompt_text, last_used, clean_input, keywords, embedding)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (prompt_hash, question, now, clean_input, "radio_deep_dive", embedding_blob))

        # 2. Save to 'responses'

        cursor.execute("""
            INSERT INTO responses (prompt_hash, response_text, created_at, usage_count, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (prompt_hash, answer, now, 0, github_link))

        # 3. Update tracking table

        current_mtime = os.path.getmtime(file_path)
        cursor.execute("""
            INSERT OR REPLACE INTO radio_processed_files (file_path, last_mtime, last_generated)
            VALUES (?, ?, ?)
        """, (str(file_path), current_mtime, now))

        conn.commit()
        conn.close()
        # utils.log_debug(f"✅ Saved (incl. vector): {question[:30]}…")

    except Exception as e:
        print(f"Database Error: {e}")


def get_semantic_match(user_text):
    # 1. Encode user input once


    from sentence_transformers import util
    model = get_embedding_model()
    user_embedding = model.encode(user_text, convert_to_tensor=True)
    try:
        conn = sqlite3.connect(utils.DB_FILE, timeout=90)
        c = conn.cursor()
        # 2. Fetch PRE-CALCULATED embeddings (BLOBs)

        c.execute("SELECT hash, embedding FROM prompts WHERE embedding IS NOT NULL")
        rows = c.fetchall()
        best_hash, max_sim = None, 0.0

        SEMANTIC_THRESHOLD = 0.7  # Live-Betrieb
        # SEMANTIC THRESHOLD = -1.0 # Test always match


        for db_hash, blob in rows:
            # 3. Load vector from BLOB (no model.encode here!)

            import pickle
            import torch
            db_embedding = torch.from_numpy(pickle.loads(blob)).to(user_embedding.device)
            # db_embedding = model.encode(user_text, convert_to_tensor=True)


            similarity = util.cos_sim(user_embedding, db_embedding).item()

            if similarity > max_sim:
                max_sim, best_hash = similarity, db_hash
        if best_hash and max_sim > SEMANTIC_THRESHOLD:
            c.execute("SELECT response_text FROM responses WHERE prompt_hash=? LIMIT 1", (best_hash,))
            res = c.fetchone()

            conn.close()

            if res:
                utils.play_cache_hit_sound()
                return res[0]
        return None
    except Exception as e:
        utils.log_debug(f"Semantic Error: {e}")
        return None


# def get_semantic_match_22222(user_text):

# """

# Performs a semantic search for the best matching response.

# Uses Cosine Similarity to find matches even without exact keyword overlaps.

# """

# # utils.init_db()

#
# # Convert user input into a vector embedding

# user_embedding = model.encode(user_text, convert_to_tensor=True)

#
# try:

# conn = sqlite3.connect(utils.DB_FILE)

# c = conn.cursor()

# # Fetch pre-calculated embeddings from the database

# c.execute("SELECT hash, prompt_text FROM prompts")

# rows = c.fetchall()

#
# utils.log_debug(f"DEBUG: Semantic Search loaded {len(rows)} embeddings from {utils.DB_FILE}")

#
# best_hash = None

# max_similarity = 0.0

# threshold = 0.3

# threshold = -1.0

#
# for row in rows:

# db_hash, db_text = row[0], row[1]

#
# # Calculate semantic similarity

# db_embedding = model.encode(db_text, convert_to_tensor=True)

# similarity = util.cos_sim(user_embedding, db_embedding).item()

#
# if similarity > max_similarity:

# max_similarity = similarity

# best_hash = db_hash

#
# if best_hash and max_similarity > threshold:

# utils.log_debug(f"🧠 Semantic Match! Score: {max_similarity:.2f}")

#
# utils.log_debug(f"🚀 Instant match found! (Hash: {best_hash[:8]})")

#
# c.execute(

# "SELECT response_text FROM responses WHERE prompt_hash=? ORDER BY rating DESC, created_at DESC LIMIT 1",

# (best_hash,))

# resp_row = c.fetchone()

# conn.close()

#
# if resp_row:

# utils.play_cache_hit_sound()

# # return f"[IMMEDIATE MODE]: {resp_row[0]}"

# return f"{resp_row[0]}"

#
# return db_text

#
# return None

# except Exception as e:

# utils.log_debug(f"Semantic Error: {e}")

# return None


# --- INSTANT MODE MATCHING ---

def get_instant_match(user_text):
    """
    Sucht in der DB nach Keywords, die dem User-Text am ähnlichsten sind.
    Nutzt Python Set-Intersection (Schnittmenge) statt LLM.
    """
    # utils.init_db()


    # 1. Break user text into words (simple normalization)

    # EXAMPLE: xs

    user_words = set(re.sub(r'[^\w\s]', '', user_text.lower()).split())
    # Remove noise words for better matching (optional but helpful)

    stop_words = {"computer", "aura", "bitte", "danke", "und", "oder", "wie", "was", "ist", "der", "die", "das",
                  "sofort", "schnell", "instant"}
    user_relevant = user_words - stop_words

    if not user_relevant:
        return None

    # utils.log_debug(f"🚀 INSTANT MODE: Finding match for {user_relevant}…")


    try:
        conn = sqlite3.connect(utils.DB_FILE)
        c = conn.cursor()

        # Load all prompts that have keywords

        c.execute("SELECT hash, keywords FROM prompts WHERE keywords IS NOT NULL")
        rows = c.fetchall()

        best_hash = None
        best_score = 0

        for row in rows:
            db_hash = row[0]
            db_keywords_str = row[1]
            if not db_keywords_str: continue

            db_keywords = set(db_keywords_str.split())

            # Count matches (Intersection)

            matches = user_relevant.intersection(db_keywords)
            score = len(matches)

            if score > best_score:
                best_score = score
                best_hash = db_hash

        # Decision: We need at least 1 significant word as a hit

        if best_score >= 1:
            utils.log_debug(f"🚀 Instant Match gefunden! Score: {best_score} (Hash: {best_hash[:8]})")

            # Upload an answer to this hash (prefer well rated ones)

            c.execute(
                "SELECT response_text FROM responses WHERE prompt_hash=? ORDER BY rating DESC, created_at DESC LIMIT 1",
                (best_hash,))
            resp_row = c.fetchone()
            conn.close()

            if resp_row:
                utils.play_cache_hit_sound()
                # return f"[IMMEDIATE MODE]: {resp_row[0]}"

                return f"{resp_row[0]}"
        else:
            utils.log_debug("🚀 Kein ausreichender Match im Instant Modus.")
            conn.close()

        return None

    except Exception as e:
        utils.log_debug(f"Instant Mode Error: {e}")
        return None


# ask_ollama.py



# def get_professional_keywords(text):

# return extreme_standardize_prompt_text(text)

#
# """

# Hybrid approach: First filter out garbage, then determine keywords.

# """

# #1. Hardcore stopword list for voice commands

# # ignore_words = {

# # "aura", "computer", "pc", "system", "hello", "hey", "please", "thank you",

# # "create", "make", "make", "do", "generate", "show", "show",

# # "a", "an", "an", "the", "the", "that", "and", "or", "with",

# # "rules", "rule", "text", "string" # Often filler words in your context

# # }

#
#
# synonyms = {

# # commands

# "create": "new", "create": "new", "generate": "new", "make": "new",

# "make": "new", "write": "new", "add": "new", "new": "new",

# # Info

# "show": "info", "show": "info", "where": "info", "how": "info", "help": "info", "explain": "info",

# # Delete

# "delete": "del", "remove": "del", "forget": "del",

# # Context

# "config": "config", "configuration": "config", "settings": "config",

# "regex": "rule", "rules": "rule", "pattern": "rule"

# }

#
# ignore_words = {

# "aura", "computer", "pc", "system", "hello", "hey", "hi",

# "please", "thank you", "time", "just", "quickly", "shortly",

# "a", "an", "an", "an", "an",

# "the", "the", "that", "dem", "den",

# "and", "or", "with", "from", "in", "in", "to", "for", "on", "for",

# "is", "are", "was", "would", "can", "you", "me", "and", "I"

# }

#
# try:

# # Clean text

# words = re.findall(r'\w+', text.lower())

#
# final_tokens = []

# for w in words:

# #1. Ignore?

# if w in ignore_words:

# continue

#
# #2. Replace synonym?

# if w in synonyms:

# final_tokens.append(synonyms[w])

# else:

# #3. Keep your word

# final_tokens.append(w)

#
# if not final_tokens:

# return ""

#
# # 4. Sort: "Light on" and "On light" become identical ("on light")

# # final_kws = sorted(list(set(final_tokens)))

# # return " ".join(final_kws)

#
#
#
#
#
# relevant_words = [w for w in final_tokens if w not in ignore_words and len(w) > 2]

# clean_text = " ".join(relevant_words)

#
# if not clean_text:

# return "" # No keywords (better than garbage)

#
# # Try YAKE on the cleaned text

# import yake

# kw_extractor = yake.KeywordExtractor(lan="de", n=1, dedupLim=0.9, top=3)

# keywords = kw_extractor.extract_keywords(clean_text)

#
# # Return sorted list

# final_kws = sorted([k[0].lower() for k in keywords])

# return " ".join(final_kws)

#
# except ImportError:

# # Fallback without YAKE

# return " ".join(sorted(list(set(relevant_words))))

# except Exception:

# return ""



# --- HELPER ---

def clean_text_for_typing(text):
    # EXAMPLE: x. - VAR äöüÄÖÜß

    allowed_chars = r'[^\w\s\.,!\?\-\(\)\[\]\{\}<>äöüÄÖÜß:;\'"\/\\@\+\=\~\#\%]'
    text = re.sub(allowed_chars, '', text)
    # EXAMPLE: None

    text = re.sub(r'\s+', ' ', text).strip()
    return text


def get_readme_content():
    try:
        readme_path = Path(__file__).parent / "README_AI-delang.md"
        if readme_path.exists():
            return readme_path.read_text(encoding='utf-8').strip()[:6000]

        hint = (
            "README_AI-delang.md nicht gefunden.\n"
            "Bitte erstelle sie mit einer großen AI (z.B. Claude/GPT) und folgendem Prompt:\n\n"
            "---\n"
            "Lies die Datei README.md dieses Projekts und erstelle daraus eine kompakte\n"
            "Version für ein lokales Ollama-Modell (llama3.2, 3B Parameter).\n"
            "Anforderungen:\n"
            "- Max 2000 Zeichen\n"
            "- Kein Markdown, nur Fließtext\n"
            "- Fakten: Python, Regeln als Tupel in FUZZY_MAP_pre.py,\n"
            "  Pipeline: Vosk → PUNCTUATION_MAP → FUZZY_MAP_pre → LanguageTool → FUZZY_MAP\n"
            "- Trigger: /tmp/sl5_record.trigger\n"
            "- Kein GUI, kein JSON, kein YAML\n"
            "- Sprache: Deutsch, technisch, direkt\n"
            "Speichern als README_AI-delang.md\n"
            f"Speichern als: {readme_path}"
            "---"
        )
        print(hint)
        log.info(hint)

        return None
    except Exception as e:
        return None
        utils.log_debug(f"get readme Error: {e}")



def get_clipboard_content():
    if not utils.BRIDGE_FILE.exists(): return None
    try:
        content = utils.BRIDGE_FILE.read_text(encoding='utf-8').strip()
        if content:
            return content
        return None
    except Exception:
        return None


def load_history():
    if not utils.MEMORY_FILE.exists(): return []
    try:
        with open(utils.MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
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
    except Exception:
        pass


def secDauerSeitExecFunctionStart(reset=False):
    # If reset=True OR the function runs for the very first time: set time

    if reset or not hasattr(secDauerSeitExecFunctionStart, "start_time"):
        secDauerSeitExecFunctionStart.start_time = time.time()
        return 0.00

    # Calculate difference

    duration = time.time() - secDauerSeitExecFunctionStart.start_time
    return round(duration, 2)


def check_static_guardrails(text_raw):
    """
    Fängt Fragen ab, die auf falschen Annahmen basieren,
    bevor sie teure AI-Zeit verschwenden.
    """
    text = text_raw.lower()

    user_keywords_stict = ["benutzer", "user", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    # If "User" AND an "Action" occurs -> Block.

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

    # 1. User management (does not exist)

    user_keywords = ["benutzer", "account", "konto", "login", "anmelden", "registrieren", "whatsapp"]
    user_actions = ["entfernen", "löschen", "erstellen", "hinzufügen", "ändern", "wechseln", "neu"]

    # If "User" AND an "Action" occurs -> Block.

    if any(k in text for k in user_keywords) and any(a in text for a in user_actions):
        return (
            "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
            "Es gibt keine Accounts oder Passwörter, Logins. "
            "Du bist der einzige Nutzer (Besitzer des Geräts)."
        )

    # 2. Trigger file misunderstandings

    # When asked for configuration IN the trigger file

    if "trigger" in text and ("konfigurier" in text or "schreib" in text or "inhalt" in text or "make update" in text):
        return (
            "Die Datei '.sl5_record.trigger' is one pure Control file (Toggle). "
            "Erstellen = Aufnahme Start/Stop. "
            "Konfigurationen gehören ausschließlich nach 'config/'."
        )

    return None


def execute(match_data):
    print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")

    # play_cache_hit_sound()


    secDauerSeitExecFunctionStart(reset=True)  # <--- Startschuss!

    utils.SESSION_COUNT += 1

    global GLOBAL_NORMALIZED_KEY

    # 1. CALCULATE CANONIC KEY ONCE


    try:
        match_obj = match_data['regex_match_obj']

        # --- FIX START ---

        # Instead of checking match_obj.lastindex (which is missing in the mock),

        # let's just check the length of the groups() tuple.

        # This works in Python re AND in mock objects.

        groups = match_obj.groups()

        # user_input_raw = (match_obj.group(2) if len(groups) >= 2 else

        # match_obj.group(1) if len(groups) >= 1 else

        # match_obj.group(0)).strip()


        # always take the last group

        user_input_raw = groups[-1].strip() if groups else match_obj.group(0).strip()
        user_input_raw = user_input_raw.lower()

        utils.log_debug(f"⏱️{secDauerSeitExecFunctionStart()}s")
        utils.log_debug(f"Input: {user_input_raw}:'{user_input_raw}'")

        if not user_input_raw: return "Nichts gehört."

        GLOBAL_NORMALIZED_KEY = normalizer.create_ultimate_cache_key(user_input_raw)
        hash_of_normalized_key = cache_core.prompt_key_to_hash(GLOBAL_NORMALIZED_KEY)

        # utils.log_debug(f"GLOBAL_NORMALIZED_KEY: {GLOBAL_NORMALIZED_KEY}")

        # utils.log_debug(f"hash_of_normalized_key: {hash_of_normalized_key}")


        keywords_str = GLOBAL_NORMALIZED_KEY

        # Catches nonsense immediately (0.00s)

        static_reply = check_static_guardrails(user_input_raw)
        if static_reply:
            utils.log_debug(f"🛡️ Guardrail ausgelöst: '{user_input_raw}'")
            return static_reply

        if "vergiss alles" in user_input_raw.lower():
            if utils.MEMORY_FILE.exists():
                try:
                    utils.MEMORY_FILE.unlink()
                except Exception:
                    pass
            return "Gedächtnis gelöscht."

        # --- INSTANT MODE CHECK ---

        # If the user says "immediately", "quickly" or "instantly",

        # we ONLY search the DB for the best keyword match.

        instant_triggers = ["sofort", "schnell", "instant"]
        if any(w in user_input_raw.lower() for w in instant_triggers):
            utils.log_debug("Mode: INSTANT REQUEST")
            instant_response = get_instant_match(user_input_raw)

            if instant_response:
                return instant_response
            else:
                return "Dazu habe ich noch keine schnelle Antwort gespeichert."

        # --- AURA TECH PROFILE (Grounding & Facts) ---

        # --- AURA TECH PROFILE (Grounding & Facts) ---

        AURA_TECH_PROFILE_2911252235Sat = (  # noqa: F841
            "Du bist SL5 Aura. Antworte auf Deutsch. Sei extrem kurz.\n"

            "ANWEISUNG FÜR DICH:\n"
            "Unterscheide selbstständig:\n"
            "1. WISSENSFRAGE (Wo/Was/Wie) -> Nur den Fakt nennen (1 Satz).\n"
            "2. HANDLUNG (Erstelle/Schreibe) -> Nur Dateiname und Code-Block.\n\n"

            "BEISPIELE (Nutze diesen Stil):\n"
            "User: 'Wo sind die Configs?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: 'Wie starte ich die Aufnahme?'\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "SYSTEM-FAKTEN (Strict Grounding):\n"
            "About: Privacy-first voice assistant framework. Core is offline. Scripts allow hybrid usage.\n"
            "1. Tech Stack: Python (87%), Shell (9%), PowerShell (2%), Vosk (Offline-Modelle ~4GB), LanguageTool. KEIN Java/C++, KEINE .exe, KEIN PDF-Support.\n"
            "2. Interface: 100% 'Headless' Hintergrund-Dienst. Interaktion NUR via Mikrofon (Input) & Terminal-Logs (Output). ES GIBT KEINE 'OBERFLÄCHE', KEINE GUI, KEIN Web-UI.\n"
            "3. Logik & Config: KEIN JSON/YAML! Regeln sind reine Python-Dateien (z.B. 'FUZZY_MAP_pre.py') mit Regex-Listen.\n"
            "   - In config/ befinden sich alle KONFIGURATION .\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer) oder spezifisch `^meinBefehl$`. (KEIN Button, reiner Code!)\n"
            "   - Syntax WICHTIG: Nutze Python 're' Syntax. Für Alternativen (ODER) nutze zwingend '|' ohne Leerzeichen!\n"
            "     FALSCH: `(Hans Max Luis)` -> RICHTIG: `(Hans|Max|Luis)`\n"
            "     FALSCH: `[Licht Lampe]`   -> RICHTIG: `(Licht|Lampe)`\n"
            "   - Lade-Reihenfolge: Plugin-ORDNER werden alphabetisch geladen (A-Z).\n"
            "   - Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "   - Stopp (Full-Match): Die Pipeline stoppt, wenn ein Regex von Anfang (`^`) bis Ende (`$`) matcht. Da Voice-Input einzeilig ist, sind Anker wichtig.\n"
            "   - In config/ befinden sich alle KONFIGURATIONEN.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            # EXAMPLE: Chancellor

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Chancellor|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "4. Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"
            "   - Beispiele: Offline-Wikipedia, SQLite-Booksearch, Ollama AI (Lokal).\n"
            "   - Ausnahme: Das 'Translate'-Plugin nutzt Online-APIs (mit lokalem Cache), benötigt also Internet.\n"
            "5. Security & Tools: \n"
            "   - Dateisuche: NUR via 'git ls-files | fzf'.\n"
            "   - Findet Aura eine versteckte '. Dateiname .py'(Punkt am Anfang), nutzt es deren Passwort zum Entpacken von _ einName .zip (OPTIONAL, nicht vorhanden).\n"
            "6. OS: Linux, Windows, macOS. (Kein Smartphone).\n"
            "7. Installation: Dauert ca. 10-20 Minuten (Download großer Sprachmodelle, >4GB). Updates sind schnell, Erst-Installation NICHT.\n"
            "   - App-Update: Via 'git pull' (Sekunden).\n"
            "   - Modell-Update: Lösche den entsprechenden Ordner in 'models/' und starte das Setup-Skript erneut. (Dauert 10-20 Min, >4GB Download).\n"
            "8. Externe Trigger (CopyQ, AutoKey, AHK): Steuerung erfolgt NUR durch Erstellen einer leeren Datei (File-Watch). KEINE API, KEINE Config!\n"
            "   - Pfad Linux/Mac: `/tmp/sl5_record.trigger`\n"
            "   - Pfad Windows: `c:\\tmp\\sl5_record.trigger`\n"
            "   - Funktion: Datei erstellen = Aufnahme/Verarbeitung starten.\n"
            "9. Verhalten: Erfinde KEINE visuellen Elemente. Fasse dich EXTREM kurz (Max 15 Wörter)."

            "BEISPIEL-DIALOGE (Lerne die Unterscheidung!):\n"
            "User: 'Wo finde ich die Konfiguration?'\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/'.\n\n"

            "User: 'Welche Datei startet die Aufnahme in Linux?'\n"
            "Aura: Das Erstellen der Datei '/tmp/sl5_record.trigger' starts the Recording  in Linux .\n\n"

            "BEISPIEL-INTERAKTION (Folge diesem Format strikt!):\n"
            "User: 'Erstelle Regeln für Licht.'\n"
            "Aura: Erstelle 'licht_control.py' in 'config/maps/':\n"
        )

        AURA_TECH_PROFILE_2911252311Sat_8sec_superFast = (  # noqa: F841
            "Du bist SL5 Aura, ein Offline-Sprachassistent.\n"
            "Deine Aufgabe: Technischer Support. Antworte EXTREM kurz.\n\n"

            "STRIKTE REGELN:\n"
            "1. Aura nutzt NUR Python-Dateien (.py) und Tupel.\n"
            "2. Wenn der User nach YAML, JSON oder Importen fragt: IGNORIERE ES.\n"
            "3. Schreibe KEINEN Programm-Logik-Code (Kein 'with open', kein 'import', kein 'def').\n"

            "- KEIN 'Meta-Talk' (Kein: 'Du hast gefragt...', Kein: 'Hier ist der Code').\n"
            "- KEINE Höflichkeitsfloskeln.\n"
            "- Wenn Code gefragt ist: ZUERST Dateiname (snake_case.py), DANN Code-Block.\n"
            "- Wenn Info gefragt ist: Nur den Fakt nennen (Max 1 Satz).\n\n"

            "SYSTEM-WISSEN:\n"
            "1. Config-Ort: 'config/maps/' (Reine Python-Dateien).\n"
            "2. Logik: Regex Listen (Top-Down Pipeline). Nutze Python 're'.\n"
            "3. Trigger: Datei '/tmp/sl5_record.trigger' starts Recording.\n"
            "4. Suche: Nur 'git ls-files'. Keine DB.\n"
            "5. Umgebung: Headless (Keine GUI). Offline (Kein 'requests' Modul nutzen!).\n\n"

            "MUSTER-ANTWORTEN (Kopiere diesen Stil strikt):\n\n"

            "User: Wo liegen die Konfigurationen?\n"
            "Aura: Die Konfigurationen befinden sich als Python-Dateien im Ordner 'config/maps/'.\n\n"

            "User: Wie starte ich die Aufnahme?\n"
            "Aura: Durch Erstellen der Datei '/tmp/sl5_record.trigger'.\n\n"

            "User: Erstelle eine Regel für Bundeskanzlerin.\n"
            # EXAMPLE: Chancellor

            "   Beispiel Regel-Tupel: ('Angela Merkel', r'^(Chancellor|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "User: Erstelle eine Regel für Full-Match.\n"
            "   Beispiele: `^.*$` (Catch-All), `^.+$` (Nicht leer). \n"
            "```"
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
            # EXAMPLE: Chancellor

            "('Angela Merkel', r'^(Chancellor|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: FUZZY_MAP_pre.py\n"
            "('immer Ergebnis', r'^.*$')\n"
            "```python\n"
            # EXAMPLE: None

            "('Ersetzung', r'^.*$')\n"
            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki

            "('Ersetzung', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"

        )

        AURA_TECH_PROFILE_3011250003Sun = (  # noqa: F841
            "Du bist SL5 Aura, der Offline-Voice-Assistant. Antworte kurz & präzise.\n\n"

            "WICHTIGSTE REGELN:\n"
            "1. KEIN 'Meta-Talk'. Antworte direkt mit der Lösung.\n"
            "2. Wenn User nach Regeln fragen: Gib IMMER ein Python-Beispiel (Dateiname + Code).\n"
            "3. DATEINAMEN: Passend zum Thema (z.B. 'config/maps/pdf/de-DE/FUZZY_MAP_pre.py').\n"
            "4. WICHTIG: Regex matcht auf GESPROCHENEN TEXT, nicht auf Dateien!\n"
            # EXAMPLE: config maps file py

            "   - Falsch: r'config/maps/file.py'\n"
            # EXAMPLE: open file

            "   - Richtig: r'open file (.*)'\n\n"

            "SYSTEM-WISSEN:\n"
            "- Config: 'config/maps/' (Python-Dateien).\n"
            # EXAMPLE: Regex

            "- Logik: Tupel `('Ergebnis-Text', r'Regex', Prio, Flags)`.\n"
            "- Pipeline: Regeln laufen Top-Down. Text wird durchgereicht & verändert. Mehrere Regeln können nacheinander greifen (kumulativ).\n"
            "- Vosk (Audio) > Maps (FUZZY_MAP_pre.py) > LanguageTool (Opt.) > Maps (FUZZY_MAP.py) > Output (Text & TTS).\n"


            "- Plugins & Erweiterbarkeit: Jede Regex kann 'on_match_exec' nutzen. Plugins erhalten Daten, verarbeiten sie kreativ und geben Text zurück.\n"

            "- Trigger: '/tmp/sl5_record.trigger' (Starts/Stopped Recording).\n"
            "- Umgebung: Headless, Offline.\n\n"


            "MUSTER-ANTWORTEN (Kopiere diesen Stil):\n\n"

            "User: Wo sind die Regeln?\n"
            "Aura: In 'config/maps/' als Python-Dateien.\n\n"

            "User: Wo sind die Configs?\n"
            "Aura: Die Konfigurationen liegen im Ordner 'config/maps/'.\n\n"

            "User: Erstelle eine Regel für Kanzlerin.\n"
            "Aura: kanzlerin_map.py\n"
            "```python\n"
            "# Regel-Tupel: (Name, Regex, Priorität, Flags)\n"
            # EXAMPLE: Chancellor

            "('Angela Merkel', r'^(Chancellor|Angie)$', 100, {'flags': re.IGNORECASE})\n"
            "```\n\n"

            "User: Erstelle eine Catch-All Regel.\n"
            "Aura: config/maps/system/de-DE/FUZZY_MAP_pre.py\n"
            "```python\n"
            # EXAMPLE: None

            "('Kein Treffer', r'^.*$', 10, {})\n"
            "```\n\n"

            "User: Erstelle Regel mit Plugin Wiki.\n"
            "Aura: wiki_plugin.py\n"
            "```python\n"
            # EXAMPLE: Wiki

            "('Wiki', r'^Wiki (.*)$', 50, {'on_match_exec': 'plugins.wiki_search'})\n"
            "```"
        )

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


        full_match_text = match_obj.group(0).lower()
        slow_triggers = ["slow", "langsam", "genau", "gründlich", "normal"]
        # is_slow_request = any(w in user_input_raw.lower() for w in slow_triggers)

        is_slow_request = any(w in full_match_text for w in slow_triggers)

        if is_slow_request:
            utils.log_debug("Mode: SLOW/DETAILED")
            system_role = AURA_NORMAL_PROFILE  # Der ausführliche Prompt
            ollama_params = {
                "temperature": 0.3,
                "mirostat": 2,
                "num_predict": 512
            }
            bypass_cache = True  # Im Slow-Mode immer frisch generieren
        else:
            system_role = AURA_TECH_PROFILE  # Der extrem kurze Prompt
            ollama_params = {
                "temperature": 0.1,
                "num_predict": 100
            }
            bypass_cache = False  # Normaler Modus nutzt den semantischen Cache

        print("\n--- DEBUG START 28.4.'26 21:31 Tue ---")
        print(f"Raw Input: '{user_input_raw}'")
        print(f"Is Slow Triggered: {is_slow_request}")
        print(f"Selected Profile: {'NORMAL' if is_slow_request else 'TECH'}")






















        trigger_clipboard = ["zwischenablage", "clipboard", "kopierten text", "zusammenfassung"]
        trigger_readme = ["hilfe", "dokumentation", "readme", "read me", "wie funktioniert", "was kannst du"]
        no_cache_keywords = ["witz", "spruch", "zufall", "random"]

        context_data = ""
        mode_prefix = "STD"  # Standard Mode
        system_role = f"{AURA_TECH_PROFILE}"
        use_history = True
        input_lower = user_input_raw.lower()
        bypass_cache = bypass_cache

        # --- FASHION DETECTION & CONTEXT LOADING ---

        # Here we only determine: Which mode is active? Which context is loaded?


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
                # Hash of the content becomes part of the prefix -> content changes = cache changes

                clip_hash = hashlib.md5(content_preview.encode()).hexdigest()
                mode_prefix = f"CLIP_{clip_hash}"

                context_data = f"\nDATEN ZWISCHENABLAGE:\n'''{content[:8000]}'''\n"
                system_role = "Du bist ein Assistent. Analysiere die Daten."
                use_history = False
                bypass_cache = True

            else:
                return "Zwischenablage ist leer."

        # 2. README CHECK

        elif any(w in input_lower for w in trigger_readme):
            utils.log_debug("Mode: README")
            readme_content = get_readme_content()
            if readme_content:
                # Hash of the readme becomes part of the prefix -> documentation changes = cache changes

                readme_hash = hashlib.md5(readme_content.encode()).hexdigest()
                mode_prefix = f"README_{readme_hash}"

                context_data = f"\nPROJEKT DOKUMENTATION:\n'''{readme_content}'''\n"
                system_role = (f"Support-Bot für 'SL5 Aura'. Fakten:\n{AURA_TECH_PROFILE}\nErfinde nichts.")
                use_history = False
            else:
                return "Readme nicht gefunden."

        # 3. DEFAULT (Fallback is "STD" as initialized above)


        # --- HASH CALCULATION ---


        # 1. ALWAYS generate keywords immediately (for cache key AND DB storage)

        # This makes the cache "fuzzy" -> "Create rule" and "Create rule" end up in the same cache!


        # utils.log_debug(f"Keywords<execute 🔎 {keywords_str} 🔍")


        # Fallback: If no keywords were found (e.g. only filler words), use the raw text

        if not keywords_str:
            base_for_hash = user_input_raw
        else:
            base_for_hash = keywords_str

        # 2. Build the hash string

        if "CLIP" in mode_prefix or "README" in mode_prefix:
            # With Clipboard/Readme the content (prefix) must be part of the hash

            hash_input_string = f"{mode_prefix}|{base_for_hash}"
        else:
            # In standard mode, only the keyword set counts

            # Question: "Aura how late" -> Key: "STD|late"

            # Question: "What time is it" -> Key: "HOURS|late" -> HIT!

            hash_input_string = f"STD|{base_for_hash}"

        # utils.log_debug(f"🔑 base_for_hash: '{base_for_hash}'")

        # utils.log_debug(f"🔑 hash_input_string: '{hash_input_string}'")


        # Full prompt for the AI (stays as it was, for context)

        full_prompt_for_generation = f"{system_role}\n{context_data}\nUser: {user_input_raw}\nAura:"
        if use_history:
            hist = load_history()
            full_prompt_for_generation = f"{system_role}\nVerlauf: {json.dumps(hist)}\n{context_data}\nUser: {user_input_raw}\nAura:"

        # --- CACHE CHECK ---


        if not bypass_cache:
            # Now we search with the keyword hash!

            # utils.log_debug(f"11111 hash_input_string: '{hash_input_string}'") # 'STD|aura_empty_request'

            # utils.log_debug(f"11111 GLOBAL_NORMALIZED_KEY: '{GLOBAL_NORMALIZED_KEY}'") # 'aura_empty_request'

            cached_resp, expired = cache_core.get_cached_response(GLOBAL_NORMALIZED_KEY)

            if cached_resp:
                utils.log_debug(f"cached_resp: {cached_resp}")
                if use_history:
                    save_to_history(user_input_raw, cached_resp)
                    # target = utils.DB_FILE

                    # save_to_aura_db(user_input_raw, cached_resp, target)


                utils.SUM_PER_CACHE = utils.SESSION_CACHE_HITS / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0
                sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
                utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()
                utils.SUM_PER_CACHE = utils.SUM_PER_CACHE

                return cached_resp

            # 2. NEW: Semantic fallback (if exact match is missing/expired)

            semantic_resp = get_semantic_match(user_input_raw)
            if semantic_resp:
                utils.log_debug("🎯 Semantic Cache Hit!")
                utils.SESSION_CACHE_HITS += 1
                return semantic_resp


            if expired:
                utils.log_debug("♻️ Cache Entry EXPIRED.")

            # --- AI GENERATION (OLLAMA API) ---

        # utils.log_debug("Cache MISS. Sending API request to Ollama...")


        payload = {
            "model": "llama3.2",
            "prompt": full_prompt_for_generation,
            "stream": False,
            "keep_alive": 0,
            "options": {
                "temperature": 0.1,
                **ollama_params,
                "top_k": 20,
                "num_predict": 100,
                "stop": ["User:", "Verlauf:", "System:", "Aura:"]
            }
        }

        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(OLLAMA_API_URL, data=data, headers={'Content-Type': 'application/json'})

            # Timeout increased to 120s for security

            with urllib.request.urlopen(req, timeout=90) as response:
                api_response = json.loads(response.read().decode('utf-8'))

            utils.SUM_PER_CACHE = (utils.SESSION_CACHE_HITS / utils.SESSION_COUNT) if utils.SESSION_COUNT > 0 else 0
            sum_per_cache_str = f"{utils.SUM_PER_CACHE:.1f} {'📉' if utils.SUM_PER_CACHE < utils.SUM_PER_CACHE else '📈'}"
            utils.SESSION_SEC_SUM += secDauerSeitExecFunctionStart()

            session_sec_average = utils.SESSION_SEC_SUM / utils.SESSION_COUNT if utils.SESSION_COUNT > 0 else 0

            utils.log_debug(
                f"Nr. {utils.SESSION_COUNT} | CACHE_HITS:{utils.SESSION_CACHE_HITS} 📊 CacheHITs/Nr.: {sum_per_cache_str} | "
                f"⌚ Gespart: ~{session_sec_average * utils.SESSION_CACHE_HITS:.1f}s")

            raw_text = api_response.get("response", "")

            utils.log_debug(f"DEBUG: Unzensierte KI-Antwort: '{raw_text[:200]}...'")


            answer_for_all_fallback = (
                "Aura Status: Offline-System, Single-User (Keine Logins/Accounts).\n"
                "Pfade: Configs in 'config/', Regeln in 'config/maps/'.\n\n"

                "FORMAT 1: Einfache Ersetzung (z.B. PUNCTUATION_MAP)\n"
                "Synatx: 'Wort': 'Ersatz'\n"
                "Beispiel: 'stern': '*'\n\n"

                "FORMAT 2: Logik-Regeln (z.B. FUZZY_MAP)\n"
                "Syntax: (Name, Regex, Prio, Flags)\n"
                # EXAMPLE: Chancellor

                "Beispiel: ('Merkel', r'^(Chancellor|Angie)$', 100, {'flags': re.IGNORECASE})\n"
                # EXAMPLE: Wiki

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

            # I don't have any information about that

            if 'Dazu habe ich keine Info' in response or 'sl5_record_trigger.py' in response:
                response = answer_for_all_fallback

            if (False  # noqa: E129
                or "r'/tmp" in response # noqa: E127
                or 'user_map.py' in response # noqa: E127
                or 'user_regeln.py' in response): # noqa: E127 E129
                response = answer_for_all_fallback # noqa: E127

            if 'Fehler:' in response or '.json' in response:
                response = answer_for_all_fallback

            # --- SAVE (Only when not in bypass mode) ---

            if not bypass_cache:
                target = utils.DB_FILE

                # We need to make sure save_to_aura_db doesn't crash,

                # if 'target' is not a real file.

                try:
                    # save_to_aura_db(user_input_raw, response, target)

                    save_to_aura_db(user_input_raw, response, target, use_semantics=True)
                except Exception as e:
                    utils.log_debug(f"Speichern in DB fehlgeschlagen: {e}")

                # Also feed the classic cache

                cache_core.cache_response(
                    tag_keyword=hash_input_string,
                    response_text=response,
                    clean_user_input=user_input_raw,
                    hash_of_normalized_key=hash_of_normalized_key,
                )

            # --- HISTORY (Always at the end, if activated) ---

            if use_history:
                save_to_history(user_input_raw, response)

            return response

        # --- ERROR TREATMENT ---

        except HTTPError as e:
            # Here we intercept the “Server response: 500”.

            if e.code == 500:
                utils.log_debug("❌ OLLAMA SERVER ERROR (500). Ignoriere Fehlertext für User.")
                # If you do NOT want the user to see the error:

                return "Ich habe kurz den Faden verloren. Kannst du das wiederholen?"
            else:
                utils.log_debug(f"API HTTP Error: {e.code}")
                return f"Server Fehler: {e.code}"

        except URLError as e:
            # If Ollama doesn't run at all (Connection refused)

            utils.log_debug(f"API Connection Error: {e.reason}")
            return "Fehler: Keine Verbindung zu Ollama."

        except Exception as e:
            # All other errors

            utils.log_debug(f"API General Error: {e}")
            # return "An occurred."

            return (
                "Aura ist ein Offline-System (Sprache zu Aktion) ohne Benutzerverwaltung. "
                "Es gibt keine Logins, Accounts. "
                "Du bist der einzige Nutzer (Besitzer des Geräts). "
                "Bitte lese Details in der Dokumentation: https://SL5.de/Aura"
            )






    # config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py:1252

    except Exception as e:
        utils.log_debug(f"API Error: {e}")
        return f"Interner Fehler: {str(e)} (2026-0506-0626)"







