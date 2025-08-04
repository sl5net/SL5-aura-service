# scripts/py/func/process_text_in_background.py
import os, sys
"""
doc:
how test language tool in command line:
curl --data "language=de-DE&text=das stimmt unsere ist nicht absolut fehlerfrei" http://localhost:8081/v2/check
"""

# from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW
from config import settings
from .normalize_punctuation import normalize_punctuation
from .map_reloader import auto_reload_modified_maps

import importlib

def load_maps_for_language(lang_code, logger):
    """Dynamically loads punctuation and fuzzy maps for a given language code (e.g., 'de')."""
    # try:

    logger.info(f"lang_code: {lang_code}")
    logger.info(f"lang_code: {lang_code}")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # e.g. 'maps.de.punctuation_map'
    punc_module_path      = f"config.languagetool_server.maps.{lang_code}.PUNCTUATION_MAP"
    fuzzy_module_path_pre = f"config.languagetool_server.maps.{lang_code}.FUZZY_MAP_pre"
    fuzzy_module_path     = f"config.languagetool_server.maps.{lang_code}.FUZZY_MAP"

    punc_module = importlib.import_module(punc_module_path)
    fuzzy_module_pre = importlib.import_module(fuzzy_module_path_pre)
    fuzzy_module     = importlib.import_module(fuzzy_module_path)

    logger.info(f"💾 Fuzzy_pre: {fuzzy_module_path_pre}")
    logger.info(f"💾 Fuzzy: {fuzzy_module_path}")

    punctuation_map = punc_module.PUNCTUATION_MAP
    fuzzy_map_pre   = fuzzy_module_pre.FUZZY_MAP_pre
    fuzzy_map       = fuzzy_module.FUZZY_MAP


    # log.info(f"Successfully loaded command maps for language '{lang_code}'.")
    return punctuation_map, fuzzy_map_pre, fuzzy_map
"""
    except (ModuleNotFoundError, AttributeError) as e:
        # log.warning(f"Could not load maps for '{lang_code}': {e}. Using empty maps.")
        return {}, [] # Fallback empty maps
"""

from .correct_text_by_languagetool import correct_text_by_languagetool
import re, time
from thefuzz import fuzz
from .notify import notify


# Helper to check if a string contains regex special characters
def is_regex_pattern(pattern):
    # This is a simple heuristic. You can add more characters if needed.
    return any(char in pattern for char in r'^$*+?{}[]\|()")')

def process_text_in_background(logger,
                               LT_LANGUAGE,
                               raw_text,
                               TMP_DIR,
                               recording_time,
                               active_lt_url,
                              output_dir_override = None):
    punctuation_map, fuzzy_map_pre, fuzzy_map = load_maps_for_language(LT_LANGUAGE, logger)
    try:
        raw_text = raw_text.lstrip('\uFEFF') # removes ZWNBSP/BOM at beginning
        logger.info(f"THREAD: Starting processing for: '{raw_text}'")

        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")

        # lang_code = "DODO dummy"
        # scripts/py/func/process_text_in_background.py
        # fuzzy_map_poker_dc = 'config' / 'plugins' / 'poker' / 'dealers_choice.py'
        #if settings.CORRECTIONS_ENABLED["poker_hotkeys"]:
        #    map_path = fuzzy_map_poker_dc
        #    processed_text, was_exact_match = normalize_punctuation(raw_text, map_path)


        # scripts/py/func/process_text_in_background.py
        normalize_punctuation_changed_size = False
        processed_text, was_exact_match = normalize_punctuation(raw_text, punctuation_map)
        if len(processed_text) != len(raw_text):
            normalize_punctuation_changed_size = True

        if normalize_punctuation_changed_size:
            # Entfernt Leerzeichen nur, wenn sie zwischen zwei Ziffern stehen
            processed_text = re.sub(r'(?<=\d)\s+(?=\d)', '', processed_text)

        regex_match_found_prev = False
        regex_pre_is_replacing_all = False

        if not was_exact_match:
            for replacement, match_phrase, threshold, *flags_list in fuzzy_map_pre:
                flags = flags_list[0] if flags_list else 0 # Default: 0 (case-sensitive)

                if is_regex_pattern(match_phrase):
                    logger.debug(f" '👀pre -->{match_phrase}<-- 👀")

                regex_pre_is_replacing_all_maybe = match_phrase.startswith('^') and match_phrase.endswith('$')

                try:
                    if re.search(match_phrase, processed_text, flags=flags):
                        logger.info(f"🔁Regex_pre in: '{processed_text}' --> '{replacement}' based on pattern '{match_phrase}'")

                        new_text = re.sub(
                            match_phrase,
                            replacement.strip(),
                            processed_text,
                            flags=flags
                        )

                        if new_text != processed_text:
                            logger.info(
                                f"🚀Regex_pre: '{processed_text}' -> '{new_text}' (Pattern: '{match_phrase}')")
                            processed_text = new_text

                        regex_match_found_prev = True

                        break  # Found a definitive match, stop this loop

                except re.error as e:
                    logger.warning(f"Invalid regex_pre pattern in FUZZY_MAP_pre: '{match_phrase}'. Error: {e}")
                    continue # Skip this invalid rule

                if regex_pre_is_replacing_all:
                    logger.info('lkjöasldkfjsödl')
                    exit(1)

            regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe and regex_match_found_prev

            if (not regex_pre_is_replacing_all
                and not (
                            settings.CORRECTIONS_ENABLED["git"] and
                            ("git" in processed_text or "push" in processed_text))):
                processed_text = correct_text_by_languagetool(
                    logger,
                    active_lt_url,
                    LT_LANGUAGE,
                    processed_text).lstrip('\uFEFF')

