# scripts/py/func/process_text_in_background.py
import difflib
import logging
import os
import pkgutil
import sys

import importlib.util
from pathlib import Path

import psutil

from .audio_manager import speak_fallback
from .log_memory_details import log4DEV


# This is your function at line 17
def load_module_from_path(script_path):
    path = Path(script_path)
    spec = importlib.util.spec_from_file_location(path.stem, path)

    # <<< FIX 1: Add this check right here
    if spec is None:
        # Log this error to know which script failed
        logging.error(f"Could not create module spec for path: {script_path}")
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# from config.settings import ENABLE_AUTO_LANGUAGE_DETECTION, ADD_TO_SENCTENCE

from config.dynamic_settings import settings

from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model

from .setup_initial_model import get_model_name_from_key

# Assumes 'models' directory is at the project root, parallel to 'scripts'
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "lid.176.bin"



fasttext_model = None # Ensure variable exists
if settings.ENABLE_AUTO_LANGUAGE_DETECTION:
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
from config.dynamic_settings import settings
from .normalize_punctuation import normalize_punctuation
from .map_reloader import auto_reload_modified_maps

import importlib


def is_plugin_enabled(hierarchical_key, plugins_config):
    """

    Prüft, ob ein Plugin aktiviert ist. Ein Plugin ist DEAKTIVIERT,
    wenn es selbst oder irgendein übergeordnetes Modul in der Hierarchie
    explizit auf `False` gesetzt ist. In allen anderen Fällen ist es AKTIVIERT.
    """
    current_key_parts = hierarchical_key.split('/')

    # Wir bauen die Hierarchie von oben nach unten auf und prüfen jeden Schritt
    # z.B. für "game/0ad" prüfen wir erst "game", dann "game/0ad"
    for i in range(len(current_key_parts)):
        # Baue den aktuellen Key zusammen, z.B. erst 'game', dann 'game/0ad'
        current_key = "/".join(current_key_parts[:i + 1])

        # Prüfe, ob dieser Key EXPLIZIT auf False gesetzt ist.
        # .get(key, True) gibt True zurück, wenn der Key nicht existiert.
        # Das entspricht deiner Regel "Kein Eintrag = True".
        if plugins_config.get(current_key) is False:
            # Sobald wir ein 'False' in der Kette finden, ist die Entscheidung gefallen.
            return False

    # Wenn wir die gesamte Hierarchie durchlaufen haben und kein einziges
    # 'False' gefunden haben, ist das Modul aktiviert.
    return True


def load_maps_for_language(lang_code, logger):
    # scripts/py/func/process_text_in_background.py:50
    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"def load_maps_for_language", logger)

    logger.info(f"🗺️Starting recursive map loading for language: {lang_code}")

    settings.reload_settings()

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"next: auto_reload_modified_maps", logger)

    # Zuerst alle Module im Speicher neu laden, um Änderungen zu erfassen
    auto_reload_modified_maps(logger)

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"last: auto_reload_modified_maps", logger)

    # Leere Container für die zusammengefügten Daten
    punctuation_map = {}
    fuzzy_map_pre   = []
    fuzzy_map       = []

    try:
        maps_package = importlib.import_module('config.languagetool_server.maps')
    except ModuleNotFoundError:
        maps_package = importlib.import_module('config.maps')

    plugin_name_before = ''
    plugin_name = ''
    for importer, modname, ispkg in pkgutil.walk_packages(
            path=maps_package.__path__,
            prefix=maps_package.__name__ + '.',
            onerror=lambda x: None):

        logger.debug(f"📚Found module candidate: {modname}")

        if ispkg:
            continue

        if f".{lang_code}." not in modname:
            continue

        log_all_map_ENABLED = True and settings.DEV_MODE

        if ".plugins." in modname:
            if len(parts := modname.split('.plugins.', 1)[1].split('.')) < 2:
                logger.warning(f"Could not determine plugin_name from modname: {modname}. Skipping.")
                continue

            plugin_name_before, plugin_name = plugin_name, parts[-3]
            hierarchical_key = "/".join(parts[:-2])

            if not is_plugin_enabled(hierarchical_key, settings.PLUGINS_ENABLED):
                if settings.DEV_MODE and plugin_name_before != plugin_name and log_all_map_ENABLED and False:
                    logger.info(f"🗺️ FALSE (by hierarchy): {hierarchical_key} ▉ {modname[:-4]}...")
                continue

            if plugin_name_before != plugin_name and log_all_map_ENABLED:
                logger.info(f"🗺️ ENABLED: {hierarchical_key} ▉ {modname[:-4]}...")
        try:
            module = importlib.import_module(modname)
            # logger.info(f"🗺️ Processing: {modname}")


            # Füge Daten hinzu, falls die Variablen existieren
            if hasattr(module, 'PUNCTUATION_MAP'):
                punctuation_map.update(module.PUNCTUATION_MAP)
            if hasattr(module, 'FUZZY_MAP_pre'):
                fuzzy_map_pre.extend(module.FUZZY_MAP_pre)
            if hasattr(module, 'FUZZY_MAP'):
                # 1. Get the raw map data
                raw_map = module.FUZZY_MAP

                # 2. Standardize the data structure using a list comprehension
                #    This ensures every item is 4 elements long (or fails if it's not 3 or 4)
                standardized_map = []
                for item in raw_map:
                    item_len = len(item)

                    if item_len == 3:
                        standardized_map.append(item + ({},))

                    elif item_len == 4:
                        standardized_map.append(item)

                    else:
                        logger.error(f"warning: FUZZY_MAP-length: ({item_len}): {item}",
                              file=sys.stderr)

                fuzzy_map.extend(standardized_map)

                # 3. Extend the main fuzzy_map with the standardized rules
                fuzzy_map.extend(standardized_map)

        except Exception as e:
            logger.error(f"Failed to process module '{modname}': {e}")

    logger.info(f"🗺️ Map loading complete. Found {len(fuzzy_map_pre)} FUZZY_MAP_pre rules.")

    logger.info(
        f"🗺️ TIP !!! Dont forget  __init__.py in each directory. If you missing replacements, please check this.")

    if settings.DEV_MODE_memory:
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"next: return punctuation_map, fuzzy_map_pre, fuzzy_map", logger)

    return punctuation_map, fuzzy_map_pre, fuzzy_map

