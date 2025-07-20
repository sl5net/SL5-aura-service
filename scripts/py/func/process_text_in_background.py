# file: scripts/py/func/process_text_in_background.py
import os
import sys
"""
doc:
how test language tool in command line:
curl --data "language=de-DE&text=das stimmt unsere ist nicht absolut fehlerfrei" http://localhost:8081/v2/check
"""

# from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW
from config import settings
from .normalize_punctuation import normalize_punctuation

import importlib

def load_maps_for_language(lang_code):
    """Dynamically loads punctuation and fuzzy maps for a given language code (e.g., 'de')."""
    # try:

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # e.g. 'maps.de.punctuation_map'
    punc_module_path = f"config.languagetool_server.maps.{lang_code}.PUNCTUATION_MAP"
    fuzzy_module_path = f"config.languagetool_server.maps.{lang_code}.FUZZY_MAP"

    punc_module = importlib.import_module(punc_module_path)
    fuzzy_module = importlib.import_module(fuzzy_module_path)

    punctuation_map = punc_module.PUNCTUATION_MAP
    fuzzy_map = fuzzy_module.FUZZY_MAP

    # log.info(f"Successfully loaded command maps for language '{lang_code}'.")
    return punctuation_map, fuzzy_map
"""
    except (ModuleNotFoundError, AttributeError) as e:
        # log.warning(f"Could not load maps for '{lang_code}': {e}. Using empty maps.")
        return {}, [] # Fallback empty maps
"""

from .correct_text import correct_text
import re, time
from thefuzz import fuzz
from .notify import notify

def process_text_in_background(logger,
                               LT_LANGUAGE,
                               raw_text,
                               TMP_DIR,
                               recording_time,
                               active_lt_url):
    punctuation_map, fuzzy_map = load_maps_for_language(LT_LANGUAGE)
    try:
        logger.info(f"THREAD: Starting processing for: '{raw_text}'")

        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")

        processed_text = normalize_punctuation(raw_text, punctuation_map)

        if not settings.CORRECTIONS_ENABLED["git"] or "git" not in processed_text and "push" not in processed_text:
            processed_text = correct_text(logger, active_lt_url, LT_LANGUAGE, processed_text)


        # Step 2: Slower, fuzzy replacements on the result
        # logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

        best_score = 0
        best_replacement = None

        for replacement, match_phrase, threshold in fuzzy_map:
            score = fuzz.token_set_ratio(processed_text.lower(), match_phrase.lower())

            if score >= threshold and score > best_score:
                best_score = score
                best_replacement = replacement

        if best_replacement:
            logger.info(f"Fuzzy match found: Replacing '{processed_text}' with '{best_replacement}' (Score: {best_score})")
            processed_text = best_replacement
        else:
            logger.info(f"No fuzzy match found for '{processed_text}'")

        # --- ENDE DER KORRIGIERTEN LOGIK ---



        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
        recording_time = time.time()

        # file: scripts/py/func/process_text_in_background.py
        # ... watchDir := "C:\tmp\sl5_dictation"
        timestamp = int(time.time() * 1000)
        unique_output_file = TMP_DIR / f"sl5_dictation/tts_output_{timestamp}.txt"
        unique_output_file.write_text(processed_text)
        logger.info(f"THREAD: Successfully wrote to {unique_output_file}")

        # notify("Transcribed", duration=700, urgency="low")

        notify("Transcribed", "", "low", duration=1000, replace_tag="transcription_status")


    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        notify(f"FATAL: Error in processing thread", duration=4000, urgency="low")
    finally:
        # file: scripts/py/func/process_text_in_background.py
        # ...
        logger.info(f" Background processing for '{raw_text[:20]}...' finished. ")
        notify(f" Background processing for '{raw_text[:20]}...' finished. ", duration=700, urgency="low")

