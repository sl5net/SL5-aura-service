# file script/py/func/correct_text_by_languagetool
import requests

# from config.settings import LANGUAGETOOL_BASE_URL

def correct_text_by_languagetool(logger, active_lt_url, LT_LANGUAGE, text: str) -> str:
    # scripts/py/func/correct_text_by_languagetool.py:7
    # LANGUAGETOOL_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
    # LANGUAGETOOL_URL active_lt_url

    log_all_changes = True
    # log_all_changes = False

    if not text.strip(): return text

    if log_all_changes:
        logger.info(f"-----> rawInput to LT:  '{text}'")
    # data = {'language': LT_LANGUAGE, 'text': text, 'maxSuggestions': 1, 'enabledCategories': 'PUNCTUATION,GRAMMAR',
    #         'Categories': 'PUNCTUATION,GRAMMAR'  }
    data = {'language': LT_LANGUAGE, 'text': text, 'maxSuggestions': 1  }
    try:
        # scripts/py/func/correct_text_by_languagetool.py:19
        response = requests.post(active_lt_url, data, timeout=20) # timeout was 10 but Windows OS seems need much more at the moment 18.1.'26 21:28 Sun
        response.raise_for_status()
        matches = response.json().get('matches', [])
        if not matches:
            if log_all_changes:
                logger.info("  <- Output from LT: (No changes)")
            return text
        sorted_matches = sorted(matches, key=lambda m: m['offset'])
        new_text_parts, last_index = [], 0
        for match in sorted_matches:
            new_text_parts.append(text[last_index:match['offset']])
            if match['replacements']:
                new_text_parts.append(match['replacements'][0]['value'])
            else:
                # FIX: Keep original text if there is no replacement
                original_slice = text[match['offset'] : match['offset'] + match['length']]
                new_text_parts.append(original_slice)

            last_index = match['offset'] + match['length']
        new_text_parts.append(text[last_index:])
        corrected_text = "".join(new_text_parts)
        if log_all_changes:
            logger.info(f"🔁 📚{text}📚 ->LT-> 📚{corrected_text}📚")
        return corrected_text
    except requests.exceptions.RequestException as e:
        logger.error(f"  <- ERROR: LanguageTool request failed: {e}")
        return text