from .correct_text_by_languagetool import correct_text_by_languagetool
import re, time
from thefuzz import fuzz
from .notify import notify


# Helper to check if a string contains regex special characters
def is_regex_pattern(pattern):
    # This is a simple heuristic. You can add more characters if needed.
    return any(char in pattern for char in r'^$*+?{}[]\|()")')


def apply_fuzzy_replacement_logic(processed_text, replacement, threshold, logger):

    log_all_processed_text = settings.DEV_MODE and False

    if type(processed_text) is int:
        if log_all_processed_text:
            logger.info(f"apply_fuzzy_replacement_logic():168: type(processed_text:{processed_text}) is int replacement:{replacement}")
        if processed_text==0:
            return processed_text
    # Ensure match_phrase is a string for fuzzy comparison if it's not a regex pattern
    # The threshold is given as a percentage (e.g., 82). difflib.SequenceMatcher ratio is 0.0-1.0.
    # So, we convert the threshold to a float between 0 and 1.
    similarity_threshold = threshold / 100.0 if threshold is not None else 0.70  # Default to 70% if no threshold given

    # Find possible fuzzy matches in the processed_text for the 'match_phrase'.
    # difflib.get_close_matches finds the best matches.
    # However, for finding and replacing *within* a text, we usually need to iterate
    # through the words of the text and compare each.

    # A simpler approach for "simple fuzzy match" if 'match_phrase' is a target word:
    # Iterate through words in processed_text and check similarity.
    words_in_text = re.findall(r'\b\w+\b', processed_text)  # Split text into words

    found_fuzzy_match = False
    # temp_processed_text = processed_text  # Use a temporary variable for replacements

    for word_in_text in words_in_text:

        # We need to iterate over the words in `processed_text` and compare each to `replacement`.
        words_in_text = re.findall(r'\b\w+\b', processed_text)
        temp_text_for_fuzzy_replace = processed_text

        for word_in_text_idx, word_in_text in enumerate(words_in_text):
            sm = difflib.SequenceMatcher(None, word_in_text.lower(),
                                         replacement.lower())  # Case-insensitive fuzzy
            similarity_ratio = sm.ratio()

            if similarity_ratio >= similarity_threshold:
                found_fuzzy_match = True
                logger.info(
                    f"✨Fuzzy Match found: '{word_in_text}' vs target '{replacement}' (Similarity: {similarity_ratio:.2f}, Threshold: {similarity_threshold:.2f})")
                # For simplicity, we'll use a direct string replace here.
                # A more precise method might involve finding the exact span of the word in original text.

                # For simple replacement of the *first* fuzzy matched instance:
                original_word_length = len(word_in_text)
                start_index = temp_text_for_fuzzy_replace.lower().find(word_in_text.lower())

                if start_index != -1:
                    temp_text_for_fuzzy_replace = (
                            temp_text_for_fuzzy_replace[:start_index] +
                            replacement +
                            temp_text_for_fuzzy_replace[start_index + original_word_length:]
                    )
                    found_fuzzy_match = True
                    logger.info(
                        f"🚀Fuzzy: '{processed_text}' -> '{temp_text_for_fuzzy_replace}' (Target: '{replacement}')")
                    processed_text = temp_text_for_fuzzy_replace  # Update processed_text
                    # If one fuzzy match is enough for this rule, break the inner loop
                    break  # Break from inner word iteration


        if found_fuzzy_match:
            # current_rule_matched = True  # Mark rule as matched due to fuzzy
            break  # Break the main loop after a successful fuzzy match as per original logic
    return processed_text


