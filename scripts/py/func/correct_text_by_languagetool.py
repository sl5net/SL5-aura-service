# scripts/py/func/correct_text_by_languagetool.py:1
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os # Zum Erkennen des Prozesses


# scripts/py/func/correct_text_by_languagetool.py:6
# _lt_session = None
_session_cache = {}
get_lt_session = None
# lt_session = requests.Session()


# scripts/py/func/correct_text_by_languagetool.py


def get_session():
    # Wir speichern eine Session pro Prozess-ID (PID)
    pid = os.getpid()
    if pid not in _session_cache:
        session = requests.Session()
        retries = Retry(total=2, backoff_factor=0.1)
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retries)
        session.mount('http://', adapter)
        _session_cache[pid] = session
    return _session_cache[pid]


def correct_text_by_languagetool(logger, active_lt_url, LT_LANGUAGE, text: str) -> str:
    if not text or not text.strip(): return text

    # Hole die für diesen Prozess gültige Session
    session = get_session()

    data = {'language': LT_LANGUAGE, 'text': text, 'maxSuggestions': 1}
    try:
        # Timeout leicht erhöhen für hohe Last
        response = session.post(active_lt_url, data=data, timeout=8)
        response.raise_for_status()

        matches = response.json().get('matches', [])
        if not matches:
            return text

        # Korrektur-Logik (unverändert, aber effizienter)
        sorted_matches = sorted(matches, key=lambda m: m['offset'])
        new_text_parts, last_index = [], 0

        for match in sorted_matches:
            # Überspringe Korrektur, wenn keine Replacements vorhanden sind
            if not match.get('replacements'):
                continue

            new_text_parts.append(text[last_index:match['offset']])
            new_text_parts.append(match['replacements'][0]['value'])
            last_index = match['offset'] + match['length']

        new_text_parts.append(text[last_index:])
        corrected_text = "".join(new_text_parts)

        return corrected_text

    except requests.exceptions.Timeout:
        logger.error(f"  <- TIMEOUT: LT Server war zu langsam.")
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"  <- ERROR: LanguageTool request failed: {e}")
        return text




















def get_lt_session_202601311817():
    global _lt_session
    if _lt_session is None:
        # Diese Initialisierung findet jetzt erst im Subprozess statt
        _lt_session = requests.Session()
        retries = Retry(total=2, backoff_factor=0.1)
        adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retries)
        _lt_session.mount('http://', adapter)
        _lt_session.mount('https://', adapter)

    return _lt_session


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
    # Tipp: Deaktivieren Sie "picky" Regeln oder schränken Sie Kategorien ein
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
        # Wenn der lokale Server länger braucht, ist er überlastet
        lt_session = get_lt_session()
        response = lt_session.post(active_lt_url, data=data, timeout=5)
        response.raise_for_status()

        matches = response.json().get('matches', [])
        if not matches:
            return text

        # Korrektur-Logik (unverändert, aber effizienter)
        sorted_matches = sorted(matches, key=lambda m: m['offset'])
        new_text_parts, last_index = [], 0

        for match in sorted_matches:
            # Überspringe Korrektur, wenn keine Replacements vorhanden sind
            if not match.get('replacements'):
                continue

            new_text_parts.append(text[last_index:match['offset']])
            new_text_parts.append(match['replacements'][0]['value'])
            last_index = match['offset'] + match['length']

        new_text_parts.append(text[last_index:])
        corrected_text = "".join(new_text_parts)

        if log_all_changes:
            logger.info(f"🔁 LT-Korrektur durchgeführt.")
        return corrected_text

    except requests.exceptions.Timeout:
        logger.error(f"  <- TIMEOUT: LT Server war zu langsam.")
        return text
    except requests.exceptions.RequestException as e:
        logger.error(f"  <- ERROR: LanguageTool request failed: {e}")
        return text