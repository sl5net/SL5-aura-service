# scripts/py/func/correct_text_by_languagetool.py:1
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# scripts/py/func/correct_text_by_languagetool.py:6
lt_session = requests.Session()


retries = Retry(total=2, backoff_factor=0.1)
lt_session.mount('http://', HTTPAdapter(max_retries=retries))


def correct_text_by_languagetool(logger, active_lt_url, LT_LANGUAGE, text: str) -> str:
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