def apply_all_rules_may_until_stable(processed_text, fuzzy_map_pre, logger):
    new_processed_text, full_text_replaced_by_rule, skip_list = apply_all_rules_until_stable(
        processed_text
        , fuzzy_map_pre
        , logger)
    #made_a_change_in_cycle = None

    #log_all_processed_text = False and settings.DEV_MODE



    a_rule_matched = False
    if new_processed_text is False:
        #made_a_change_in_cycle = False
        log4DEV(f"new_processed_text is return ... None", logger)
        return new_processed_text, None, skip_list


    if full_text_replaced_by_rule:
        log4DEV("full_text_replaced_by_rule --> skip_list.append('LanguageTool')", logger)
        skip_list.append('LanguageTool')
        # regex_pre_is_replacing_all_maybeTEST1 = True
        log4DEV(f"242: 🔁??? new_processed_text: {new_processed_text}", logger)
        return new_processed_text, True, skip_list

    log4DEV(f"new_processed_text: {new_processed_text},  "
        f"skip_list:{skip_list} ,  full_text_replaced_by_rule: '{full_text_replaced_by_rule}'   ",logger)

    # if regex_pre_is_replacing_all_maybe:
    #     regex_match_found_prev = True  # need to be then also true for historical reasons. to be compatible to rest of the code
    log4DEV(f"skip_list={skip_list} 🔁🔁🔁🔁🔁 full_text_replaced_by_rule: '{full_text_replaced_by_rule}' ",logger)

    if new_processed_text:
        processed_text = new_processed_text
        log4DEV(f"251: 🔁🔁🔁🔁🔁 full_text_replaced_by_rule: '{full_text_replaced_by_rule}' ", logger)
    else:
        # scripts/py/func/process_text_in_background.py:248
        #for replacement, match_phrase, threshold, *flags_list, rule_mode in fuzzy_map_pre:
        for replacement, match_phrase, threshold, options_dict in fuzzy_map_pre:

            # logger.info(f"252: 🔁??? threshold: '{threshold}' based on pattern '{match_phrase}'")

            flags = options_dict.get('flags', 0)  # Hier extrahierst du den INTEGER korrekt
            skip_list = options_dict.get('skip_list', [])

            # logger.info(f"248: threshold={threshold} , skip_list: {skip_list}")

            # flags = flags_list[0] if flags_list else 0  # Default: 0 (case-sensitive)

            if is_regex_pattern(match_phrase):
                logger.debug(f" '👀pre -->{match_phrase}<-- 👀")

            # regex_pre_is_replacing_all_maybeTEST1 = match_phrase.startswith('^') and match_phrase.endswith('$')
            #regex_pre_is_replacing_all_maybe = regex_pre_is_replacing_all_maybeTEST1

            # Flag to track if a match (regex or fuzzy) was found for the current iteration
            current_rule_matched = False


            try:

                # <<< ÄNDERUNG 1: Speichere das Ergebnis von re.search in 'match_obj'
                match_obj = re.search(match_phrase, processed_text, flags=flags)

                # <<< ÄNDERUNG 2: Prüfe, ob 'match_obj' existiert
                if match_obj:
                    logger.info(
                        f"🔁 265: Regex_pre in: '{processed_text}' --> '{replacement}' based on pattern '{match_phrase}'")

                    # Die Ersetzung bleibt genau gleich
                    new_text = re.sub(
                        match_phrase,
                        replacement.strip(),
                        processed_text,
                        flags=flags
                    )

                    # Hier wird es interessant: Wir behalten den alten und den neuen Text für die Skripte
                    original_text_before_rule = processed_text

                    if new_text != original_text_before_rule:
                        logger.info(
                            f"🚀Regex_pre: '{processed_text}' -> '{new_text}' (Pattern: '{match_phrase}')")
                        processed_text = new_text

                    a_rule_matched = True

                    on_match_exec_list = options_dict.get('on_match_exec', [])

                    # <<< ÄNDERUNG 3: Bereite das 'match_data'-Paket für die Skripte vor
                    match_data = {
                        'original_text': original_text_before_rule,  # Der Text VOR der Regelanwendung
                        'text_after_replacement': new_text,  # Der Text NACH re.sub, aber VOR den Skripten
                        'regex_match_obj': match_obj,  # Das entscheidende Match-Objekt!
                        'rule_options': options_dict  # Die kompletten Optionen der Regel
                    }

                    for script_path in on_match_exec_list:
                        module = load_module_from_path(script_path)
                        logger.info(f"360: script_path:'{script_path}'")
                        if hasattr(module, 'execute'):
                            # <<< ÄNDERUNG 4: Übergebe das 'match_data'-Dictionary
                            script_result = module.execute(match_data)  # Das Skript gibt den finalen Text zurück

                            # lang_for_tts = "de-DE"  # Deine Standard-Systemsprache

                            new_current_text = ''
                            if isinstance(script_result, str):
                                new_current_text = script_result
                                # lang_for_tts bleibt der Standardwert "de-DE"

                            elif isinstance(script_result, dict):
                                # Fall 2: Dictionary mit Metadaten (unser Übersetzer-Plugin)
                                new_current_text = script_result.get("text")  # Hole den Text aus dem Dictionary
                                # Hole die Sprache aus dem Dictionary, mit einem Fallback auf die Standardsprache
                                lang_for_tts = script_result.get("lang", "de-DE")

                                handle_tts_fallback(new_current_text, lang_for_tts, logger)
                                logger.info(f"289: handle_tts_fallback({new_current_text}, {lang_for_tts}, logger)")

                            # WICHTIG: Dein Code beendet die Funktion hier nach dem ERSTEN Skript.
                            # Das ist okay, wenn pro Regel nur ein Skript vorgesehen ist.
                            return processed_text, a_rule_matched, skip_list

                    logger.info(f"Line 223: regex_match_found: break")
                    break  # Found a definitive match, stop this loop
            except re.error as e:
                logger.warning(f"Invalid regex_pre pattern in FUZZY_MAP_pre: '{match_phrase}'. Error: {e}")
                continue  # Skip this invalid rule

            if not current_rule_matched:
                # logger.info(f"310: new: new_processed_text={new_processed_text}, threshold={threshold} , a_rule_matched={a_rule_matched}")
                # , is in # file config/languagetool_server/PUNCTUATION_MAP.py
                if type(new_processed_text) is int and new_processed_text == 0:
                    # if log_all_processed_text:
                    log4DEV('TODO: what to do here?',logger)
                    # new_processed_text = ''
                new_processed_text = apply_fuzzy_replacement_logic(new_processed_text, replacement, threshold, logger)
                log4DEV(f"new: new_processed_text={new_processed_text} , threshold={threshold} , a_rule_matched={a_rule_matched}",logger)

    return new_processed_text, a_rule_matched, skip_list


GLOBAL_PUNCTUATION_MAP = {} # Use distinct names for clarity!
GLOBAL_FUZZY_MAP_PRE = [] # Note: fuzzy_map_pre is a list!
GLOBAL_FUZZY_MAP = []     # Note: fuzzy_map is a list!

