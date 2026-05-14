# scripts/py/func/correct_text_by_languagetool.py:1

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# scripts/py/func/correct_text_by_languagetool.py:6
# _lt_session = None
_session_cache = {}
get_lt_session = None
# lt_session = requests.Session()


# scripts/py/func/correct_text_by_languagetool.py

import sqlite3
import hashlib
import json
# from typing import Optional

DB_PATH = "data/_languagetool_cache.db"
# scripts/py/func/correct_text_by_languagetool.py:22
def get_db_conn(path: str = DB_PATH) -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(path, timeout=30, isolation_level=None)  # autocommit off if you call begin
    except sqlite3.OperationalError as e:
        import os
        print(f"DEBUG: path: {path}")
        print(f"DEBUG: UID: {os.getlogin()} (UID: {os.getuid()})")
        print(f"DEBUG: access: {os.access(os.path.dirname(path), os.W_OK)}")
        raise e

    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn

def make_key(server_url: str, language: str, text: str) -> str:
    h = hashlib.sha256()
    # deterministic canonicalization
    h.update(server_url.encode("utf-8"))
    h.update(b"|")
    h.update(language.encode("utf-8"))
    h.update(b"|")
    h.update(text.encode("utf-8"))
    return h.hexdigest()

def ensure_schema(conn: sqlite3.Connection) -> None:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS lt_cache (
        key TEXT PRIMARY KEY,
        server_url TEXT NOT NULL,
        language TEXT NOT NULL,
        input_text TEXT NOT NULL,
        corrected_text TEXT NOT NULL,
        lt_response_json TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lt_cache_server_lang ON lt_cache(server_url, language)")


def corrected_from_matches(text: str, matches: list) -> str:
    # same merge logic as your current code, but as a helper so we can reconstruct from cached JSON
    if not matches:
        return text
    sorted_matches = sorted(matches, key=lambda m: m['offset'])
    new_text_parts = []
    last_index = 0
    for match in sorted_matches:
        if not match.get('replacements'):
            continue
        if match['offset'] < last_index:  # prevent overlapping
            continue
        new_text_parts.append(text[last_index:match['offset']])
        new_text_parts.append(match['replacements'][0]['value'])
        last_index = match['offset'] + match['length']
    new_text_parts.append(text[last_index:])
    return "".join(new_text_parts)


# def get_session():
#     # We store one session per process ID (PID)
#     pid = os.getpid()
#     if pid not in _session_cache:
#         session = requests.Session()
#         retries = Retry(total=2, backoff_factor=0.1)
#         adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retries)
#         session.mount('http://', adapter)
#         _session_cache[pid] = session
#     return _session_cache[pid]


def correct_text_by_languagetool(logger, active_lt_url, LT_LANGUAGE, text: str) -> str:
    if not text or not text.strip():
        return text

    base_url = active_lt_url.rstrip('/')
    if base_url.endswith('/v2'):
        check_url = f"{base_url}/check"
    elif not base_url.endswith('/v2/check'):
        check_url = f"{base_url}/v2/check"
    else:
        check_url = base_url

    conn = get_db_conn()
    ensure_schema(conn)

    key = make_key(check_url, LT_LANGUAGE, text)

    # Try cache lookup
    cur = conn.execute("SELECT corrected_text, lt_response_json FROM lt_cache WHERE key = ?", (key,))
    row = cur.fetchone()
    if row:
        corrected_text, lt_json = row
        logger.debug("LT cache hit (key=%s).", key)
        # Optional: could validate JSON / re-run correction_from_matches if you want to update correction logic
        return corrected_text

    # Cache miss -> call LT
    session = requests.Session()  # or use your get_session()
    data = {'language': LT_LANGUAGE, 'text': text, 'maxSuggestions': 1}
    try:
        response = session.post(check_url, data=data, timeout=8)
        response.raise_for_status()
        resp_json = response.json()
        matches = resp_json.get('matches', [])

        corrected = corrected_from_matches(text, matches)

        # Persist to DB
        lt_json_text = json.dumps(resp_json, ensure_ascii=False)
        # Use a transaction to write
        with conn:  # sqlite3 Connection supports context manager -> BEGIN/COMMIT
            conn.execute(
                "INSERT OR REPLACE INTO lt_cache (key, server_url, language, input_text, corrected_text, lt_response_json) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (key, check_url, LT_LANGUAGE, text, corrected, lt_json_text)
            )

        logger.debug("LT request cached (key=%s, matches=%d).", key, len(matches))
        return corrected

    except requests.exceptions.Timeout:
        logger.error("TIMEOUT: LT-Server zu langsam.")
        return text
    except requests.exceptions.RequestException as e:
        logger.error("LanguageTool request failed: %s", e)
        return text
    finally:
        conn.close()




















# Optimization for 16-Core CPU:
# Increase pool_connections and pool_maxsize to 20 or more
retries = Retry(total=2, backoff_factor=0.1)
adapter = HTTPAdapter(
    pool_connections=25,
    pool_maxsize=25,
    max_retries=retries
)
# lt_session.mount('http://', adapter)
# lt_session.mount('https://', adapter)



# retries = Retry(total=2, backoff_factor=0.1)
# lt_session.mount('http://', HTTPAdapter(max_retries=retries))


def correct_text_by_languagetool_202601311818(logger, active_lt_url, LT_LANGUAGE, text: str) -> str:
    if not text or not text.strip():
        return text

    log_all_changes = True

    # 1. Daten-Payload optimieren
    # Tip: Disable picky rules or restrict categories
    data = {
        'language': LT_LANGUAGE,
        'text': text,
        'maxSuggestions': 1,
        # 'enabledCategories': 'PUNCTUATION,GRAMMAR', # Nur das Nötigste
        # 'disabledRules': 'WHITESPACE_RULE', # Beispiel für langsame Regeln
        'level': 'default'  # 'picky' wäre deutlich langsamer
    }

    try:
        # 2. Timeout senken (z.B. 5 Sekunden)
        # If the local server takes longer, it is overloaded
        lt_session = get_lt_session()
        response = lt_session.post(active_lt_url, data=data, timeout=5)
        response.raise_for_status()

        matches = response.json().get('matches', [])
        if not matches:
            return text

        # Correction logic (unchanged, but more efficient)
        sorted_matches = sorted(matches, key=lambda m: m['offset'])
        new_text_parts, last_index = [], 0

        for match in sorted_matches:
            # Skip correction if there are no replacements
            if not match.get('replacements'):
                continue

            new_text_parts.append(text[last_index:match['offset']])
            new_text_parts.append(match['replacements'][0]['value'])
            last_index = match['offset'] + match['length']

        new_text_parts.append(text[last_index:])
        corrected_text = "".join(new_text_parts)

        if log_all_changes:
            logger.info("🔁 LT-Korrektur durchgeführt.")
        return corrected_text

    except requests.exceptions.Timeout:
        logger.error("  <- TIMEOUT: LT Server war zu langsam.")
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"  <- ERROR: LanguageTool request failed: {e}")
        return text