#  1 2 3 4 5
                # Step 2: Slower, fuzzy replacements on the result
            # logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

            best_score = 0
            best_replacement = None

            # 80:scripts/py/func/process_text_in_background.py

            # --- NEW HYBRID MATCHING LOGIC ---

            # Pass 1: Prioritize and check for exact REGEX matches first.
            # A regex match is considered definitive and will stop further processing.
            regex_match_found = False

            if regex_pre_is_replacing_all == False:
                for replacement, match_phrase, threshold, *flags_list in fuzzy_map:
                    flags = flags_list[0] if flags_list else 0 # Default: 0 (case-sensitive)


                    if is_regex_pattern(match_phrase):
                        logger.debug(f" '👀 -->{match_phrase}<-- 👀")

                        try:
                            if re.search(match_phrase, processed_text, flags=flags):
                                logger.info(f"🔁Regex in: '{processed_text}' --> '{replacement}' based on pattern '{match_phrase}'")

                                new_text = re.sub(
                                    match_phrase,
                                    replacement.strip(),
                                    processed_text,
                                    flags=flags
                                )

                                if new_text != processed_text:
                                    logger.info(
                                        f"Regex match: '{processed_text}' -> '{new_text}' (Pattern: '{match_phrase}')")
                                    processed_text = new_text

                                regex_match_found = True
                                break  # Found a definitive match, stop this loop

                        except re.error as e:
                            logger.warning(f"Invalid regex pattern in FUZZY_MAP: '{match_phrase}'. Error: {e}")
                            continue # Skip this invalid rule

            # Pass 2: If no regex matched, perform the FUZZY search as before.
            # This code will only run if the loop above didn't find a regex match.
            if not regex_pre_is_replacing_all and not regex_match_found:
                logger.info(f"No regex match. Proceeding to fuzzy search for: '{processed_text}'")
                best_score = 0
                best_replacement = None

                # for replacement, match_phrase, threshold in fuzzy_map:
                for replacement, match_phrase, threshold, *_ in fuzzy_map:
                    # Skip regex patterns in this pass
                    if is_regex_pattern(match_phrase):
                        continue

                    score = fuzz.token_set_ratio(processed_text.lower(), match_phrase.lower())
                    if score >= threshold and score > best_score:
                        best_score = score
                        best_replacement = replacement

                if best_replacement:
                    logger.info(f"🎊{best_score}% Fuzzy found: Replacing '{processed_text}' with '{best_replacement}'")
                    processed_text = best_replacement.strip()
                else:
                    logger.info(f"👎best fuzzy score:{best_score}% for '{processed_text}'")




        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
        recording_time = time.time()

        # file: scripts/py/func/process_text_in_background.py
        # ... watchDir := "C:\tmp\sl5_dictation"
        timestamp = int(time.time() * 1000)

        if output_dir_override:
            # unique_output_file = f"{output_dir_override}/tts_output_{timestamp}.txt"
            unique_output_file = output_dir_override / f"tts_output_{timestamp}.txt"
        else:
            unique_output_file = TMP_DIR / f"sl5_dictation/tts_output_{timestamp}.txt"

        # unique_output_file = TMP_DIR / f"sl5_dictation/tts_output_{timestamp}.txt"
        # unique_output_file.write_text(processed_text)
        unique_output_file.write_text(processed_text, encoding="utf-8-sig")
        logger.info(f"✅ THREAD: Successfully wrote to {unique_output_file}")

        # notify("Transcribed", duration=700, urgency="low")

        notify("Transcribed", "", "low", duration=1000, replace_tag="transcription_status")


    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        notify(f"FATAL: Error in processing thread", duration=4000, urgency="low")
    finally:
        # file: scripts/py/func/process_text_in_background.py
        logger.info(f"✅ Background processing for '{raw_text[:20]}...' finished. ")
        notify(f" Background processing for '{raw_text[:20]}...' finished. ", duration=700, urgency="low")

        auto_reload_modified_maps(logger)