def process_text_in_background(logger,
                               LT_LANGUAGE,
                               raw_text,
                               TMP_DIR,
                               recording_time,
                               active_lt_url,
                              output_dir_override = None):

    global GLOBAL_PUNCTUATION_MAP, GLOBAL_FUZZY_MAP_PRE, GLOBAL_FUZZY_MAP

    # scripts/py/func/process_text_in_background.py:167
    new_punctuation, new_fuzzy_pre, new_fuzzy = load_maps_for_language(LT_LANGUAGE, logger)

    GLOBAL_PUNCTUATION_MAP = new_punctuation
    GLOBAL_FUZZY_MAP_PRE = new_fuzzy_pre
    GLOBAL_FUZZY_MAP = new_fuzzy

    new_processed_text = ''
    skip_list=[]
    options_dict = None
    log4DEV(f"skip_list: {skip_list}", logger)

    try:

        # if settings.DEV_MODE:
        #     logger.info(f"start sanitize_transcription_start")
        raw_text = sanitize_transcription_start(raw_text)
        # if settings.DEV_MODE:
        #     logger.info(f"end sanitize_transcription_start")


        # ZWNBSP

        # DEV_MODE_all_processing = settings.DEV_MODE and True

        log4DEV(f"THREAD: Starting processing for: '{raw_text}'", logger)

        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")


        lang_code_predictions = ''

        log4DEV(f"process_text_in_background.py:371 raw_text:{raw_text}", logger)

        if len(raw_text) > 0:
            try:
                if LT_LANGUAGE == 'en-US':
                    threshold = 0.50  # Low threshold: switch even if not 100% sure it's German
                else:
                    threshold=0.60
                predictions = None
                if settings.ENABLE_AUTO_LANGUAGE_DETECTION:
                    logger.info(f"👀👀👀 Start lang_code predictions for: '{raw_text}'")
                    # predictions = fasttext_model.predict(raw_text, threshold=threshold)

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

        # scripts/py/func/process_text_in_background.py:229
        normalize_punctuation_changed_size = False
        is_only_number = False
        processed_text, was_exact_match = normalize_punctuation(raw_text, GLOBAL_PUNCTUATION_MAP)
        if len(processed_text) != len(raw_text):
            normalize_punctuation_changed_size = True
            new_processed_text = processed_text
            log4DEV(f"process_text_in_background.py:426 processed_text:{processed_text} ?? normalize_punctuation_changed_size:{normalize_punctuation_changed_size}", logger)

        if normalize_punctuation_changed_size:
            processed_text = re.sub(r'(?<=\d)\s+(?=\d)', '', processed_text)

            is_only_number =  processed_text.isdigit()

        # scripts/py/func/process_text_in_background.py

        #regex_pre_is_replacing_all = False
        regex_match_found_prev = False
        regex_pre_is_replacing_all_maybe = False
        result_languagetool = None

        log4DEV(
            f"proces..:'{processed_text}' new..:'{new_processed_text}'",logger)

        if not was_exact_match:

            regex_pre_is_replacing_all_maybeTEST1 = None

            log4DEV(f"new_processed_text: {new_processed_text}"
                f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe}"
                f" normalize_punctuation_changed_size={normalize_punctuation_changed_size}"
                f" regex_pre_is_replacing_all_maybeTEST1:{regex_pre_is_replacing_all_maybeTEST1}"
                f" regex_match_found_prev:{regex_match_found_prev}",logger)


            if settings.default_mode_is_all:
                # if true call iteratively all rules
                log4DEV(f"Applying all rules until stable (default 'all' mode).", logger)
                (new_processed_text
                , regex_pre_is_replacing_all_maybe
                , skip_list) = apply_all_rules_may_until_stable(processed_text
                , GLOBAL_FUZZY_MAP_PRE, logger)

                log4DEV(f"new_processed_text: {new_processed_text}"
                    f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe} "
                    f" skip_list={skip_list}",logger)


            regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe # and regex_match_found_prev
            log4DEV(f"new_processed_text: {new_processed_text}"
                f" regex_pre_is_replacing_all:{regex_pre_is_replacing_all} "
                f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe}"
                f" normalize_punctuation_changed_size={normalize_punctuation_changed_size}"
                f" regex_pre_is_replacing_all_maybeTEST1:{regex_pre_is_replacing_all_maybeTEST1}"
                f" regex_match_found_prev:{regex_match_found_prev}"
                f" skip_list={skip_list}",logger)

            log4DEV(f"new_processed_text:{new_processed_text}, regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe}",logger)

            log4DEV(f"LT_LANGUAGE = {LT_LANGUAGE} , SkipList=skip_list = {skip_list} , regex_pre_is_replacing_all_maybe ={regex_pre_is_replacing_all_maybe}",logger) #
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

            log4DEV(f"if ({not regex_pre_is_replacing_all}"
                f" and not {is_only_number}"
                f" and 📚📚'LanguageTool'📚📚 not in SkipList:{skip_list} "
                f" and not ( ... {processed_text}",logger)

            if (not regex_pre_is_replacing_all
                and not is_only_number
                and 'LanguageTool' not in skip_list
                and not (
                            settings.CORRECTIONS_ENABLED["git"]
                            and ("git " in processed_text or " push" in processed_text))):

                if new_processed_text ==0:
                    new_processed_text = processed_text

                log4DEV(f"and not 📚📚'LanguageTool'📚📚 in skip_list ==> {skip_list}"
                    f" processed_text:{processed_text}"
                    f" new_processed_text:{new_processed_text} ",logger)


                if settings.DEV_MODE_memory:
                    from scripts.py.func.log_memory_details import log_memory_details
                    log_memory_details(f"next  correct_text_by_languagetool:", logger)

                result_languagetool = correct_text_by_languagetool(
                    logger,
                    active_lt_url,
                    LT_LANGUAGE,
                    new_processed_text).lstrip('\uFEFF')



                if settings.DEV_MODE_memory:
                    from scripts.py.func.log_memory_details import log_memory_details
                    log_memory_details(f"last correct_text_by_languagetool:", logger)

            # Step 2: Slower, fuzzy replacements on the result
            # logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

            best_score = 0
            best_replacement = None

            # 80:scripts/py/func/process_text_in_background.py

            # --- NEW HYBRID MATCHING LOGIC ---

            # Pass 1: Prioritize and check for exact REGEX matches first.
            # A regex match is considered definitive and will stop further processing.
            log4DEV(f"SkipList: {skip_list} "
                    f" regex_pre_is_replacing_all:{regex_pre_is_replacing_all} "
                    f" processed_text:{processed_text} "
                    f" new_processed_text:{new_processed_text}" 
                    f" 📚📚result_languagetool📚📚:{result_languagetool} ",logger)
            # 477: SkipList: ['LanguageTool'] regex_pre_is_replacing_all:True processed_text:git at new_processed_text:git add .

            regex_match_found = False
            log4DEV(f'regex_pre_is_replacing_all:{regex_pre_is_replacing_all} ',logger)
            log4DEV(f"skip_list: {skip_list}", logger)
            skip_list_backup = skip_list
            options_dict = None
            log4DEV(f"skip_list_backup: {skip_list_backup}", logger)
            if not regex_pre_is_replacing_all and not is_only_number:
                log4DEV(f'in fuzzy_map: regex_pre_is_replacing_all:{regex_pre_is_replacing_all} ',logger)
                for replacement, match_phrase, threshold, options_dict in GLOBAL_FUZZY_MAP:
                    log4DEV(f'for {replacement}, {match_phrase} ... in fuzzy_map:', logger)

                    # logger.info(
                    #     f'process_text_in_background.py:549 in fuzzy_map:'
                    #     f' regex_pre_is_replacing_all:{regex_pre_is_replacing_all}'
                    #     f' replacement:{replacement}'
                    #     f' match_phrase:{match_phrase}'
                    #     f' threshold:{threshold}')

                    flags = options_dict.get('flags', 0)  # Standardwert ist 0, wenn kein Flag angegeben
                    #log4DEV(f"skip_list: {skip_list}", logger)
                    skip_list = options_dict.get('skip_list', [])  # Standardwert ist leere Liste
                    #log4DEV(f"skip_list: {skip_list}", logger)

                    # ... Rest deiner Logik
                    # logger.info(f"Flags: {flags}, Skip List: {skip_list}")
                    if skip_list:
                        log4DEV(f"Skip List:{skip_list} ==> sys.exit(1)",logger)
                        sys.exit(1)

                    log4DEV(f"is_regex_pattern({match_phrase})",logger)
                    # is_regex_pattern seems useless here. we also can replace with normal text. must not look like a regex. 8.11.'25
                    if True or is_regex_pattern(match_phrase):
                        # logger.info(f"516 in fuzzy_map: '👀 -->{match_phrase}<-- 👀")
                        log4DEV(f"re.search({match_phrase}, {result_languagetool}..):",logger)

                        try:

                            if result_languagetool is None:
                                log4DEV("Skipping regex matching because result_languagetool is None.", logger)
                                continue

                            if not re.search(match_phrase, result_languagetool, flags=flags):
                                continue
                            log4DEV(f"🔁Regex in: '{result_languagetool}' --> '{replacement}' based on pattern '{match_phrase}'",logger)

                            new_text = re.sub(
                                match_phrase,
                                replacement.strip(),
                                result_languagetool,
                                flags=flags
                            )

                            if new_text != result_languagetool:
                                log4DEV(
                                    f"Regex match: '{result_languagetool}' -> '{new_text}' (Pattern: '{match_phrase}')",logger)
                                processed_text = new_text
                                result_languagetool = new_text # TODO: lazy programming

                            regex_match_found = True
                            break  # Found a definitive match, stop this loop

                        except re.error as e:
                            logger.warning(f"704: Invalid regex pattern in FUZZY_MAP: '{match_phrase}'. Error: {e}")
                            continue # Skip this invalid rule
                        except Exception as e:
                            logger.warning(f"❌ 707: FUZZY_MAP: '{match_phrase}'. Error: {e}")

            # Pass 2: If no regex matched, perform the FUZZY search as before.
            # This code will only run if the loop above didn't find a regex match.



            if (not regex_pre_is_replacing_all
                    and not regex_pre_is_replacing_all_maybe
                    and not regex_match_found
                    and not is_only_number):
                log4DEV(f"No regex match. Proceeding to fuzzy search for: '{processed_text}'",logger)
                best_score = 0
                best_replacement = None

                log4DEV(f"skip_list_backup: {skip_list_backup}", logger)
                skip_list=skip_list_backup

                # for replacement, match_phrase, threshold in fuzzy_map:
                for replacement, match_phrase, threshold, *_ in GLOBAL_FUZZY_MAP:
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

        if new_processed_text:
            log4DEV(f"SkipList: {skip_list} regex_match_found_prev:{regex_match_found_prev} regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe} processed_text:{processed_text} "
                    f"new_processed_text:{new_processed_text}",logger)
        # 477: SkipList: ['LanguageTool'] regex_pre_is_replacing_all:True processed_text:git at new_processed_text:git add .


        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
            if settings.ADD_TO_SENCTENCE:
                if len(processed_text)> 70 and re.match(r"\w\s*$", processed_text):
                    processed_text +=  settings.ADD_TO_SENCTENCE
        recording_time = time.time()

        # file: scripts/py/func/process_text_in_background.py
        # ... watchDir := "C:\tmp\sl5_aura"
        timestamp = int(time.time() * 1000)

        if output_dir_override:
            # unique_output_file = f"{output_dir_override}/tts_output_{timestamp}.txt"
            unique_output_file = output_dir_override / f"tts_output_{timestamp}.txt"
        else:
            unique_output_file = TMP_DIR / f"sl5_aura/tts_output_{timestamp}.txt"

        log4DEV(
            f"SkipList:{skip_list} "
            f" processed_text:{processed_text} "
            f" new_processed_text:{new_processed_text}"
            f" result_languagetool:{result_languagetool} ",logger)
        # SkipList: ['LanguageTool'] regex_pre_is_replacing_all:True processed_text:git at new_processed_text:git add .
        # SkipList:[]  processed_text: mit nachnamen Lauffer  new_processed_text:False result_languagetool:Mit Nachnamen lauf er


        if not new_processed_text:
            log4DEV(f"Empty results are allowed not |||  SkipList:{skip_list}"
                f" new_processed_text:{new_processed_text}"
                f" result_languagetool:{result_languagetool}"
                f" processed_text:{processed_text} ",logger)

        if new_processed_text != processed_text:
            processed_text = new_processed_text

        # unique_output_file = TMP_DIR / f"sl5_aura/tts_output_{timestamp}.txt"
        # unique_output_file.write_text(processed_text)
        log4DEV(f"SkipList:{skip_list}"
            f" new_processed_text:{new_processed_text}"
            f" result_languagetool:{result_languagetool}"
            f" processed_text:{processed_text} ",logger)

        #processed_text = (result_languagetool) ? result_languagetool : processed_text



        processed_text = result_languagetool if result_languagetool else processed_text

        script_result = processed_text  # Wir starten mit dem Originaltext

        # new_current_text wird das finale Ergebnis sein

        new_current_text = None
        # lang_for_tts startet mit der Originalsprache
        lang_for_tts = LT_LANGUAGE

        # --- Hier wird die Magie passieren ---
        # (Dein Code, der das Plugin aufruft und script_result füllt, fehlt hier, aber das Ergebnis ist klar)
        # Nehmen wir an, script_result ist jetzt das Dictionary vom Übersetzer

        if isinstance(script_result, str):
            new_current_text = script_result
            # lang_for_tts bleibt die Standardsprache

        elif isinstance(script_result, dict):
            new_current_text = script_result.get("text")
            lang_for_tts = script_result.get("lang", LT_LANGUAGE)  # Fallback auf Originalsprache

        # --- AB HIER KOMMEN DIE KORREKTUREN ---

        if new_current_text:

            if options_dict: # If it exists, no sub-module will be output. they have may its own signature.
                # e.g. the tranlating modules have their own signature
                log4DEV(f"options_dict={options_dict}",logger)

                if type(new_current_text) is str and len(new_current_text) >= 11:
                    new_current_text += f"{settings.signatur1}"

            new_current_text = sanitize_transcription_start(new_current_text)

            # DIESE ZEILE WAR SCHON RICHTIG:
            unique_output_file.write_text(new_current_text, encoding="utf-8-sig")

            # KORREKTUR 1: Verwende die NEUEN Variablen für den Fallback
            handle_tts_fallback(new_current_text, lang_for_tts, logger)
            log4DEV(f"handle_tts_fallback({new_current_text}, {lang_for_tts})",logger)

            # KORREKTUR 2: Logge den Text, der WIRKLICH geschrieben wurde
            logger.info(f"✅ THREAD: Successfully wrote to {unique_output_file} '{new_current_text}'")
        else:
            logger.warning("Nach der Plugin-Verarbeitung gab es keinen Text zum Ausgeben.")







        #
        # notify("Transcribed", duration=700, urgency="low")

        notify("Transcribed", "", "low", duration=1000, replace_tag="transcription_status")

    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        notify(f"FATAL: Error in processing thread", duration=4000, urgency="low")
    finally:
        # file: scripts/py/func/process_text_in_background.py
        if settings.DEV_MODE:
            logger.info(f"✅ Background processing for '{raw_text[:20]}...' finished. ")
            notify(f" Background processing for '{raw_text[:20]}...' finished. ", duration=700, urgency="low")

        # # scripts/py/func/process_text_in_background.py:433 TODO fallback:
        max_model_memory_footprint_mb_not_calculate =  5000

        # 21:05:34,680 - INFO     - Attempting to load missing model: 'vosk-model-en-us-0.22'
        # 21:05:43,987 - INFO     - Learned new max model footprint: ~4.4GB

        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        rss_mb = mem_info.rss / (1024 * 1024)
        if (rss_mb*0.4) > max_model_memory_footprint_mb_not_calculate:
            # restart your script is a very common and effective fallback workaround for managing excessive memory usage
            logger.info(f"Fallback restart script: rss_mb={rss_mb}*2.5 > max_model_memory_footprint={max_model_memory_footprint_mb_not_calculate}")
            # restart script
            time.sleep(0.02)
            os.execv(sys.executable, ['python'] + sys.argv + ['restarted'])

        auto_reload_modified_maps(logger)
