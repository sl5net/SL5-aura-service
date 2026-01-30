# scripts/py/func/process_text_in_background.py
import difflib
import logging
import os
import pkgutil
#import pprint
import sys

import importlib.util
from pathlib import Path
# from platform import system

import psutil

#import shutil
#import subprocess

from .audio_manager import speak_fallback
from .auto_fix_module import try_auto_fix_module
from .get_active_window_title import get_active_window_title_safe
from .log_memory_details import log4DEV
from .state_manager import should_trigger_startup
from .windows_apply_correction_with_sync import windows_apply_correction_with_sync

# scripts/py/func/process_text_in_background.py:25
from .global_state import SEQUENCE_LOCK, SESSION_LAST_PROCESSED, OUT_OF_ORDER_CACHE, SIGNATURE_TIMES


from .correct_text_by_languagetool import correct_text_by_languagetool
import re, time
from thefuzz import fuzz
from .notify import notify


from scripts.py.func.config.dynamic_settings import DynamicSettings


import platform

settings = DynamicSettings()

# global last_signature_time

# active_window_title = None
global _active_window_title

from .normalize_punctuation import normalize_punctuation
from .map_reloader import auto_reload_modified_maps

import importlib

from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model

from .setup_initial_model import get_model_name_from_key





# scripts/py/func/process_text_in_background.py
GLOBAL_PUNCTUATION_MAP = {} # noqa: F824
GLOBAL_FUZZY_MAP_PRE = [] # noqa: F824
GLOBAL_FUZZY_MAP = [] # noqa: F824

GLOBAL_debug_skip_list=False

from .config.regex_cache import REGEX_COMPILE_CACHE


def normalize_fuzzy_map_rule_entry(entry):
    if len(entry) == 2:
        return *entry, 75, {'flags': re.IGNORECASE}
    if len(entry) == 3:
        if isinstance(entry[2], dict):
            # Fall: (Ersatz, Pattern, {Optionen}) -> Die 0 (Schwelle) fehlt!
            return entry[0], entry[1], 100, entry[2]
        else:
            # Fall: (Ersatz, Pattern, Schwelle) -> Die Optionen fehlen!
            return entry[0], entry[1], entry[2], {'flags': re.IGNORECASE}

        # return (*entry, {'flags': re.IGNORECASE})


    return entry

def execute_hook(logger, module, hook_name, lock_key):
    if hasattr(module, hook_name):
        # Unique lock ID for the specific hook and context
        full_lock_id = f"{lock_key}_{hook_name}"
        if should_trigger_startup(full_lock_id):
            try:
                # Correct way to call a function by string name
                hook_func = getattr(module, hook_name)
                if callable(hook_func):
                    hook_func()
            except Exception as e:
                logger.error(f"Error in {hook_name} for {lock_key}: {e}")

