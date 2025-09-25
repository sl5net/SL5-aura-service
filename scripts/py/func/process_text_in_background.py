# scripts/py/func/process_text_in_background.py
import logging
import pkgutil

from pathlib import Path

from config.settings import ENABLE_AUTO_LANGUAGE_DETECTION, ADD_TO_SENCTENCE
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model

from .setup_initial_model import get_model_name_from_key

# Assumes 'models' directory is at the project root, parallel to 'scripts'
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "lid.176.bin"

fasttext_model = None # Ensure variable exists
if ENABLE_AUTO_LANGUAGE_DETECTION:
    if not MODEL_PATH.exists():
        # Using logger that will be passed into the main function later
        # This part of the code needs a logger instance to be available.
        logging.error(f"ERROR: Auto language detection is enabled, but model file is missing: {MODEL_PATH}")
        # Or ideally, log this with a logger instance.
    else:
        import fasttext
        fasttext_model = fasttext.load_model(str(MODEL_PATH))

# from .audio_manager import unmute_microphone

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
    logger.info(f"Starting recursive map loading for language: {lang_code}")

    # Zuerst alle Module im Speicher neu laden, um Änderungen zu erfassen
    auto_reload_modified_maps(logger)

    # Leere Container für die zusammengefügten Daten
    punctuation_map = {}
    fuzzy_map_pre   = []
    fuzzy_map       = []

    try:
        maps_package = importlib.import_module('config.languagetool_server.maps')
    except ModuleNotFoundError:
        maps_package = importlib.import_module('config.maps')

    for importer, modname, ispkg in pkgutil.walk_packages(
            path=maps_package.__path__,
            prefix=maps_package.__name__ + '.',
            onerror=lambda x: None):

        if ispkg:
            continue

        if f".{lang_code}." not in modname:
            continue

        # not use not needed plugins
        if ".plugins." in modname:
            plugin_name = modname.split('.plugins.')[1].split('.')[0]
            if not settings.PLUGINS_ENABLED.get(plugin_name, True):
                continue


        try:
            module = importlib.import_module(modname)
            logger.debug(f"Processing module for aggregation: {modname}")

            # Füge Daten hinzu, falls die Variablen existieren
            if hasattr(module, 'PUNCTUATION_MAP'):
                punctuation_map.update(module.PUNCTUATION_MAP)
            if hasattr(module, 'FUZZY_MAP_pre'):
                fuzzy_map_pre.extend(module.FUZZY_MAP_pre)
            if hasattr(module, 'FUZZY_MAP'):
                fuzzy_map.extend(module.FUZZY_MAP)

        except Exception as e:
            logger.error(f"Failed to process module '{modname}': {e}")

    logger.info(f"Map loading complete. Found {len(fuzzy_map_pre)} FUZZY_MAP_pre rules.")
    return punctuation_map, fuzzy_map_pre, fuzzy_map



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

        logger.info(f"start sanitize_transcription_start")
        raw_text = sanitize_transcription_start(raw_text)
        logger.info(f"end sanitize_transcription_start")


        # ZWNBSP
        logger.info(f"THREAD: Starting processing for: '{raw_text}'")

        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")


        lang_code_predictions = ''

        if len(raw_text) > 0:
            try:
                if LT_LANGUAGE == 'en-US':
                    threshold = 0.50  # Low threshold: switch even if not 100% sure it's German
                else:
                    threshold=0.60
                predictions = None
                if ENABLE_AUTO_LANGUAGE_DETECTION:
                    logger.info(f"👀👀👀 Start lang_code predictions for: '{raw_text}'")
                    predictions = fasttext_model.predict(raw_text, threshold=threshold)

                if predictions:
                    logger.info(
                        f"---------------------------> predictions: {predictions} , LT_LANGUAGE: {LT_LANGUAGE}")
                    if predictions[0] and predictions[0][0]:
                        lang_code_predictions = predictions[0][0].replace('__label__', '')
                        # logger.info(f"Raw prediction object: {predictions}")

                        logger.info(f"👀👀👀 lang_code predictions of '{raw_text}': {lang_code_predictions} 👀")

                        # get something like language_code = "en-US":
                        lang_code_predictions = guess_lt_language_from_model(logger, lang_code_predictions)

                        # if predictions and predictions[0]:
                        if LT_LANGUAGE != lang_code_predictions:
                            logger.info(f'❌❌❌  {lang_code_predictions} != {LT_LANGUAGE} old +++++++++++++++++++++')
                            logger.info(f'❌❌❌  {lang_code_predictions} != {LT_LANGUAGE} old +++++++++++++++++++++')
                            logger.info(f'❌❌❌  {lang_code_predictions} != {LT_LANGUAGE} old +++++++++++++++++++++')
                            logger.info(f'❌❌❌  {lang_code_predictions} != {LT_LANGUAGE} old +++++++++++++++++++++')

                            LT_LANGUAGE = lang_code_predictions

                            # get something like 'en-US': 'vosk-model-en-us-0.22':
                            model_name = get_model_name_from_key(lang_code_predictions)

                            (PROJECT_ROOT / "config" / "model_name.txt").write_text(model_name)
                            # load_maps_for_language(lang_code_predictions, logger)

            except Exception as e:
                logger.info(f"❌❌❌ An exception in lang_code predictions  {e} lang_code: {lang_code_predictions} , LT_LANGUAGE: {LT_LANGUAGE}")
                logger.info(f"❌❌❌ An exception in lang_code predictions  {e} lang_code: {lang_code_predictions} , LT_LANGUAGE: {LT_LANGUAGE}")
                logger.info(f"❌❌❌ An exception in lang_code predictions  {e} lang_code: {lang_code_predictions} , LT_LANGUAGE: {LT_LANGUAGE}")
                # lang_code_predictions = 'de'
                exit(1)

        # scripts/py/func/process_text_in_background.py
        normalize_punctuation_changed_size = False
        is_only_number = False
        processed_text, was_exact_match = normalize_punctuation(raw_text, punctuation_map)
        if len(processed_text) != len(raw_text):
            normalize_punctuation_changed_size = True

        if normalize_punctuation_changed_size:
            processed_text = re.sub(r'(?<=\d)\s+(?=\d)', '', processed_text)

            is_only_number =  processed_text.isdigit()

        # scripts/py/func/process_text_in_background.py

        #regex_pre_is_replacing_all = False
        regex_match_found_prev = False
        regex_pre_is_replacing_all_maybe = False

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

            regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe and regex_match_found_prev

            logger.info(f"LT_LANGUAGE = {LT_LANGUAGE}") #
            if regex_pre_is_replacing_all:
                if processed_text == 'english please' and LT_LANGUAGE == 'de-DE':
                    processed_text = 'Ok, lets write in english now.'
                    LT_LANGUAGE =  'en-US' # 'de-DE'
                    model_name = get_model_name_from_key(LT_LANGUAGE)
                    (PROJECT_ROOT / "config" / "model_name.txt").write_text(model_name)
                    # load_maps_for_language(LT_LANGUAGE, logger)

                elif processed_text == 'Deutsch bitte':
                    processed_text = 'Klar, jetzt Deutsch.'
                    LT_LANGUAGE =  'de-DE' # 'en-US' # 'de-DE'
                    model_name = get_model_name_from_key(LT_LANGUAGE)
                    (PROJECT_ROOT / "config" / "model_name.txt").write_text(model_name)
                    # load_maps_for_language(LT_LANGUAGE, logger)
                    # Switched to English mill ﻿ Deutsche Putin the

            if (not regex_pre_is_replacing_all
                and not is_only_number
                and not (
                            settings.CORRECTIONS_ENABLED["git"]
                            and ("git" in processed_text or "push" in processed_text))):
                processed_text = correct_text_by_languagetool(
                    logger,
                    active_lt_url,
                    LT_LANGUAGE,
                    processed_text).lstrip('\uFEFF')

            # Step 2: Slower, fuzzy replacements on the result
            # logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

            best_score = 0
            best_replacement = None

            # 80:scripts/py/func/process_text_in_background.py

            # --- NEW HYBRID MATCHING LOGIC ---

            # Pass 1: Prioritize and check for exact REGEX matches first.
            # A regex match is considered definitive and will stop further processing.
            regex_match_found = False

            if not regex_pre_is_replacing_all and not is_only_number:
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
            if (not regex_pre_is_replacing_all
                    and not regex_match_found
                    and not is_only_number):
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
            if ADD_TO_SENCTENCE:
                if len(processed_text)> 70 and re.match(r"\w\s*$", processed_text):
                    processed_text +=  ADD_TO_SENCTENCE
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
        unique_output_file.write_text(processed_text, encoding="utf-8") # BOM -sig is outdated and not needed anymore
        # unique_output_file.write_text(processed_text, encoding="utf-8-sig") # BOM -sig is outdated and not needed anymore
        logger.info(f"✅ THREAD: Successfully wrote to {unique_output_file}")
        #
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
# Hallo des Hallo Test

def sanitize_transcription_start(raw_text: str) -> str:
    """
    cost: ~ 1 Microsecond (µs)


    Removes leading junk characters from a string, preserving any language.

    It iterates through the string to find the first alphanumeric character
    (respecting Unicode, so it works for Cyrillic, CJK, etc.) and returns
    the substring from that point onward. Also cleans BOM and ZWSP.
    """
    #logging.info(f"Sanitizing raw text: '{raw_text[:50]}...'")

    start_index = -1
    for i, char in enumerate(raw_text):
        # isalnum() is Unicode-aware and checks for letters or numbers
        if char.isalnum():
            start_index = i
            #logging.info(f"Found first valid character '{char}' at index {i}.")
            break

    #if start_index == -1:
        #logging.info("No alphanumeric characters found. Returning empty string.")
    #    return raw_text  # Or return raw_text if that's preferred

    # Slice from the first valid character and then perform other cleanup
    clean_text = raw_text[start_index:]
    clean_text = clean_text.lstrip('\uFEFF')
    clean_text = clean_text.replace('\u200b', '').strip()

    #logging.info(f"Returning sanitized text: '{clean_text[:50]}...'")
    return clean_text