# Hallo des Hallo Test

def sanitize_transcription_start(raw_text: str) -> str:
    """
    ﻿test (original:'test', Voice Translation SL5.de/Aura ).
    ZWNBSP

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
        if char.isalnum() or char == '/' or char == '~': # <-- MODIFICATION HERE
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


def handle_tts_fallback(processed_text: str, LT_LANGUAGE: str, logger):
    # scripts/py/func/process_text_in_background.py:900
    home_dir = Path.home()
    speak_piper_file_path = home_dir / "projects" / "py" / "TTS" / "speak_file.py"
    primary_tts_successful = False
    if not speak_piper_file_path.exists():
        primary_tts_successful = False
    use_fallback = (
            settings.USE_AS_PRIMARY_SPEAK == "ESPEAK" or
            (not primary_tts_successful and settings.USE_ESPEAK_FALLBACK and processed_text)
    )
    if use_fallback:
        logger.warning("primary TTS failed. try Espeak-Fallback...")
        speak_fallback(processed_text, LT_LANGUAGE)


def apply_all_rules_until_stable(text, rules_map, logger_instance):
    """
    Applies all rules from the given rules_map iteratively to the text until the text no longer changes after a complete pass through all the rules.
    Replaces the entire match of the regex without group references with the replacement_text.

    Args:
        text (str): The input text on which the substitutions should be applied.
        rules_map (list): A list of rule tuples. Each tuple in the format:
                          (replacement_text, regex_pattern, threshold_value, optional_flags).
                          The threshold_value is ignored.
        logger_instance (logging.Logger): The logger for logging.

    Returns:
        tuple: A tuple (str, bool).
               str: The stabilized text.
               bool: True if a complete replacement of the text by a rule has taken place, indicating an early termination. False otherwise.
    """
    # log_all_changes = False and settings.DEV_MODE

    skip_list = []

    previous_text = ""
    current_text = text
    full_text_replaced_by_rule = False

    regex_pattern = None

    made_a_change = 0

    # --- START OF STABILITY PATCH: TIME-BASED WARNING/THROTTLE ---
    MAX_PROCESSING_SECONDS = 2.0  # Threshold for warning the user about an infinite loop
    RECURSION_LOOP_START_TIME = time.time()
    WARNING_ISSUED = False

    # We also add a simple counter for robustness in case time.time() is unreliable
    MAX_ITERATIONS_FOR_SAFETY = 50000
    current_iteration = 0
    # --- END OF STABILITY PATCH ---


    while current_text != previous_text:
        previous_text = current_text
        made_a_change_in_cycle = False
        full_text_replaced_by_rule = False

        # --- Stability Check inside the loop (Line 970 area) ---
        current_iteration += 1
        elapsed_time = time.time() - RECURSION_LOOP_START_TIME

        if elapsed_time > MAX_PROCESSING_SECONDS or current_iteration > MAX_ITERATIONS_FOR_SAFETY:
            if not WARNING_ISSUED:
                # Issue the warning to both the main log and the console
                warning_message = (
                    f"⚠️ CRITICAL WARNING: Recursive map processing exceeded {MAX_PROCESSING_SECONDS}s "
                    f"or {MAX_ITERATIONS_FOR_SAFETY} iterations. This suggests an infinite loop in your maps. "
                    f"Processing continues but check your last map change (e.g., recursive rule 'hallo')."
                )
                logger_instance.error(warning_message)
                print(warning_message, file=sys.stderr)  # Output to console/stderr
                WARNING_ISSUED = True

            # Throttle the loop by forcing a break, but ONLY if the time is exceeded (not just the iteration count)
            if elapsed_time > MAX_PROCESSING_SECONDS + 0.5:  # Give it half a second grace period after warning
                break
        # --- END OF STABILITY CHECK ---


        for rule_entry in rules_map:
            # (replacement_text, regex_pattern, threshold_value, options_dict)
            replacement_text, regex_pattern, threshold, options_dict = rule_entry

            # Extrahiere die Flags aus dem options_dict
            flags = options_dict.get('flags', 0) # Jetzt ist 'flags' ein Integer
            skip_list_temp = options_dict.get('skip_list', [])
            skip_list=skip_list_temp
            log4DEV(f"{full_text_replaced_by_rule} skip_list:{skip_list} , skip_list_temp={skip_list_temp} (Pattern: '{regex_pattern}')",logger_instance)

            #log4DEV(f"made_a_change={made_a_change} REPLACE:{full_text_replaced_by_rule} options_dict={options_dict} skip_list:{skip_list} (Pattern: '{regex_pattern}')",logger_instance)

            # Den threshold hast du jetzt auch direkt entpackt

            sub_replacement_string = replacement_text

            try:
                match_obj = re.fullmatch(regex_pattern, current_text, flags=flags)
                if match_obj:
                    # Der ursprüngliche Text, bevor irgendetwas geändert wird
                    original_text_for_script = current_text
                    log4DEV(f"original..={original_text_for_script}", logger_instance)

                    new_current_text = re.sub(
                        regex_pattern,
                        sub_replacement_string,
                        current_text,
                        flags=flags
                    )
                    log4DEV(f"new..={new_current_text}", logger_instance)
                    log4DEV(f"regex_pattern:{regex_pattern}, sub_replacement_string={sub_replacement_string}", logger_instance)

                    if new_current_text != original_text_for_script:

                        log4DEV(f"new..:'{new_current_text}' "
                                f"!= original..:'{original_text_for_script}'",logging)

                        match_data = {
                            'original_text': original_text_for_script,
                            'text_after_replacement': new_current_text,
                            'regex_match_obj': match_obj,  # Wir haben es bereits von re.fullmatch
                            'rule_options': options_dict
                        }

                        on_match_exec_list = options_dict.get('on_match_exec', [])
                        for script_path in on_match_exec_list:
                            module = load_module_from_path(script_path)
                            if module and hasattr(module, 'execute'):
                                # <<< ÄNDERUNG 2: Übergebe match_data und aktualisiere den Text
                                new_current_text = module.execute(match_data)
                                log4DEV(f"module:'{module}' new_current_text='{new_current_text}'",logging)

                        # <<< HINWEIS: Dein restlicher Code kann jetzt unverändert bleiben >>>
                        # Er verwendet new_current_text, das jetzt das finale Ergebnis aus den Skripten enthält.

                        log4DEV(f"new..:'{new_current_text}' != original..:'{original_text_for_script}'",logging)

                        made_a_change_in_cycle = True
                        made_a_change = made_a_change + 1
                        skip_list = skip_list_temp
                        current_text = new_current_text  # Jetzt wird der finale Text zugewiesen

                        full_text_replaced_by_rule = True  # because was full-match
                        log4DEV(f"full_text_replaced_by_rule = {full_text_replaced_by_rule}",logger_instance)

                        log4DEV(f"🚀🚀 skip_list:{skip_list} 🚀🚀🚀819: made_a_change={made_a_change} '{original_text_for_script}' ----> '{current_text}' (Pattern: '{regex_pattern}') Iterative-All-Rules FULL_REPLACE:{full_text_replaced_by_rule}",logger_instance)

                        if 'fullMatchStop' not in skip_list:
                            break

                else:  # Dieser Block wird ausgeführt, wenn es KEIN fullmatch gab

                    # <<< ÄNDERUNG 3: Wir müssen hier explizit nach einem partiellen Match suchen, um das match_obj zu bekommen
                    partial_match_obj = re.search(regex_pattern, current_text, flags=flags)

                    # Nur fortfahren, wenn auch wirklich etwas gefunden wurde
                    if partial_match_obj:
                        original_text_for_script = current_text
                        new_current_text = re.sub(
                            regex_pattern,
                            sub_replacement_string,
                            current_text,
                            flags=flags
                        )

                        if new_current_text != original_text_for_script:

                            # Erstelle das match_data-Dictionary für den partiellen Match
                            match_data = {
                                'original_text': original_text_for_script,
                                'text_after_replacement': new_current_text,
                                'regex_match_obj': partial_match_obj,  # Verwende das neue partial_match_obj
                                'rule_options': options_dict
                            }

                            on_match_exec_list = options_dict.get('on_match_exec', [])
                            for script_path in on_match_exec_list:
                                module = load_module_from_path(script_path)
                                if module and hasattr(module, 'execute'):
                                    # Übergebe match_data und aktualisiere den Text
                                    # new_current_text = module.execute(match_data)

                                    script_result = module.execute(match_data)

                                    # Standardwerte initialisieren
                                    # lang_for_tts = "de-DE"  # Deine Standard-Systemsprache

                                    if isinstance(script_result, str):
                                        new_current_text = script_result
                                        # lang_for_tts bleibt der Standardwert "de-DE"

                                    elif isinstance(script_result, dict):
                                        # Fall 2: Dictionary mit Metadaten (unser Übersetzer-Plugin)
                                        new_current_text = script_result.get("text")  # Hole den Text aus dem Dictionary
                                        # Hole die Sprache aus dem Dictionary, mit einem Fallback auf die Standardsprache
                                        lang_for_tts = script_result.get("lang", "de-DE")

                                        handle_tts_fallback(new_current_text, lang_for_tts, logger_instance)
                                        logger_instance.info(f"1026: handle_tts_fallback({new_current_text}, {lang_for_tts}, logger_instance)")



                                # Dein restlicher Code für diesen Block
                            made_a_change += 1
                            log4DEV(
                                    f"834🚀🚀Iterative-All-Rules made_a_change={made_a_change} : '{original_text_for_script}' -> '{new_current_text}' (Pattern: '{regex_pattern}')",logger_instance)

                            current_text = new_current_text
                            made_a_change_in_cycle = True
            except re.error as e:
                logger_instance.error(f"Invalid regex pattern in map: '{regex_pattern}' - {e}. Skipping rule.")

        if full_text_replaced_by_rule:
            made_a_change = True
            log4DEV(f"made a_change: {made_a_change}",logger_instance)
            logger_instance.info(
                f"🚀Iterative-All-Rules: full_text_replaced_by_rule='{full_text_replaced_by_rule}, skip_list='{skip_list}'")


            break

        if not made_a_change_in_cycle:
            break

    if not made_a_change:
        log4DEV(f"made_a_change={made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",logger_instance)
        #  z.b. "das ist ein test landet" hier. Es gibt auch (höchstwahrschienlich keine Regel hiervür. Also correkt.
        # logging.info('sys.exit(1) 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923')
        # sys.exit(1) # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 Test
        log4DEV(f"🚀🚀🚀skip_list:{skip_list} made_a_change:{made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",
                logger_instance)
        return made_a_change, full_text_replaced_by_rule, skip_list
        log4DEV(f"🚀🚀🚀skip_list:{skip_list} made_a_change:{made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",logger_instance)
    # 17:08:56,492 - INFO     - 758: made_a_change=True full_text_replaced_by_rule:False current_text:mit nachnamen Lauffer

    # 1. Calculate the Ratio
    lt_skip_ratio_threshold = settings.LT_SKIP_RATIO_THRESHOLD
    len_previous_text = len(previous_text)
    ratio = len_previous_text / made_a_change if made_a_change > 0 else float('inf')

    # 2. Check against the threshold
    # If the text is short OR the change density is high (low ratio), skip LT.
    if ratio < lt_skip_ratio_threshold and 'LT_SKIP_RATIO_THRESHOLD' not in skip_list:
        log4DEV(
            f"skip_list:{skip_list}",logger_instance)

        # Check if LanguageTool is not already marked for skipping
        if 'LanguageTool' not in skip_list:
            explain =f'ratio:{ratio} < {lt_skip_ratio_threshold}: If the text is short OR the change density is high (low ratio), skip LT.'
            log4DEV(f"explain:{explain}",logger_instance)
            # Add LT to the skip list
            skip_list.append('LanguageTool')
            log4DEV("skip_list.append('LanguageTool')",logger_instance)

            # 3. Add the Warning Message
            log4DEV(
                f"LT Skipped (Heuristic): Change density is too high or text too short. "
                f"Length: {len_previous_text}, Changes: {made_a_change}. "
                f"Ratio ({ratio:.2f}) is below threshold ({lt_skip_ratio_threshold})."
            ,logger_instance)


    # if made_a_change > 1:
    #     if 'LanguageTool' not in skip_list:
    #         skip_list.append('LanguageTool')
    log4DEV(f"🚀🚀🚀skip_list:{skip_list} "
            f"regex_pattern={regex_pattern} made_a_change:{made_a_change} "
            f"full_text_replaced_by_rule:{full_text_replaced_by_rule} "
            f"current_text:{current_text}",logger_instance)
    # 17:08:56,492 - INFO     - 758: made_a_change=True full_text_replaced_by_rule:False current_text:mit nachnamen Lauffer

    return current_text, full_text_replaced_by_rule, skip_list

#