def repariere_pakete_mit_laenderkuerzeln(logger, basis_pfad: Path, aktuelle_tiefe: int = 1, max_tiefe: int = 2):
    """
    Durchsucht den gegebenen Pfad und seine direkten Unterordner (bis max_tiefe)
    und erstellt fehlende __init__.py-Dateien.

    Args:
        basis_pfad: Der Pfad, der gescannt werden soll (als Path-Objekt).
        aktuelle_tiefe: Interne Zählvariable. Startet bei 1.
        max_tiefe: Die maximale Rekursionstiefe (hier 2).
    """

    if not basis_pfad.is_dir():
        # print(f"Warnung: Pfad '{basis_pfad}' existiert nicht oder ist kein Ordner.")
        return

    # Liste, um die Unterordner für die nächste Rekursion zu speichern
    unterordner_zur_weitergabe = []
    reparierte_anzahl = 0

    # 1. Scanne den aktuellen Pfad (basis_pfad) und repariere fehlende __init__.py
    for eintrag in basis_pfad.iterdir():
        # logger.info(f"eintrag {eintrag } llllllllllllllllllllllllllllllllllllllllll")

        if eintrag.is_dir() and eintrag.name != '__pycache__':
            init_datei = eintrag / "__init__.py"

            # Speichere den Ordner für die nächste Stufe
            unterordner_zur_weitergabe.append(eintrag)

            # 1.1 REPARATUR des aktuellen Unterordners
            if not init_datei.exists():
                try:
                    init_datei.touch()
                    logger.info(f"Repariert (Stufe {aktuelle_tiefe}): __init__.py erstellt in: {eintrag}")
                    reparierte_anzahl += 1
                except OSError as e:
                    logger.error(
                        f"FEHLER: Konnte __init__.py in '{eintrag}' nicht erstellen: {e}")
            else:
                logger.info(f"found init_datei in: {eintrag}")

    # 2. Rekursion in die nächste Stufe (Ländercodes)
    if aktuelle_tiefe < max_tiefe:
        logger.info(
            f"🗺️ {aktuelle_tiefe} < {max_tiefe} ##########################################################################################################################################")
        for unterordner in unterordner_zur_weitergabe:
            logger.info(
                f"🗺️ {unterordner} OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

            # Rufe die Funktion für jeden Unterordner auf (z.B. Ländercode-Ordner)
            reparierte_anzahl += repariere_pakete_mit_laenderkuerzeln(logger,
                unterordner,
                aktuelle_tiefe + 1,
                max_tiefe
            )

    return reparierte_anzahl

# This is your function at line 17
def load_module_from_path(script_path, run_mode_override=None):
    if GLOBAL_debug_skip_list:
        print(f'86: run_mode_override: {run_mode_override}')

    path = Path(script_path)

    # scripts/py/func/process_text_in_background.py:88
    if run_mode_override:
        RUN_MODE = run_mode_override
    else:
        RUN_MODE = os.getenv('RUN_MODE')  # returns None or the value


    if RUN_MODE == "API_SERVICE" and path.parent.name.startswith('_'):
        print(
            f"a####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None
    if RUN_MODE == "API_SERVICE" and path.parent.parent.name.startswith('_'):
        print(
            f"b####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None
    if RUN_MODE == "API_SERVICE" and path.parent.parent.parent.name.startswith('_'):
        print(
            f"c####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")
        return None    # Ignore folders that start with _

    print(
        f"####### map_file_path={path.parent.parent.parent.parent.name} {path.parent.parent.parent.name} {path.parent.parent.name} {path.parent.name} {path.name} ++++++++++++++++++++++++")

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
        #


        print(f"168: TODO: performance killer (2025-1225-1950)")
        print(f"168: TODO: performance killer (2025-1225-1950)")
        print(f"168: TODO: performance killer (2025-1225-1950)")



# from .audio_manager import unmute_microphone

"""
doc:
how test language tool in command line:
curl --data "language=de-DE&text=das stimmt unsere ist nicht absolut fehlerfrei" http://localhost:8081/v2/check
"""

# from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW

# scripts/py/func/process_text_in_background.py:120


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

    # process_text_in_background.py:260 (is_plugin_enabled)
    return True


def load_maps_for_language(lang_code, logger, run_mode_override=None):
    # process_text_in_background.py:265 (load_maps_for_language)
    if getattr(settings, "DEV_MODE_memory", False):
        from .log_memory_details import log_memory_details
        log_memory_details(f"def load_maps_for_language", logger)

    logger.info(f"🗺️Starting recursive map loading for language: {lang_code}, run_mode_override:{run_mode_override}")

    settings.reload_settings()

    if getattr(settings, "DEV_MODE_memory", False):
        from .log_memory_details import log_memory_details
        log_memory_details(f"next: auto_reload_modified_maps", logger)

    # Zuerst alle Module im Speicher neu laden, um Änderungen zu erfassen
    auto_reload_modified_maps(logger,run_mode_override)



    if getattr(settings, "DEV_MODE_memory", False):
        from .log_memory_details import log_memory_details
        log_memory_details(f"last: auto_reload_modified_maps", logger)

    # Leere Container für die zusammengefügten Daten
    punctuation_map = {}
    fuzzy_map_pre   = []
    fuzzy_map       = []

    # process_text_in_background.py:290 (load_maps_for_language)
    try:
        maps_package = importlib.import_module('config.languagetool_server.maps')
        log4DEV("whats this?", logger)
    except ModuleNotFoundError:
        maps_package = importlib.import_module('config.maps')
        log4DEV("whats this?", logger)

    plugin_name_before = ''
    plugin_name = ''
    ENABLED_modname_list = []

    if run_mode_override:
        RUN_MODE = run_mode_override
    else:
        RUN_MODE = os.getenv('RUN_MODE')  # returns None or the value

    # logger.info(f'245: run_mode_override:{run_mode_override} , run_mode:{RUN_MODE}')
    # process_text_in_background.py:310 (load_maps_for_language)
    for importer, modname, ispkg in pkgutil.walk_packages(
            path=maps_package.__path__,
            prefix=maps_package.__name__ + '.',
            onerror=lambda x: None):


        is_private = False

        # scripts/py/func/process_text_in_background.py:316 (load_maps_for_language)
        if "._" in modname or "/_" in modname or "\\_" in modname  :
            is_private = True
        if RUN_MODE == "API_SERVICE" and ( "._" in modname or "/_" in modname  ):
            continue # maps with underscore are private
        # logger.debug(f"📚Found module candidate: {modname}",logger)
        # log4DEV(f"📚Found module candidate: {modname}",logger)


        #     In modules use import os and os.getenv('RUN_MODE') where needed.

        #test 55test 55test 55test 55Jeffs


        if ispkg:
            continue

        if f".{lang_code}." not in modname:
            continue

        log4DEV(f"############################## modname {modname}",logger)

        # process_text_in_background.py:341 (load_maps_for_language)

            # for key, val in modname.items():
            #     if isinstance(val, dict):
            #         val['is_private'] = is_private
            #         val['source_modname'] = modname

        log_all_map_ENABLED = True and settings.DEV_MODE
        hierarchical_key = None
        if ".plugins." in modname:
            if len(parts := modname.split('.plugins.', 1)[1].split('.')) < 2:
                logger.warning(f"Could not determine plugin_name from modname: {modname}. Skipping.")
                continue

            plugin_name_before, plugin_name = plugin_name, parts[-3]
            hierarchical_key = "/".join(parts[:-2])


            log4DEV(f'##### {hierarchical_key} #######', logger)
            log4DEV(hierarchical_key, logger)


            if not is_plugin_enabled(hierarchical_key, settings.PLUGINS_ENABLED):
                if settings.DEV_MODE and plugin_name_before != plugin_name and log_all_map_ENABLED and False:
                    logger.info(f"🗺️ FALSE (by hierarchy): {hierarchical_key} ▉ {modname[:-4]}...")

                    #basis_pfad = Path(os.path.dirname(settings._settings_file_path)) / "maps"
                    #eltern_pfad_maps = basis_pfad / hierarchical_key
                    # repariere_pakete_mit_laenderkuerzeln(logger, eltern_pfad_maps, max_tiefe=1)

                continue

            # scripts/py/func/process_text_in_background.py:304 (load_maps_for_language)
            if plugin_name_before != plugin_name:

                if settings.show_PLUGINS_ENABLED:
                    # logger.info(f"🗺️ ENABLED: {hierarchical_key} ▉ {modname[:-4]}...")
                    ENABLED_modname_list.append(hierarchical_key)


                # pprint.pprint(vars(settings))

                #basis_pfad = Path(os.path.dirname(settings._settings_file_path)) / "maps"

                # eltern_pfad_maps = basis_pfad / hierarchical_key
                # repariere_pakete_mit_laenderkuerzeln(logger,eltern_pfad_maps, max_tiefe=2)
                # print(f"eltern_pfad_maps={eltern_pfad_maps} -> anzahl: {anzahl}")
                # exit(1)

        try:
            # process_text_in_background.py:430 (load_maps_for_language)
            module = importlib.import_module(modname)

            # logger.info(f"🗺️ Processing: {modname}")
            # logger.info(f"🔎 Checking {modname} for hooks. Attributes: {dir(module)}")

            # logger.info(f"313: found on_startup: {plugin_name}")
            # logger.info(f"1 {module.__dir__()}_on_startup")
            # logger.info(f"2 {module.Path}_on_startup")
            # logger.info(f"3 {module.Path}_on_startup")
            # logger.info(f"4 {module.RULES_FILE_PATH}_ 123456789")
            # logger.info(f"5 {module.__package__}_on_startup")
            # logger.info(f"6 {module.__cached__}_on_startup")
            # logger.info(f"7 {hierarchical_key}{module.__dir__()}_on_startup")
            # sys.exit(1)

            # {module.__package__}

            execute_hook(logger, module, 'on_plugin_load', hierarchical_key)
            execute_hook(logger, module, 'on_file_load', module.__package__)

            # hook_name = 'on_package_when_first_speak_trigger_is_pressed'
            # if hasattr(module, hook_name):
            #     if should_trigger_startup(f"{hierarchical_key}_{hook_name}"):
            #         if should_trigger_startup(f"{module.RULES_FILE_PATH}_{hook_name}"):
            #             try:
            #                 hook_function = getattr(module, hook_name)
            #                 hook_function()
            #             except Exception as e:
            #                 m = f"336: {hook_name} failed for {hierarchical_key}_{hook_name}: {e}"
            #                 logger.info(m)
            #
            # hook_name = 'on_startup_when_first_speak_trigger_is_pressed'
            # if hasattr(module, hook_name):
            #     if should_trigger_startup(f"{module.RULES_FILE_PATH}_{hook_name}"):
            #         try:
            #             hook_function = getattr(module, hook_name)
            #             hook_function()
            #         except Exception as e:
            #             m = f"319: on_startup failed for {hierarchical_key}_{hook_name}: {e}"
            #             # logger.error(m)
            #             logger.info(m)


            # --- Metadaten  ---
            injection_data = {
                'source_modname': modname
            }
            if is_private:
                injection_data['is_private'] = True
            # -----------------------------

            if hasattr(module, 'PUNCTUATION_MAP'):

                if is_private:
                    m = (f"⚠️ 💥 🚨 🛑 SECURITY WARNING: Found 'PUNCTUATION_MAP' in 🔑 private module '{modname}' "
                         f"Punctuation maps do NOT support privacy masking! "
                         f"Entries from this map will be logged in plain text. "
                         f"Please move sensitive rules to 'FUZZY_MAP'.")
                    logger.info(m)
                    logger.warning(m)
                    print(m)

                punctuation_map.update(module.PUNCTUATION_MAP)


            if hasattr(module, 'FUZZY_MAP_pre'):

                if is_private:
                    for entry in module.FUZZY_MAP_pre:
                        # Annahme: entry ist entweder Dict oder Tupel mit Dict am Ende
                        if isinstance(entry, dict):
                            entry.update(injection_data)
                        elif isinstance(entry, (list, tuple)) and len(entry) > 0:
                            last_item = entry[-1]
                            if isinstance(last_item, dict):
                                last_item.update(injection_data)

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

                        if is_private:
                            standardized_map.append(item + (injection_data.copy(),))
                        else:
                            standardized_map.append(item + ({},))

                    elif item_len == 4:

                        if is_private:
                            options_dict = item[3]
                            options_dict.update(injection_data)

                        standardized_map.append(item)

                    else:
                        logger.error(f"warning: FUZZY_MAP-length: ({item_len}): {item}",
                                     file=sys.stderr)

                fuzzy_map.extend(standardized_map)

                # 3. Extend the main fuzzy_map with the standardized rules
                # fuzzy_map.extend(standardized_map)

        except Exception as e:

            # scripts/py/func/process_text_in_background.py:506
            file_path = None
            spec = importer.find_spec(modname)
            if spec and spec.origin:
                file_path = spec.origin

            if 'file_path' in locals() and try_auto_fix_module(file_path, e, logger):
                logger.info("🔧 Auto-Fix in Background-Loop finished! try Reload...")
                try:
                    importlib.invalidate_caches()
                    # Hier musst du schauen, wie das Modul im Original geladen wurde
                    # Meistens so:
                    module = importlib.import_module(modname)
                    importlib.reload(module)

                    # Wenn wir hier sind, hat es geklappt!
                    # Je nach Logik musst du das Modul jetzt vielleicht zur Liste hinzufügen
                    # oder einfach 'continue' machen, damit der nächste Loop-Durchlauf es sauber lädt.
                    logger.info("✅ Modul repaired. ")

                    if platform.system() == "Windows":
                        windows_apply_correction_with_sync()

                    continue

                except Exception as retry_err:
                    logger.error(f"❌ Reload gescheitert: {retry_err}")
                    logger.info(f"❌ Reload gescheitert: {retry_err}")
                    log4DEV(f"❌ Reload gescheitert: {retry_err}",logger)
            # --- AUTO-FIX ENDE ---



    if settings.show_PLUGINS_ENABLED:
        enabled_modname_str = '▉'.join(ENABLED_modname_list)
        logger.info(f"🗺️ ENABLED: ▉{enabled_modname_str}▉")
    # englisch einschalten Hallo wie geht'senglisch einschaltenHallo wie geht's

    logger.info(f"🗺️ Map loading complete. Found {len(fuzzy_map_pre)} FUZZY_MAP_pre rules.")

    if getattr(settings, "DEV_MODE_memory", False):
        from scripts.py.func.log_memory_details import log_memory_details
        log_memory_details(f"next: return punctuation_map, fuzzy_map_pre, fuzzy_map", logger)

    # process_text_in_background.py:502 (load_maps_for_language)
    return punctuation_map, fuzzy_map_pre, fuzzy_map



# Helper to check if a string contains regex special characters
def is_regex_pattern(pattern):
    # This is a simple heuristic. You can add more characters if needed.
    return any(char in pattern for char in r'^$*+?{}[]\|()")')


def apply_fuzzy_replacement_logic(processed_text, replacement, threshold, logger):
    # is called in apply_all_rules_may_until_stable(

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

                    # scripts/py/func/process_text_in_background.py:560 (apply_fuzzy_replacement_logic)
                    # angefangen noch ganz ohne funtion <=================================================
                    # is_private = "/_" in source_path or "\\_" in source_path

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
    new_processed_text, full_text_replaced_by_rule, skip_list, privacy_taint_occurred = apply_all_rules_until_stable(
        processed_text
        , fuzzy_map_pre
        , logger)
    #made_a_change_in_cycle = None

    #log_all_processed_text = False and settings.DEV_MODE

    is_private = False
    if privacy_taint_occurred:
        is_private = True

    if GLOBAL_debug_skip_list:

        print(f'567: skip_list={skip_list}')

    a_rule_matched = False
    if new_processed_text is False:
        #made_a_change_in_cycle = False
        log4DEV(f"new_processed_text is return ... None", logger)

        if GLOBAL_debug_skip_list:
            print(f'574: skip_list={skip_list}')

        return new_processed_text, None, skip_list, privacy_taint_occurred


    if full_text_replaced_by_rule:
        # source_modname = options_dict.get('source_modname', '')

        log4DEV("full_text_replaced_by_rule --> skip_list.append('LanguageTool')", logger)
        skip_list.append('LanguageTool')
        # regex_pre_is_replacing_all_maybeTEST1 = True
        log4DEV(f"242: 🔁??? new_processed_text: {new_processed_text}", logger)

        if GLOBAL_debug_skip_list:
            print(f'585: skip_list={skip_list} | {new_processed_text} ')

        return new_processed_text, True, skip_list, privacy_taint_occurred

    log4DEV(f"new_processed_text: {new_processed_text},  "
        f"skip_list:{skip_list} ,  full_text_replaced_by_rule: '{full_text_replaced_by_rule}'   ",logger)

    # if regex_pre_is_replacing_all_maybe:
    #     regex_match_found_prev = True  # need to be then also true for historical reasons. to be compatible to rest of the code
    log4DEV(f"skip_list={skip_list} 🔁🔁🔁🔁🔁 full_text_replaced_by_rule: '{full_text_replaced_by_rule}' ",logger)

    if new_processed_text:
        processed_text = new_processed_text
        log4DEV(f"251: 🔁🔁🔁🔁🔁 full_text_replaced_by_rule: '{full_text_replaced_by_rule}' ", logger)
    else:
        # scripts/py/func/process_text_in_background.py:248 (apply_all_rules_may_until_stable)
        #for replacement, match_phrase, threshold, *flags_list, rule_mode in fuzzy_map_pre:

        for entry in fuzzy_map_pre:


            if len(entry) < 4:
                entry =normalize_fuzzy_map_rule_entry(entry)



            replacement, match_phrase, threshold, options_dict = entry

            # 1. Try to determine privacy from options
            # Assuming 'options_dict' is defined earlier in the loop (it usually is)
            source_modname = options_dict.get('source_modname', '')

            if options_dict.get('is_private'):
                # Best case: The loader already flagged it
                is_private = True
            elif "/_" in str(source_modname) or "\\_" in str(source_modname):
                # Fallback: Check path string
                is_private = True

            # Track global taint for this function execution

                # ... (Jetzt kommt dein if is_private: Block) ...
            # for replacement, match_phrase, threshold, options_dict in fuzzy_map_pre:

            # logger.info(f"252: 🔁??? threshold: '{threshold}' based on pattern '{match_phrase}'")

            flags = options_dict.get('flags', 0)  # Hier extrahierst du den INTEGER korrekt
            
            
            skip_list = options_dict.get('skip_list', [])

            if GLOBAL_debug_skip_list:
                print(f'618: skip_list={skip_list}')

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
                    # logger.info(
                    #     f"🔁 455: Regex_pre in: '{processed_text}' --> '{replacement}' based on pattern '{match_phrase}'")

                    # Die Ersetzung bleibt genau gleich
                    new_text = re.sub(
                        match_phrase,
                        replacement.strip(),
                        processed_text,
                        flags=flags
                    )
                    # logger.info(
                    # f"🔁 464: '{new_text}'")

                    # Hier wird es interessant: Wir behalten den alten und den neuen Text für die Skripte

                    original_text_before_rule = processed_text
                    log4DEV(f'original_text_before_rule = processed_text ===> {original_text_before_rule}',logger)
                    log4DEV(f'original_text_before_rule = processed_text ===> {original_text_before_rule} <- {processed_text}',logger)

                    if new_text != original_text_before_rule:


                        if is_private:
                            logger.info(
                                f"apply_all_rules_may_until_stable -> 470: 🚀Regex_pre: '***' -> '***' (Pattern: '{match_phrase}')")
                            processed_text = new_text
                        else:
                            logger.info(
                                f"apply_all_rules_may_until_stable -> 470: 🚀Regex_pre: '{processed_text}' -> '{new_text}' (Pattern: '{match_phrase}')")
                            processed_text = new_text
                    else:
                        log4DEV(
                            f"not changed: '{processed_text}' ???? '{new_text}' (Pattern: '{match_phrase}')",logger)
                        processed_text = new_text # its a bit strange to replace same with same. but anyhow it should possible (4.12.'25 13:46 Thu)


                    a_rule_matched = True

                    if is_private:
                        privacy_taint_occurred = True

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

                            if GLOBAL_debug_skip_list:
                                print(f'708: skip_list={skip_list}')

                            # return processed_text, a_rule_matched, skip_list # in
                            return processed_text, a_rule_matched, skip_list, privacy_taint_occurred

                    log4DEV(f"a_rule_matched({a_rule_matched}) -> break",logger)
                    break  # Found a definitive match, stop this loop
            except re.error as e:
                logger.warning(f"Invalid regex_pre pattern in FUZZY_MAP_pre: '{match_phrase}'. Error: {e}")
                continue  # Skip this invalid rule

            if not current_rule_matched:
                # logger.info(f"310: new: new_processed_text={new_processed_text}, threshold={threshold} , a_rule_matched={a_rule_matched}")
                # , is in # file config/languagetool_server/PUNCTUATION_MAP.py
                if type(new_processed_text) is int and new_processed_text == 0:
                    # if log_all_processed_text:
                    log4DEV(f'TODO: what to do here? new_processed_text={new_processed_text}',logger)
                    # new_processed_text = ''
                new_processed_text = apply_fuzzy_replacement_logic(new_processed_text, replacement, threshold, logger)
                log4DEV(f"new: new_processed_text={new_processed_text} , threshold={threshold} , a_rule_matched={a_rule_matched}",logger)


    log4DEV(f"new_processed_text: {new_processed_text} , a_rule_matched: {a_rule_matched}, skip_list: {skip_list}",logger)

    if GLOBAL_debug_skip_list:
        print(f'731: skip_list={skip_list}')
    return new_processed_text, a_rule_matched, skip_list, privacy_taint_occurred

def process_text_in_background(logger,
        LT_LANGUAGE,
        raw_text,
        TMP_DIR,
        recording_time,
        active_lt_url,
        output_dir_override = None,
        chunk_id: int = 0,
        session_id: int = 0,
        unmasked = False
        ):
    # scripts/py/func/process_text_in_background.py:588 (process_text_in_background)

    RUN_MODE = os.getenv('RUN_MODE')
    global settings
    global _active_window_title

    # required_windows = cmd_config['only_in_windows']
    # required_windows = 'dummy'

    # clipboard_text_linux = get_clipboard_text_linux()

    # scripts/py/func/process_text_in_background.py:782 (process_text_in_background)
    # start = time.time()
    _active_window_title = get_active_window_title_safe()
    # end = time.time()
    # duration = end - start # its about 3milliSeconds
    if settings.DEV_MODE:
        print(f"window_title: 🔵{_active_window_title} ")

    # start = time.time()
    # wt = get_active_window_title_safe()
    # end = time.time()
    # duration = end - start
    # print(f"DISPLAY wt: {wt} duration: {duration} clipboard: {c}")

    privacy_taint_occurred = False

    if RUN_MODE == "API_SERVICE" and unmasked is True:
        run_mode_override = "API_SERVICE_local"
        logger.info(f"616: temporary run_mode_override={run_mode_override} (unmasked request).")
    else:
        run_mode_override = RUN_MODE

        # if getattr(settings, "DEV_MODE_all_processing", False):
        if getattr(settings, "DEV_MODE_all_processing", False):
            logger.info(f"📍run_mode_override={run_mode_override}.")


        # --- KRITISCHE SEQUENZPRÜFUNG AM ANFANG DER FUNKTION ---
    if chunk_id > 0:

        # 1. Warte-Loop, um die Reihenfolge zu garantieren
        while True:
            expected_id = 0
            with SEQUENCE_LOCK:
                expected_id = SESSION_LAST_PROCESSED.get(session_id, 0) + 1

            if chunk_id == expected_id:
                # Wir sind dran!
                break

            if chunk_id < expected_id:
                # Wurde bereits verarbeitet/überholt (oder wir sind ein Duplikat). Abbrechen!
                logger.warning(f"ID {chunk_id} skipped. Already processed up to {expected_id - 1}.")
                return

                # Wir sind zu schnell. In den Cache legen und warten.
            logger.info(f"ID {chunk_id} arrived early. Waiting for {expected_id}...")

            # --- CACHE: Legt uns in den Warte-Cache und wartet auf andere Threads, die abarbeiten ---
            with SEQUENCE_LOCK:
                if chunk_id not in OUT_OF_ORDER_CACHE:
                    OUT_OF_ORDER_CACHE[chunk_id] = (logger, LT_LANGUAGE, raw_text, TMP_DIR, recording_time,
                                                    active_lt_url, output_dir_override)

            # Kurze, effiziente Wartezeit, um den Thread freizugeben
            time.sleep(0.005)

            # --- Wenn der Cache-Eintrag nicht mehr da ist, wurde er von einem anderen Thread abgeholt ---
            if chunk_id not in OUT_OF_ORDER_CACHE:
                # Der Chunk wurde gerade von einem anderen Thread freigegeben, also neu prüfen.
                continue

                # 2. Erfolgreich an der Reihe: Aktualisiere die letzte verarbeitete ID
        with SEQUENCE_LOCK:
            SESSION_LAST_PROCESSED[session_id] = chunk_id

        # 3. Cache prüfen: Nachdem wir verarbeitet wurden, prüfen, ob wir Blocker für andere waren
        # Hier müsste ein weiterer Block hin, der den Cache aufräumt. (Wir implementieren das später)

    # --- ENDE DER SEQUENZPRÜFUNG ---


    global GLOBAL_PUNCTUATION_MAP, GLOBAL_FUZZY_MAP_PRE, GLOBAL_FUZZY_MAP

    # scripts/py/func/process_text_in_background.py:167 (process_text_in_background)
    new_punctuation, new_fuzzy_pre, new_fuzzy = load_maps_for_language(LT_LANGUAGE, logger,run_mode_override)

    if getattr(settings, "DEV_MODE_all_processing", False):
        logger.info(f"📍new_punctuation={new_punctuation}")
        log4DEV(f"📍new_punctuation={new_punctuation}",logger)

    GLOBAL_PUNCTUATION_MAP = new_punctuation
    GLOBAL_FUZZY_MAP_PRE = new_fuzzy_pre
    GLOBAL_FUZZY_MAP = new_fuzzy

    new_processed_text = ''
    skip_list=[]
    options_dict = None
    log4DEV(f"skip_list: {skip_list}", logger)

    settings = DynamicSettings()

    timestamp = int(time.time() * 1000)
    if output_dir_override:
        unique_output_file = output_dir_override / f"tts_output_{timestamp}.txt"
    else:
        unique_output_file = TMP_DIR / f"sl5_aura/tts_output_{timestamp}.txt"

    if settings.DEV_MODE: # some test. want check if we can change setting and get some setting correct back ( 2026-0104-1433 4.1.'26 14:33 Sun )
        timestamp = int(time.time() * 1000)

        if output_dir_override:
            # unique_output_file = f"{output_dir_override}/tts_output_{timestamp}.txt"
            unique_output_file = output_dir_override / f"tts_output_{timestamp}.txt"
        else:
            unique_output_file = TMP_DIR / f"sl5_aura/tts_output_{timestamp}.txt"

        if not privacy_taint_occurred:
            log4DEV(f'raw_text:{raw_text}',logger)
        if raw_text == '->SPEECH_PAUSE_TIMEOUT<-':
            if not privacy_taint_occurred:

                log4DEV(f'raw_text:{raw_text}',logger)
            raw_text = settings.SPEECH_PAUSE_TIMEOUT
            unique_output_file.write_text(f'{str(raw_text)}', encoding="utf-8-sig")
            return raw_text
        if raw_text == '->AUDIO_INPUT_DEVICE<-':
            if not privacy_taint_occurred:

                log4DEV(f'raw_text:{raw_text}',logger)
            raw_text = settings.AUDIO_INPUT_DEVICE
            unique_output_file.write_text(f'{str(raw_text)}', encoding="utf-8-sig")
            return raw_text





    try:

        # if settings.DEV_MODE:
        #     logger.info(f"start sanitize_transcription_start")
        raw_text = sanitize_transcription_start(raw_text)
        # if settings.DEV_MODE:
        #     logger.info(f"end sanitize_transcription_start")


        # ZWNBSP

        # DEV_MODE_all_processing = settings.DEV_MODE and True
        if not privacy_taint_occurred:

            log4DEV(f"THREAD: Starting processing for: '{raw_text}'", logger)

        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")


        lang_code_predictions = ''

        # log4DEV(f"process_text_in_background.py:850 (process_text_in_background) raw_text:{raw_text}", logger)

        if len(raw_text) > 0:
            try:
                if LT_LANGUAGE == 'en-US':
                    threshold = 0.50  # Low threshold: switch even if not 100% sure it's German
                else:
                    threshold=0.60
                predictions = None
                if settings.ENABLE_AUTO_LANGUAGE_DETECTION:
                    if not privacy_taint_occurred:

                        logger.info(f"👀👀👀 Start lang_code predictions for: '{raw_text}'")
                    # predictions = fasttext_model.predict(raw_text, threshold=threshold)

                if predictions:
                    logger.info(
                        f"---------------------------> predictions: {predictions} , LT_LANGUAGE: {LT_LANGUAGE}")
                    if predictions[0] and predictions[0][0]:
                        lang_code_predictions = predictions[0][0].replace('__label__', '')
                        # logger.info(f"Raw prediction object: {predictions}")

                        if not privacy_taint_occurred:

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

        # scripts/py/func/process_text_in_background.py:898 (process_text_in_background)
        normalize_punctuation_changed = False
        is_only_number = False
        if not privacy_taint_occurred:

            log4DEV(f"process_text_in_background.py:900 (process_text_in_background) raw_text:{raw_text}", logger)
        processed_text, was_exact_match = normalize_punctuation(raw_text, GLOBAL_PUNCTUATION_MAP, logger)
        # if len(processed_text) != len(raw_text):
        if processed_text != raw_text:
            normalize_punctuation_changed = True
            new_processed_text = processed_text
            if not privacy_taint_occurred:

                log4DEV(f"process_text_in_background.py:426 (process_text_in_background) processed_text:{processed_text} ?? normalize_punctuation_changed_size:{normalize_punctuation_changed}", logger)

        if normalize_punctuation_changed:
            processed_text = re.sub(r'(?<=\d)\s+(?=\d)', '', processed_text)

            is_only_number =  processed_text.isdigit()

        # scripts/py/func/process_text_in_background.py

        #regex_pre_is_replacing_all = False
        regex_match_found_prev = False
        regex_pre_is_replacing_all_maybe = False
        result_languagetool = None

        if not privacy_taint_occurred:

            log4DEV(
                f"processed_text:'{processed_text}' new_processed_text:'{new_processed_text}'",logger)

        if not was_exact_match:

            regex_pre_is_replacing_all_maybeTEST1 = None

            if not privacy_taint_occurred:

                log4DEV(f"new_processed_text: {new_processed_text}"
                    f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe}"
                    f" normalize_punctuation_changed_size={normalize_punctuation_changed}"
                    f" regex_pre_is_replacing_all_maybeTEST1:{regex_pre_is_replacing_all_maybeTEST1}"
                    f" regex_match_found_prev:{regex_match_found_prev}",logger)


            if settings.default_mode_is_all:
                # if true call iteratively all rules

                if not privacy_taint_occurred:

                    log4DEV(f"Applying all rules until stable (default 'all' mode).", logger)
                (new_processed_text
                , regex_pre_is_replacing_all_maybe
                , skip_list, privacy_taint_occurred) = apply_all_rules_may_until_stable(processed_text
                , GLOBAL_FUZZY_MAP_PRE, logger)

                if not privacy_taint_occurred:

                    log4DEV(f"new_processed_text: {new_processed_text}"
                        f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe} "
                        f" skip_list={skip_list}",logger)


            regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe # and regex_match_found_prev

            if not privacy_taint_occurred:
                log4DEV(f"new_processed_text: {new_processed_text}"
                    f" regex_pre_is_replacing_all:{regex_pre_is_replacing_all} "
                    f" regex_pre_is_replacing_all_maybe:{regex_pre_is_replacing_all_maybe}"
                    f" normalize_punctuation_changed_size={normalize_punctuation_changed}"
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

            if not privacy_taint_occurred:

                log4DEV(f"if ({not regex_pre_is_replacing_all}"
                    f" and not {is_only_number}"
                    f" and 📚📚'LanguageTool'📚📚 not in SkipList:{skip_list} "
                    f" and not ( ... {processed_text}",logger)

            # scripts/py/func/process_text_in_background.py:982 (process_text_in_background)
            if (not regex_pre_is_replacing_all and not is_only_number and 'LanguageTool' not in skip_list ):

                if new_processed_text ==0:
                    new_processed_text = processed_text

                if not privacy_taint_occurred:

                    log4DEV(f"and not 📚📚'LanguageTool'📚📚 in skip_list ==> {skip_list}"
                        f" processed_text:{processed_text}"
                        f" new_processed_text:{new_processed_text} ",logger)



                result_languagetool = correct_text_by_languagetool(
                    logger,
                    active_lt_url,
                    LT_LANGUAGE,
                    new_processed_text).lstrip('\uFEFF')



                if getattr(settings, "DEV_MODE_memory", False):
                    from scripts.py.func.log_memory_details import log_memory_details
                    log_memory_details(f"last correct_text_by_languagetool:", logger)


            # scripts/py/func/process_text_in_background.py:1080 (process_text_in_background)
            # Step 2: Slower, fuzzy replacements on the result
            # logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

            best_score = 0
            best_replacement = None


            # --- NEW HYBRID MATCHING LOGIC ---

            # Pass 1: Prioritize and check for exact REGEX matches first.
            # A regex match is considered definitive and will stop further processing.

            if not privacy_taint_occurred:

                log4DEV(f"SkipList: {skip_list} "
                        f" regex_pre_is_replacing_all:{regex_pre_is_replacing_all} "
                        f" processed_text:{processed_text} "
                        f" new_processed_text:{new_processed_text}"
                        f" 📚📚result_languagetool📚📚:{result_languagetool} ",logger)
            # 477: SkipList: ['LanguageTool'] regex_pre_is_replacing_all:True processed_text:git at new_processed_text:git add .

            regex_match_found = False
            log4DEV(f'regex_pre_is_replacing_all:{regex_pre_is_replacing_all} ',logger)
            log4DEV(f"skip_list: {skip_list}", logger)
            if GLOBAL_debug_skip_list:
                print(f'1051: skip_list={skip_list}')
            skip_list_backup = skip_list
            options_dict = None
            log4DEV(f"skip_list_backup: {skip_list_backup}", logger)
            if not regex_pre_is_replacing_all and not is_only_number:
                log4DEV(f'in fuzzy_map: regex_pre_is_replacing_all:{regex_pre_is_replacing_all} ',logger)
                for replacement, match_phrase, threshold, options_dict in GLOBAL_FUZZY_MAP:

                    if not privacy_taint_occurred:
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
                    if GLOBAL_debug_skip_list:
                        print(f'1070: skip_list={skip_list}')
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
                        if not privacy_taint_occurred:
                            log4DEV(f"re.search({match_phrase}, {result_languagetool}..):",logger)

                        try:
                            log4DEV(f"DEBUG FUZZY: Starting fuzzy loop with text: '{processed_text}'", logger)

                            if result_languagetool is None:
                                log4DEV("Skipping regex matching because result_languagetool is None.", logger)
                                continue

                            if not re.search(match_phrase, result_languagetool, flags=flags):
                                continue
                            if not privacy_taint_occurred:
                                log4DEV(f"🔁Regex in: '{result_languagetool}' --> '{replacement}' based on pattern '{match_phrase}'",logger)

                            new_text = re.sub(
                                match_phrase,
                                replacement.strip(),
                                result_languagetool,
                                flags=flags
                            )

                            if new_text != result_languagetool:
                                if not privacy_taint_occurred:
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

                if not privacy_taint_occurred:
                    log4DEV(f"No regex match. Proceeding to fuzzy search for: '{processed_text}'",logger)
                best_score = 0
                best_replacement = None

                log4DEV(f"skip_list_backup: {skip_list_backup}", logger)
                skip_list=skip_list_backup
                if GLOBAL_debug_skip_list:
                    print(f'1132: skip_list={skip_list}')

                # for replacement, match_phrase, threshold in fuzzy_map:
                for replacement, match_phrase, threshold, *_ in GLOBAL_FUZZY_MAP:
                    # Skip regex patterns in this pass
                    if is_regex_pattern(match_phrase):
                        continue

                    score = fuzz.token_set_ratio(processed_text.lower(), match_phrase.lower())

                    # DEBUG:
                    if "marmela" in match_phrase.lower():
                        log4DEV(
                            f"DEBUG FUZZY CHECK: Input='{processed_text}' vs Rule='{match_phrase}' -> Score={score} (Threshold={threshold})",
                            logger)

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

        if not privacy_taint_occurred:
            log4DEV(
                f"SkipList:{skip_list} "
                f" processed_text:{processed_text} "
                f" new_processed_text:{new_processed_text}"
                f" result_languagetool:{result_languagetool} ",logger)
        # SkipList: ['LanguageTool'] regex_pre_is_replacing_all:True processed_text:git at new_processed_text:git add .
        # SkipList:[]  processed_text: mit nachnamen Lauffer  new_processed_text:False result_languagetool:Mit Nachnamen lauf er



        if not new_processed_text:
            if not privacy_taint_occurred:
                log4DEV(f"Empty results are allowed not |||  SkipList:{skip_list}"
                    f" new_processed_text:{new_processed_text}"
                    f" result_languagetool:{result_languagetool}"
                    f" processed_text:{processed_text} ",logger)

        if (new_processed_text and new_processed_text != '0' and new_processed_text is not None) and new_processed_text != processed_text:
            if not privacy_taint_occurred:
                log4DEV(f'new_processed_text != processed_text | {new_processed_text} != {processed_text} ==> processed_text = new_processed_text',logger)
            processed_text = new_processed_text

            # unique_output_file = TMP_DIR / f"sl5_aura/tts_output_{timestamp}.txt"
            # unique_output_file.write_text(processed_text)

            if not privacy_taint_occurred:
                log4DEV(f"SkipList:{skip_list}"
                    f" new_processed_text:{new_processed_text}"
                    f" result_languagetool:{result_languagetool}"
                    f" processed_text:{processed_text} ",logger)

            #processed_text = (result_languagetool) ? result_languagetool : processed_text


            # log4DEV(f'{result_languagetool} {processed_text}', logger)

            # her now fixed at 4.12.'25 15:55 Thu 'Null'->0 replacement was not recognized correctly:
            # All 88tested of 97 tests(all lang) passed! Great no test failed
            # 15:55:30,922 - INFO     - ----------------------------------------
            # 15:55:30,922 - INFO     - ⌚ self_test_readable_duration: 0:00:37.181278
        processed_text = result_languagetool if result_languagetool else new_processed_text if new_processed_text else processed_text

        if not privacy_taint_occurred:
            log4DEV(f"SkipList:{skip_list}"
                f" new_processed_text:{new_processed_text}"
                f" result_languagetool:{result_languagetool}"
                f" processed_text:{processed_text} ",logger)


        script_result = processed_text  # Wir starten mit dem Originaltext

        # new_current_text wird das finale Ergebnis sein

        if not privacy_taint_occurred:
            log4DEV(f'processed_text={processed_text}', logger)
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

        # scripts/py/func/process_text_in_background.py:1440
        if new_current_text:

            # scripts/py/func/process_text_in_background.py:1443
            if options_dict: # If it exists, no sub-module will be output. they have may its own signature.
                # e.g. the translating modules have their own signature
                log4DEV(f"options_dict={options_dict}",logger)

                # scripts/py/func/process_text_in_background.py:1448


                if hasattr(settings, 'SIGNATURE_MAPPING'):
                    if type(new_current_text) is str and len(new_current_text) >= 11:

                        current_time = time.time()
                        active_sig = ""
                        active_cooldown = 3600  # Globaler Fallback

                        # 1. Finde das passende Pattern
                        for pattern, config in settings.SIGNATURE_MAPPING.items():
                            if re.search(pattern, str(_active_window_title), re.IGNORECASE):
                                active_sig, active_cooldown = config
                                break

                        # if active_sig == active_sig_default:
                        log4DEV(f'🔵 window_title: {_active_window_title}',logger)


                        if active_sig:
                            with SEQUENCE_LOCK:
                                # 2. Nutze den spezifischen Cooldown für dieses Fenster
                                last_time = SIGNATURE_TIMES.get(_active_window_title, 0)

                                if (current_time - last_time > active_cooldown):
                                    new_current_text += f"{active_sig}"
                                    SIGNATURE_TIMES[_active_window_title] = current_time




                if False and hasattr(settings, 'SIGNATURE_MAPPING'):
                    if type(new_current_text) is str and len(new_current_text) >= 11:

                        # 1. Bestimme die richtige Signatur basierend auf dem Fenster
                        active_sig_default = settings.SIGNATURE_MAPPING.get("DEFAULT", "")
                        active_sig = active_sig_default

                        for pattern, sig in settings.SIGNATURE_MAPPING.items():
                            if re.search(pattern, str(_active_window_title), re.IGNORECASE):
                                active_sig = sig
                                break




                        if active_sig == active_sig_default:
                            log4DEV(f'🔵 window_title: {_active_window_title}',logger)

                        # for app_name, sig in settings.SIGNATURE_MAPPING.items():
                        #     if app_name in _active_window_title:  # Sucht nach "0 A.D." im Titel
                        #         active_sig = sig
                        #         break

                        if active_sig:
                            signature_cooldown = getattr(settings, 'SIGNATURE_COOLDOWN', 3600)

                            with SEQUENCE_LOCK:
                                last_time = SIGNATURE_TIMES.get(_active_window_title, 0)
                                current_time = time.time()

                                if (current_time - last_time > signature_cooldown):
                                    new_current_text += f" {active_sig}"
                                    SIGNATURE_TIMES[_active_window_title] = current_time

                if False and hasattr(settings, 'signatur1'):

                    if len(new_current_text) >= 11:

                        current_time = time.time()

                        if not hasattr(process_text_in_background, "last_signature_times"):
                            process_text_in_background.last_signature_times = {}

                        last_times = process_text_in_background.last_signature_times
                        last_time = last_times.get(_active_window_title, 0)

                        signature_cooldown = getattr(settings, 'SIGNATURE_COOLDOWN', 3600)

                        with SEQUENCE_LOCK:
                            last_time = SIGNATURE_TIMES.get(_active_window_title, 0)
                            current_time = time.time()

                            if (current_time - last_time > signature_cooldown):

                                if type(new_current_text) is str:
                                    new_current_text += f"{settings.signatur1}"

                                    SIGNATURE_TIMES[_active_window_title] = current_time

                                    # last_signature_times[_active_window_title] = current_time
                                    # process_text_in_background.last_signature_times[_active_window_title] = current_time



            new_current_text = sanitize_transcription_start(new_current_text)



            # DIESE ZEILE WAR SCHON RICHTIG:
            unique_output_file.write_text(new_current_text, encoding="utf-8-sig")

            # KORREKTUR 1: Verwende die NEUEN Variablen für den Fallback
            handle_tts_fallback(new_current_text, lang_for_tts, logger)
            if not privacy_taint_occurred:
                log4DEV(f"handle_tts_fallback({new_current_text}, {lang_for_tts})",logger)

            # KORREKTUR 2: Logge den Text, der WIRKLICH geschrieben wurde

            # process_text_in_background.py:1453 (process_text_in_background)
            if privacy_taint_occurred:
                logger.info(f"✅ THREAD: Successfully wrote to {unique_output_file} '***'")
            else:
                logger.info(f"✅ THREAD: Successfully wrote to {unique_output_file} '{new_current_text}'")

        else:
            logger.warning("Nach der Plugin-Verarbeitung gab es keinen Text zum Ausgeben.")
            log4DEV("new_current_text={new_current_text} . Nach der Plugin-Verarbeitung gab es keinen Text zum Ausgeben.",logger)


        # notify("Transcribed", duration=700, urgency="low")

        notify("Transcribed", "", "low", duration=1000, replace_tag="transcription_status")

    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        logger.error(f"scripts/py/func/process_text_in_background.py:1167  (process_text_in_background)")
        notify(f"FATAL: Error in processing thread", duration=4000, urgency="low")
    finally:
        # file: scripts/py/func/process_text_in_background.py
        if settings.DEV_MODE:
            if not privacy_taint_occurred:
                log4DEV(f"✅ Background processing for '{raw_text[:20]}...' finished. ",logger)
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

        auto_reload_modified_maps(logger,run_mode_override)


# Hallo des Hallo Test

# py/func/process_text_in_background.py:1196
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
    # scripts/py/func/process_text_in_background.py:900 (handle_tts_fallback)
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
        logger.warning("primary 🗣️ TTS failed. try 🗣️ Espeak-Fallback...")
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
    privacy_taint_occurred = False

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

            if GLOBAL_debug_skip_list:
                print(f'1420: Processing rule {rule_entry}')



            # (replacement_text, regex_pattern, threshold_value, options_dict)

            # SAFETY GUARD: Skip invalid entries that are not tuples/lists
            if not isinstance(rule_entry, (tuple, list)):
                # scripts/py/func/process_text_in_background.py:1634 (apply_all_rules_until_stable)
                if not privacy_taint_occurred:
                    m = f"🚨 INVALID RULE ENTRY found while working on rule text=📃{text}📄 "\
                        f"Type {type(rule_entry)}): {rule_entry}. Please check your map files!"
                    log4DEV(m,logger_instance)
                    logger_instance.info(m)

                if GLOBAL_debug_skip_list:
                    print(f'1433: Processing rule {rule_entry} ')

                continue

            if len(rule_entry) < 4:
                rule_entry = normalize_fuzzy_map_rule_entry(rule_entry)


            if len(rule_entry) != 4:
                print(f"____________________________________________")
                print(f"____________________________________________")
                print(f"____________________________________________")
                print(f"DEBUG: Broken rule found: {rule_entry}")
                logger_instance.info(f"DEBUG: Broken rule found: {rule_entry}")
                log4DEV(f"DEBUG: Broken rule found: {rule_entry}",logger_instance)
                print(f"____________________________________________")
                print(f"____________________________________________")
                print(f"____________________________________________")
                time.sleep(3)
                return None, False
                # sys.exit(1)

            # 🔵

            # scripts/py/func/process_text_in_background.py -> apply_all_rules_until_stable :1471
            replacement_text, regex_pattern, threshold, options_dict = rule_entry

            if regex_pattern in [r'.+', r'.*', r'^.+$', r'^.*$']:
                source_modname = options_dict.get('source_modname', '')
                m = (f"🚨 WARNING: Dangerous Catch-all '{regex_pattern}' found in {source_modname}"
                     f" =>will skip LanguageTool because not needed")
                log4DEV(m, logger_instance)
                logger_instance.info(m)

            skip_list_temp = options_dict.get('skip_list', [])

            # source_modname = options_dict.get('source_modname', '')

            # process_text_in_background.py:1669 (apply_all_rules_until_stable)

            # 1. Check Metadata from Injection (Primary Source)
            # scripts/py/func/process_text_in_background.py:1676 (apply_all_rules_until_stable)
            rule_is_private = options_dict.get('is_private', False)

            # 2. Safety Fallback: Check Source Path if metadata is missing/False
            # (Only needed if rule_is_private is False)
            if not rule_is_private:
                # get path, when exist
                src = str(options_dict.get('source_modname', ''))  # oder 'source_path' je nach Benennung
                if "/_" in src or "\\_" in src:
                    rule_is_private = True

            # 3. Update Global Taint (Sticky)

            # 4. Logging (Simplified)
            # if rule_is_private:
                # if settings.DEV_MODE:
                #    logger_instance.info(f"🔒 Apply Private Rule (Source: ...)")


            only_in_windows_list = options_dict.get('only_in_windows', [])
            skip_this_regex_pattern = False
            # global _active_window_title

            # if settings.DEV_MODE:
            #     print(f"def process_text_in_background -> _active_window_title: {_active_window_title} ")

            if only_in_windows_list and _active_window_title:
                show_debug_prints = False

                m_202601180206=f"🔵 window_title: {_active_window_title} ◀️ {regex_pattern[0:72]} …"
                # log4DEV(m,logger_instance)
                # logger_instance.info(m_202601180206)

                if show_debug_prints:
                    print(f' ▶️{only_in_windows_list}◀️ , '
                          f'{m_202601180206}️ ')

                if any(re.search(pattern, str(_active_window_title)) for pattern in only_in_windows_list):
                    skip_this_regex_pattern = False

                    if show_debug_prints:
                        logger_instance.info(f'window title matched: 🥳 {m_202601180206}')

                # for pattern in only_in_windows_list:
                #     if show_debug_prints:
                #         print(f'????? pattern="{pattern} ..."')
                #         print(f'????? {active_window_title}')
                #     if re.search(pattern, str(active_window_title)):
                #         if show_debug_prints:
                #             print(f'🔎 🥳 matched: pattern="{pattern}... its okay use it"')
                #         skip_this_regex_pattern = False
                #         continue
                else:
                    # if show_debug_prints:
                    # print('🔎 👎 not matched: pattern="{pattern}... dont use it -> skip this rule"')
                    skip_this_regex_pattern = True


            if skip_this_regex_pattern:
                continue

            if GLOBAL_debug_skip_list:
                print(f'1476: skip_list_temp={skip_list_temp}')
                print(f'1476: skip_list_temp={options_dict}')

            # 1. Flags extrahieren für den Cache-Key
            flags = options_dict.get('flags', re.IGNORECASE)
            cache_key = (regex_pattern, flags)

            # 2. Cache-Check oder Kompilierung
            if cache_key not in REGEX_COMPILE_CACHE:
                try:
                    REGEX_COMPILE_CACHE[cache_key] = re.compile(regex_pattern, flags=flags)
                except re.error as e:
                    logger_instance.error(f"Invalid regex: {regex_pattern} - {e}")
                    continue

            compiled_regex = REGEX_COMPILE_CACHE[cache_key]

            # 3. Nutzung des kompilierte Objekts (viel schneller!)
            try:
                match_obj = compiled_regex.fullmatch(current_text)

                if match_obj:
                    # Der ursprüngliche Text, bevor irgendetwas geändert wird
                    original_text_for_script = current_text
                    # print(f"1571:🔎 🔎 🔎 original..={original_text_for_script} current_text={current_text}")
                    if not privacy_taint_occurred:
                        log4DEV(f"original..={original_text_for_script}", logger_instance)

                    new_current_text = compiled_regex.sub(replacement_text, current_text)
                    if not privacy_taint_occurred:
                        log4DEV(f"new..={new_current_text}", logger_instance)
                    # log4DEV(f"regex_pattern:{regex_pattern}, sub_replacement_string={sub_replacement_string}", logger_instance)

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

                        if not privacy_taint_occurred:
                            log4DEV(f"new..:'{new_current_text}' != original..:'{original_text_for_script}'",logging)

                        made_a_change_in_cycle = True

                        # scripts/py/func/process_text_in_background.py:1799 (apply_all_rules_until_stable)
                        privacy_taint_occurred = True

                        made_a_change = made_a_change + 1
                        skip_list = skip_list_temp

                        if GLOBAL_debug_skip_list:
                            print(f'1525: skip_list={skip_list}')

                        current_text = new_current_text  # Jetzt wird der finale Text zugewiesen

                        full_text_replaced_by_rule = True  # because was full-match
                        log4DEV(f"full_text_replaced_by_rule = {full_text_replaced_by_rule}",logger_instance)

                        if not privacy_taint_occurred:
                            log4DEV(f"🚀🚀 skip_list:{skip_list} 🚀🚀🚀819: made_a_change={made_a_change} '{original_text_for_script}' ----> '{current_text}' (Pattern: '{regex_pattern}') Iterative-All-Rules FULL_REPLACE:{full_text_replaced_by_rule}",logger_instance)

                        if GLOBAL_debug_skip_list:
                            print(f'1534: skip_list={skip_list}')

                        if 'fullMatchStop' not in skip_list:
                            break

                else:  # Dieser Block wird ausgeführt, wenn es KEIN fullmatch gab

                    # <<< ÄNDERUNG 3: Wir müssen hier explizit nach einem partiellen Match suchen, um das match_obj zu bekommen
                    # partial_match_obj = re.search(regex_pattern, current_text, flags=flags)
                    partial_match_obj = compiled_regex.search(current_text)

                    if partial_match_obj:
                        original_text_for_script = current_text

                        new_current_text = compiled_regex.sub(replacement_text, current_text)


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
                            if not privacy_taint_occurred:
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
        if not privacy_taint_occurred:
            log4DEV(f"made_a_change={made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",logger_instance)
            #  z.b. "das ist ein test landet" hier. Es gibt auch (höchstwahrschienlich keine Regel hiervür. Also correkt.
            # logging.info('sys.exit(1) 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923')
            # sys.exit(1) # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 # 2025-1016-1923 Test
            log4DEV(f"🚀🚀🚀skip_list:{skip_list} made_a_change:{made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",
                    logger_instance)
        return made_a_change, full_text_replaced_by_rule, skip_list, privacy_taint_occurred
        # log4DEV(f"🚀🚀🚀skip_list:{skip_list} made_a_change:{made_a_change} full_text_replaced_by_rule:{full_text_replaced_by_rule} current_text:{current_text}",logger_instance)
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
    if not privacy_taint_occurred:
        log4DEV(f"🚀🚀🚀skip_list:{skip_list} "
                f"regex_pattern={regex_pattern} made_a_change:{made_a_change} "
                f"full_text_replaced_by_rule:{full_text_replaced_by_rule} "
                f"current_text:{current_text}",logger_instance)
    # 17:08:56,492 - INFO     - 758: made_a_change=True full_text_replaced_by_rule:False current_text:mit nachnamen Lauffer

    return current_text, full_text_replaced_by_rule, skip_list, privacy_taint_occurred

#


# scripts/py/func/process_text_in_background.py:1282
def clear_global_maps(logger):
    """
    Clears all global map dictionaries to release references before a full reload.
    This prevents memory leaks from unreferenced old map functions.
    """
    # logger.info("Starting CLEAR of global Map Registries.")

    # CRITICAL FIX: Use 'global' to access the module-level variables for clearing.
    global GLOBAL_PUNCTUATION_MAP, GLOBAL_FUZZY_MAP_PRE, GLOBAL_FUZZY_MAP # noqa: F824

    # Clearing the dictionaries explicitly breaks the reference to old functions.
    GLOBAL_PUNCTUATION_MAP.clear()
    GLOBAL_FUZZY_MAP_PRE.clear()
    GLOBAL_FUZZY_MAP.clear()

    # logger.info("Global Map Registries successfully cleared.")





