# scripts/py/func/checks/self_tester.py

# TODO:
# 5.5.'26 21:32 Tue
#  https://github.com/sl5net/SL5-aura-service/issues/94

import re
import concurrent.futures
import shutil
import sys
# import concurrent.futures

import os
from pathlib import Path

# from .auto_zip_startup_test import run_auto_zip_sanity_check

from ..audio_manager import speak_inclusive_fallback
# from ..log_memory_details import log4DEV
from ..process_text_in_background import process_text_in_background

from enum import IntEnum
from .run_function_with_throttling import run_function_with_throttling

from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
TMP_DIR = tmp_dir
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


class TestPrio(IntEnum):
    ALWAYS = 1     # 100% Chance
    HIGH = 2       # 80% Chance
    OPTIONAL = 3   # 30% Chance

def check_translator_hijack_is_active(logger):



    path = PROJECT_ROOT / "config"  / "maps" / "plugins" / "standard_actions" / "language_translator" / "de-DE" / "FUZZY_MAP_pre.py"

    if not path.exists():
        logger.info(f"st:HIJACK: path {path} not exists!")
        return False

    pattern = re.compile(r"#[ ]*TRANSLATION_RULE[ ]*\n[^\n]*#")
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if pattern.search(line):
            logger.info(f"st:🚨 HIJACK: Rule in ..{str(path)[-30:]}{lineno} is active!")
            return lineno

    return False



# file: scripts/py/func/checks/self_tester.py:79
def run_core_logic_self_test(logger, tmp_dir_aura: Path, lt_url, lang_code): # , LANGUAGETOOL_JAR_PATH=None, lt_process=None):
    """
    Runs a series of predefined tests, guarded by a persistent throttle mechanism.
    """
    # scripts/py/func/checks/self_tester.py

    _wait_for_languagetool_ready(lt_url, logger)

    rules_file_path = Path(__file__).parents[4] / 'config' / 'maps' / 'plugins' / 'standard_actions' / 'language_translator' / 'de-DE' / 'FUZZY_MAP_pre.py'
    translation_state_path = Path(__file__).parents[4] / 'config' / 'maps' / 'plugins' / 'standard_actions' / 'language_translator' / 'de-DE' / 'translation_state.py'

    # Source - https://stackoverflow.com/q/10840533
    # Posted by Scott C Wilson
    # Retrieved 2026-02-08, License - CC BY-SA 3.0

    if os.path.exists(translation_state_path):
        os.remove(translation_state_path)

    # RULES_FILE_PATH = 'config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py'
    # create backup path (same name + .bak)
    backup_path = rules_file_path.with_name(rules_file_path.name + ".off.backup.py")
    # copy (overwrites existing backup)
    # shutil.copy2(backup_path, rules_file_path)

    if should_restore(backup_path, rules_file_path):
        shutil.copy2(backup_path, rules_file_path)
    else:
        print(":st:Skipping restore: files appear different/newer or within tolerance.")



    lineno = check_translator_hijack_is_active(logger)
    if lineno and lineno>0:
        logger.info("st:self_tester.py exit exit exit")
        logger.info("st:75:🚨 HIJACK: rule is activ")
        logger.info(f"""
        st:
        75:🚨 HIJACK: rule is activ during self_test! maybe check: 
        config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py:{lineno} 
        (check_translator_hijack) --> exit(1)
        """)
        exit(1)



    # 1. Collect all parameters needed by _execute_self_test_core
    core_params = {
        'logger': logger,
        'tmp_dir_aura': tmp_dir_aura,
        'lt_url': lt_url,
        'lang_code': lang_code
    }

    # 2. Call the generic wrapper function

    test_executed = run_function_with_throttling(
        logger,
        state_dir=tmp_dir_aura,
        core_logic_function=_execute_self_test_core,
        func_params=core_params,
        state_file_name="self_test_throttle_state.json"  # Provide a specific file name for this function
    )

    # scripts/py/func/checks/self_tester.py:135
    if not test_executed:
        logger.warning(f":st:⏩ Self-test not executed. Wey?? _execute_self_test_core:{_execute_self_test_core}")

    return test_executed

# helper for use named Parameters
def case(input_text: str, expected: str, context: str = '', 
        lang: str = 'de-DE', 
        lt: bool = True, 
        prio: TestPrio = TestPrio.OPTIONAL):
    # prio = TestPrio.ALWAYS  # 1.0 = 100%
    return input_text, expected, context, lang, lt, prio

# file: scripts/py/func/checks/self_tester.py:79

# import concurrent.futures

def _wait_for_languagetool_ready(lt_url, logger, timeout=60, interval=2):
    """Wait until LanguageTool server is ready to accept requests."""
    import urllib.request
    import urllib.error

    # health_url = f"{lt_url}/v2/languages"
    health_url = f"{lt_url.rstrip('/').replace('/v2/check', '')}/v2/languages"
    logger.info(f":st:⏳ Waiting for LanguageTool at {health_url} ...")

    start = time.perf_counter()
    while time.perf_counter() - start < timeout:
        try:
            with urllib.request.urlopen(health_url, timeout=3) as resp:
                if resp.status == 200:
                    elapsed = time.perf_counter() - start
                    logger.info(f":st:✅ LanguageTool ready after {elapsed:.1f}s")
                    return True
        except Exception:
            pass
        time.sleep(interval)

    logger.error(f":st: ❌ LanguageTool not ready after {timeout}s – aborting.")
    logger.error(f":st: LanguageTool not ready after {timeout}s – aborting.")
    logger.info(f":st: LanguageTool not ready after {timeout}s – aborting.")
    print(f":st: LanguageTool not ready after {timeout}s – aborting.")
    sys.exit(1)




def _execute_self_test_core(logger, tmp_dir_aura, lt_url, lang_code):
    """

    """
    _wait_for_languagetool_ready(lt_url, logger)

    settings = DynamicSettings()

    backup_tts_enabled = settings.PLUGIN_HELPER_TTS_ENABLED
    settings.PLUGIN_HELPER_TTS_ENABLED = False

    # /home/seeh/projects/py/STT/scripts/py/func/checks/self_tester.py

    # Base directory for all tests

    print(':st:🌞🌞🌞🌞🌞 4.5.26 15:17 Mon 🌞🌞🌞🌞🌞🌞🌞 tmp_dir=', tmp_dir_aura)

    test_base_dir = tmp_dir_aura / "sl5_aura_self_test"
    test_base_dir.mkdir(parents=True, exist_ok=True)

    # run_auto_zip_sanity_check(logger) # runs asynchron and will run at the end to check if creating zips work
    # auto_zip_thread = run_auto_zip_sanity_check(logger)

    test_cases = [
        # --- Settings checks ---
        case(input_text='leerworttest', expected="leerworttest1", context='punctation map test', lang='de-DE', lt=False,
             prio=TestPrio.OPTIONAL),
        case(input_text='->AUDIO_INPUT_DEVICE<-', expected="SYSTEM_DEFAULT",
             context='proff if we can change settings 2026-0104-1435', lt=False, prio=TestPrio.OPTIONAL),

        # --- LT + MAP Kombinationen ---
        case('Sebastian mit nachnamen', 'Sebastian mit Nachnamen',
             'LT Uppercase. may check --> FUZZY_MAP_pre.py', lt=True, prio=TestPrio.HIGH),
        case(input_text='null', expected='0', context='MAP git', lt=False, prio=TestPrio.OPTIONAL),
        case(input_text='über die konsole zu bedienen', expected='Über die Konsole zu bedienen', context='git', lt=True,
             prio=TestPrio.HIGH),
        case(input_text='geht cobit', expected='git commit', context='FUZZY_MAP_pre git', lt=False, prio=TestPrio.OPTIONAL),

        # --- en-US ---
        case('colours', 'colors', 'fix by LT', lang='en-US', lt=True, prio=TestPrio.OPTIONAL),
        case('underilnes', 'underlines', 'fix by LT', lang='en-US', lt=True, prio=TestPrio.ALWAYS),
        case('too have', 'to have', 'fix by LT', lang='en-US', lt=True, prio=TestPrio.ALWAYS),
        case('5 PM in the afternoon', '5 PM', 'fix by LT', lang='en-US', lt=True, prio=TestPrio.HIGH),
        case('good nigt Mum', 'Good night Mum', 'Funny useless rule ;) just for testing', lang='en-US', lt=True,
             prio=TestPrio.ALWAYS),
        case('thousand dollars.', '1000 dollars.', 'Number with unit', lang='en-US', lt=False, prio=TestPrio.HIGH),
        case('one and thousand dollars.', '1 and 1000 dollars.', 'Number with unit', lang='en-US', lt=False, prio=TestPrio.ALWAYS),

        # --- de-DE MAP + LT ---
        case('tausend euro. Und euro großgeschrieben.', '1000 Euro. Und Euro großgeschrieben.',
             'Number with unit', lt=True, prio=TestPrio.HIGH),
        case('was ist 5 plus 3', 'Das Ergebnis von 5 plus 3 ist 8.', 'calc in MAP Wannweil', lt=False, prio=TestPrio.ALWAYS),
        case('bitte reservieren sie einen tisch für zwei personen um acht uhr',
             'Bitte reservieren Sie einen Tisch für 2 Personen um 8 Uhr',
             'Polite request with time and number', lt=True, prio=TestPrio.HIGH),

        # --- Zahlen ---
        case('eins', '1', 'numbers_to_digits', lt=False, prio=TestPrio.OPTIONAL),
        case('eins zwei', '12', 'numbers_to_digits', lt=False, prio=TestPrio.ALWAYS),
        case('sieben acht neun', '789', 'numbers_to_digits', lt=False, prio=TestPrio.ALWAYS),
        case('zwei zwei', '22', 'Multiple replacement check', lt=False, prio=TestPrio.ALWAYS),
        case('sieben', '7', 'Numbers as digits', lt=False, prio=TestPrio.HIGH),
        case('acht', '8', 'Numbers as digits', lt=False, prio=TestPrio.ALWAYS),
        case('neun', '9', 'Numbers as digits', lt=False, prio=TestPrio.ALWAYS),
        case('zehn', '10', 'Number as digit', lt=False, prio=TestPrio.HIGH),
        case('komma', ',', 'Exact MAP punctuation', lt=False, prio=TestPrio.OPTIONAL),
        case('fünf komma', '5 ,', 'Decimal number', lt=False, prio=TestPrio.HIGH),
        case('fünf komma drei', '5 , 3', 'Decimal number', lt=False, prio=TestPrio.ALWAYS),

        # --- Grundlegende Satzzeichen ---
        case('punkt', '.', 'Exact MAP', lt=False, prio=TestPrio.OPTIONAL),
        case('fragezeichen', '?', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('ausrufezeichen', '!', 'Exact MAP', lt=False, prio=TestPrio.HIGH),
        case('doppelpunkt', ':', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('semikolon', ';', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('bindestrich', '-', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('gedankenstrich', '–', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('klammer auf', '(', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),
        case('klammer zu', ')', 'Exact MAP', lt=False, prio=TestPrio.ALWAYS),

        # --- MAP Wannweil ---
        case('Sekunde Lauffer', 'Sigune Lauffer', 'MAP Wannweil', lt=False, prio=TestPrio.OPTIONAL),
        case('Sekunde lauf war', 'Sigune Lauffer war', 'MAP Wannweil', lt=False, prio=TestPrio.HIGH),

        # --- Partial MAP + LT ---
        case('mit nachnamen laufer', 'Mit Nachnamen Lauffer', 'Partial map + LT', lt=True, prio=TestPrio.HIGH),
        case('Sebastian mit nachnamen', 'Sebastian mit Nachnamen', 'Partial map + LT', lt=True, prio=TestPrio.HIGH),
        case('von sebastian laufer', 'Von Sebastian Lauffer', 'Partial map + LT', lt=True, prio=TestPrio.HIGH),
        case('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT', lt=True, prio=TestPrio.HIGH),
        case('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', lt=False, prio=TestPrio.OPTIONAL),

        # --- FUZZY_MAP_pre ---
        case('git at', 'git add .', 'Fuzzy map REGEX match', lt=False, prio=TestPrio.OPTIONAL),
        case('geht status', 'git status', 'Fuzzy map FUZZY string', lt=False, prio=TestPrio.ALWAYS),
        case('geht cobit', 'git commit', 'FUZZY_MAP_pre', lt=False, prio=TestPrio.OPTIONAL),

        # --- Großschreibung via LT ---
        case('ich heiße max', 'Ich heiße Max', 'Capitalization pronoun + proper noun', lt=True, prio=TestPrio.HIGH),
        case('der hund bellt', 'Der Hund bellt', 'Capitalization article + noun', lt=True, prio=TestPrio.OPTIONAL),
        case('die katze schläft', 'Die Katze schläft', 'Capitalization article + noun', lt=True, prio=TestPrio.ALWAYS),
        case('ein haus und ein garten', 'Ein Haus und ein Garten', 'Capitalization nouns', lt=True, prio=TestPrio.HIGH),
        case('heute ist montag', 'Heute ist Montag', 'Capitalization day', lt=True, prio=TestPrio.OPTIONAL),
        case('heute ist ein schöner tag', 'Heute ist ein schöner Tag', 'Capitalization day', lt=True, prio=TestPrio.ALWAYS),
        case('heute ist ein schöner tag zwei drei', 'Heute ist ein schöner Tag 23',
             'Capitalization + number', lt=True, prio=TestPrio.ALWAYS),
        case('zwei drei hunde sind im wald', '23 Hunde sind im Wald', 'Number at start + LT', lt=True, prio=TestPrio.OPTIONAL),
        case('die antwort ist ein test', 'Die Antwort ist ein Test', 'Window filter provocation', lt=True, prio=TestPrio.HIGH),
        case('im sommer ist es warm', 'Im Sommer ist es warm', 'Capitalization season', lt=True, prio=TestPrio.ALWAYS),

        # --- Häufige Phrasen ---
        case('danke schön', 'Danke schön', 'Common thanks', lt=True, prio=TestPrio.ALWAYS),
        case('bitte schön', 'Bitte schön', 'Common courtesy', lt=True, prio=TestPrio.ALWAYS),
        case('entschuldigung', 'Entschuldigung', 'Common apology', lt=True, prio=TestPrio.HIGH),
        case('ich verstehe', 'Ich verstehe', 'Common confirmation', lt=True, prio=TestPrio.ALWAYS),
        case('ich weiß nicht', 'Ich weiß nicht', 'Common uncertainty', lt=True, prio=TestPrio.HIGH),
        case('alles klar', 'Alles klar', 'Common affirmation', lt=True, prio=TestPrio.ALWAYS),
        case('auf wiedersehen', 'Auf Wiedersehen', 'Common farewell', lt=True, prio=TestPrio.HIGH),
        case('bis später', 'Bis später', 'Common farewell', lt=True, prio=TestPrio.ALWAYS),
        case('es ist kalt draußen', 'Es ist kalt draußen', 'Simple sentence', lt=True, prio=TestPrio.ALWAYS),
        case('was machst du heute', 'Was machst du heute', 'Common question', lt=True, prio=TestPrio.ALWAYS),
        case('kein problem', 'Kein Problem', 'Common phrase', lt=True, prio=TestPrio.HIGH),
        case('zum beispiel', 'Zum Beispiel', 'Common phrase', lt=True, prio=TestPrio.HIGH),
        case('und so weiter', 'Und so weiter', 'Common phrase', lt=True, prio=TestPrio.ALWAYS),
        case('einer nach dem anderen', 'Einer nach dem anderen', 'Idiomatic', lt=True, prio=TestPrio.ALWAYS),

        # --- Umlaute ---
        case('schön', 'schön', 'Umlaut – unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('überall', 'überall', 'Umlaut – unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('für', 'für', 'Umlaut – unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('größer', 'größer', 'Umlaut+Eszett – unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('weiß', 'weiß', 'Eszett – unverändert', lt=True, prio=TestPrio.ALWAYS),
        case('müde', 'müde', 'Umlaut – unverändert', lt=True, prio=TestPrio.ALWAYS),
        case('straße', 'Straße', 'Eszett + Großschreibung', lt=True, prio=TestPrio.HIGH),
        case('füße', 'Füße', 'Umlaut + Großschreibung', lt=True, prio=TestPrio.ALWAYS),
        case('hände', 'Hände', 'Umlaut + Großschreibung', lt=True, prio=TestPrio.ALWAYS),

        # --- Abkürzungen ---
        case('respektive', 'respektive', 'unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('circa', 'circa', 'unverändert', lt=False, prio=TestPrio.ALWAYS),
        case('unter anderem', 'Unter anderem', 'Common abbreviation', lt=True, prio=TestPrio.HIGH),
        case('doktor', 'Doktor', 'Title abbreviation', lt=True, prio=TestPrio.HIGH),
        case('professor', 'Professor', 'Title abbreviation', lt=True, prio=TestPrio.ALWAYS),
        case('zum schluss', 'Zum Schluss', 'Custom abbreviation', lt=True, prio=TestPrio.ALWAYS),

        # --- Fragen und Ausrufe ---
        case('wie spät ist es', 'Wie spät ist es', 'Direct question', lt=True, prio=TestPrio.HIGH),
        case('wo finde ich toilette', 'Wo finde ich Toilette', 'Direct question', lt=True, prio=TestPrio.ALWAYS),
        case('das ist unglaublich', 'Das ist unglaublich', 'Exclamatory', lt=True, prio=TestPrio.ALWAYS),
        case('hilfe', 'Hilfe', 'word', lt=True, prio=TestPrio.HIGH),
        case('was für ein tag', 'Was für ein Tag', 'Exclamatory phrase', lt=True, prio=TestPrio.ALWAYS),
        case('stopp', 'stopp', 'unverändert', lt=False, prio=TestPrio.ALWAYS),

        # --- Befehle ---
        case('gehe nach links', 'Gehe nach links', 'Simple command', lt=True, prio=TestPrio.ALWAYS),
        case('schalte das licht ein', 'Schalte das Licht ein', 'Simple command', lt=True, prio=TestPrio.HIGH),
        case('öffne die tür', 'Öffne die Tür', 'Simple command', lt=True, prio=TestPrio.ALWAYS),
        case('wiederhole das bitte', 'Wiederhole das bitte', 'Request', lt=True, prio=TestPrio.ALWAYS),

        # --- Komplexere Sätze ---
        case('die sonne scheint auf die blumen', 'Die Sonne scheint auf die Blumen',
             'Compound sentence', lt=True, prio=TestPrio.HIGH),
        case('obwohl es regnet ist die stimmung gut', 'Obwohl es regnet, ist die Stimmung gut',
             'Subordinate clause + comma', lt=True, prio=TestPrio.OPTIONAL),
        case('der kleine hund spielt mit seinem neuen spielzeug',
             'Der kleine Hund spielt mit seinem neuen Spielzeug',
             'Detailed sentence', lt=True, prio=TestPrio.ALWAYS),
        case('das wetter wird morgen sonnig mit temperaturen um die zwanzig grad',
             'Das Wetter wird morgen sonnig mit Temperaturen um die 20 Grad',
             'digits_to_numbers + LT', lt=True, prio=TestPrio.HIGH),
    ]

    # test_cases = [
    #     # ('was is 5 mal 1', 'Das Ergebnis von 5 mal 2 ist 10.', 'Partial map + LT correction', 'de-DE'),
    #     ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
    # ]

    # 1. Filter test cases for the current language
    PRIO_CHANCE = {
        TestPrio.ALWAYS: 1.0,
        TestPrio.HIGH: 0.8,
        TestPrio.OPTIONAL: 0.3
    }
    import random
    active_tests = []
    for test_case in test_cases:
        if len(test_case) == 6:
            raw_text, expected, description, check_lang, use_lt, prio = test_case
            if check_lang == lang_code and random.random() < PRIO_CHANCE[prio]:
                active_tests.append((raw_text, expected, description, use_lt))
        elif len(test_case) == 5:
            raw_text, expected, description, check_lang, use_lt = test_case
            if check_lang == lang_code:
                active_tests.append((raw_text, expected, description, use_lt))
        elif len(test_case) == 4:
            raw_text, expected, description, check_lang = test_case
            if check_lang == lang_code:
                active_tests.append((raw_text, expected, description, True))
        elif len(test_case) == 3:
            active_tests.append((*test_case, True))
        elif len(test_case) == 2 and lang_code == 'de-DE':
            active_tests.append((test_case[0], test_case[1], '', True))



    logger.info(f":st:Running {len(active_tests)} tests in parallel using PROCESSES...")
    # logger.info(f":st:Running {len(active_tests)} tests in parallel (ThreadPool)...")


    # 2. Worker function with isolated sub-directory

    # 3. Parallel Execution
    passed_count = 0
    failed_count = 0

    # Use 20 workers to fully saturate the 16-core Ryzen CPU



    # ProcessPoolExecutor nutzt echte CPU-Kerne parallel
    # But ATTENTION: The 'logger' object often cannot be easily copied into processes.
    # We pass None as a logger or use simple print logging within.


    # scripts/py/func/checks/self_tester.py:383

    # import multiprocessing
    import multiprocessing
    # ctx = multiprocessing.get_context("fork")
    # with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=ctx) as executor:






    import os
    os.environ["AURA_SELF_TEST_RUNNING"] = "1"  # inherited by fork
    start_time = time.perf_counter()
    ctx = multiprocessing.get_context("fork")
    num_workers = os.cpu_count()
    # lt_workers = max(2, num_workers // 2)

    lt_tests = [(r, e, d, True) for r, e, d, use_lt in active_tests if use_lt]
    non_lt_tests = [(r, e, d, False) for r, e, d, use_lt in active_tests if not use_lt]
    logger.info(f":st: Phase 1 – {len(non_lt_tests)} deterministic tests (max_workers={num_workers})")
    logger.info(f":st: Phase 2 – {len(lt_tests)} LT-dependent tests   (max_workers=2)")

    test_metrics = [] # To store (duration, description, success)

    def _collect_results(futures_map):
        nonlocal passed_count, failed_count
        for future in concurrent.futures.as_completed(futures_map):
            try:
                result = future.result(timeout=60)
                success, raw, actual, expected, desc, duration, use_lt = result

                test_metrics.append({
                    'duration': duration,
                    'desc': desc,
                    'input': raw,
                    'success': success,
                    'use_lt': use_lt
                })

                if success:
                    passed_count += 1
                else:
                    failed_count += 1
                    logger.error(f":st:  FAIL: {desc} ({duration:.3f}s)")
                    logger.error(f":st:   Input: ---> '{raw}'")
                    logger.error(f":st:   Expected:-> '{expected}'")
                    logger.error(f":st:   Got: -----> '{actual}'")
                    logger.info(
                        f":st: ==> Passed: {passed_count}, Failed: {failed_count} ==> :) its oky no problem. try it better next time ;)")
            except Exception as e:
                failed_count += 1
                print(f":st: Process crashed: {e}")

    # Issue #94: submit non-LT tests first, then LT tests (single pool, stable)
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=ctx) as executor:
        futures = {}
        for i, t in enumerate(non_lt_tests):
            futures[executor.submit(run_single_test_process, i, t, lang_code, lt_url, str(test_base_dir))] = t
        for i, t in enumerate(lt_tests, start=len(non_lt_tests)):
            futures[executor.submit(run_single_test_process, i, t, lang_code, lt_url, str(test_base_dir))] = t
        _collect_results(futures)











    #core_logic_self_test_is_running_FILE = tmp_dir_aura / "core_logic_self_test_FILE_is_running"


    # MAX_WAIT_SECONDS=150

    # run_auto_zip_sanity_check(logger)

    # Am Ende, bevor das Programm endet:
    # if auto_zip_thread:
    #     logger.info("Auto-Zip: Warte auf Thread...")
    #     auto_zip_thread.join(timeout=MAX_WAIT_SECONDS)

    # scripts/py/func/checks/self_tester.py:420

    # 4.1 Detailed Performance Report at the very end
    logger.info("=" * 40)
    # logger.info(":st: PERFORMANCE REPORT (Slowest tests first):")
    logger.info(f":st: {'STAT':<5} | {'TIME':<8} | {'LT':<4} | {'DESCRIPTION':<40} | {'INPUT'}")
    # Sort by duration descending
    sorted_metrics = sorted(test_metrics, key=lambda x: x['duration'], reverse=True)

    for m in sorted_metrics:
        status = "✅" if m['success'] else "❌"
        lt_flag = "LT" if m['use_lt'] else "--"
        logger.info(f":st: {status:<1} | {m['duration']:>6.3f}s | {lt_flag:<2} | {m['desc'][:40]:<40} | '{m['input']}'")


    logger.info("=" * 40)


    # 4.2 Summary
    duration = time.perf_counter() - start_time
    logger.info("=" * 40)
    # m1 =f"✅ Passed: {passed_count} | ❌ Failed: {failed_count}"
    if failed_count > 0:
        logger.info(f":st:✅ Passed: {passed_count} | ❌ Failed: {failed_count} Tests (hint search for: ❌ FAIL )")
    else:
        logger.info(f":st:✅ Passed: all {passed_count} ✅ | {failed_count} failed 🙂")

    second_per_test = duration / len(active_tests)
    max202605042151 =  0.078
    if second_per_test > max202605042151:
        m1 = f"🛑 ALERT tests_per_second: expected second per test  <= {max202605042151}, got {second_per_test:.3f} second per test"
        m2 = "🛑 mostly it was 6.45 to 7 seconds per 92 tests. Check README variable for more info."
        logger.critical(f"{m1} {m2}")
        logger.info(f"{m1} {m2}")

        if second_per_test > 3 * max202605042151:
            m1 = f"🛑 its DOUBLE of expected second per test, got {second_per_test:.3f} second per test. that maybe happens at the first run when RAM is clear"
            m2 = "🛑 ==> exit"
            logger.critical(f"{m1} {m2}")
            logger.info(f"{m1} {m2}")
            sys.exit(1)


    m2=f"⌚ Total Duration: {duration:.2f} seconds (second_per_test:{second_per_test:.2f} s/test)"
    logger.info(f"pid:{os.getpid()} :st:{m2}")
    speak_inclusive_fallback(f"{m2}", 'de-DE') # 'en-US') # 'de-DE')

    import threading
    thread_name = threading.current_thread().name
    logger.info(f"- {thread_name} :st:⌚ maybe check: run_always_no_throttling_ignore_times = True/False ?")
    logger.info(f"- {thread_name} -" * 40)

    README = """
# Example Results (from scripts/py/func/checks/self_tester.py:525):

5.5.'26 21:07 Tue
20:54:08,072 - MainThread - INFO - pid:211301 :st:⌚ Total Duration: 5.95 seconds (second_per_test:0.06 s/test)

4.5.'26 14:07 Mon
59,741 - INFO   - :st:✅ Passed: 95 | ❌ Failed: 0 Tests

10 matches (10 checked) found in open files
/home/seeh/projects/py/STT/log/aura_engine.log: 10
19:49:59,063 - MainThread - INFO - :st:⌚ Total Duration: 7.65 seconds (second_per_test:0.08 s/test)
1703: 27: 14:14:11,884 - INFO   - :st:⌚ Total Duration: 8.57 seconds
1704: 27: 14:14:11,884 - INFO   - :st:⌚ Total Duration: 8.57 seconds
1715: 25: 15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds
1716: 25: 15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds
1722: 25: 15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds
1725: 25: 15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds
1734: 25: 15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds
1735: 25: 15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds
1741: 25: 15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds
1744: 25: 15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds

15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds
15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds



## 17.4.'26 15:15 Fri
59,741 - INFO   - :st:✅ Passed: 95 | ❌ Failed: 0 Tests
15:08:59,741 - INFO   - :st:⌚ Total Duration: 6.52 seconds

Passed: 95 | ❌ Failed: 0 Tests (hint search for: ❌ FAIL )
15:17:25,615 - INFO   - :st:⌚ Total Duration: 6.45 seconds


    """
    logger.info("-" * 40)
    # logger.info(README)
    formatted_readme = "\n".join([f"📜 {line}" for line in README.strip().splitlines()])
    logger.info(f"History:\n{formatted_readme}")

    settings.PLUGIN_HELPER_TTS_ENABLED = backup_tts_enabled

    # scripts/py/func/checks/self_tester.py:434
    # core_logic_self_test_is_running_FILE.unlink(missing_ok=True)

    core_logic_self_test_is_running_file = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"
    core_logic_self_test_is_running_file.unlink(missing_ok=True)


    if failed_count > 0:
        print(f':st: failed_count > 0: {failed_count} ==> exiting')
        # sys.exit(1)


# futures = {executor.submit(run_single_test, i, t, lang_code, lt_url, str(test_base_dir)): t
#            for i, t in enumerate(active_tests)}


import sys
import os
import time
# import traceback
# from pathlib import Path


# Dummy-Logger for Proses

class SimpleNullLogger:
    def info(self, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def debug(self, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args, **kwargs):
        pass

# if somebody is confused send him:
# find . -name "*settings.py"                                                                                                                                     ✔

def run_single_test_process(index, test_data, lang_code, lt_url, test_base_dir_str):
    # print(f":st:🐣 [{index}] Sub-Process gestartet") # Direkter Print
    start_individual = time.perf_counter() # Start timing
    raw_text, expected, description, use_lt = test_data

    try:

        # os.environ["AURA_SELF_TEST_RUNNING"] = "1"

        # print(f":st:🐣 [{index}] Imports ok")

        # current_file = Path(__file__).resolve()

        # 1. Manueller Import
        # ds_path = current_file.parents[1] / "config" / "dynamic_settings.py"
        # spec = importlib.util.spec_from_file_location("dynamic_settings", str(ds_path))
        # ds_mod = importlib.util.module_from_spec(spec)
        # spec.loader.exec_module(ds_mod)
        # DynamicSettings = ds_mod.DynamicSettings
        #
        # 2. Root setzen
        # PROJECT_ROOT = str(current_file.parents[4])
        # if PROJECT_ROOT not in sys.path:
        #     sys.path.insert(0, PROJECT_ROOT)




        # raw_text, expected, description = test_data

        # 3. Absolut isoliertes Verzeichnis (Task-Index im Namen)
        worker_dir = Path(test_base_dir_str) / f"task_{index}"
        worker_dir.mkdir(parents=True, exist_ok=True)

        settings = DynamicSettings()
        null_logger = SimpleNullLogger()

        # 4. NANOSEKUNDEN + INDEX für absolute Eindeutigkeit
        # time.time_ns() liefert z.B. 1705678901234567890
        unique_id_ns = time.time_ns() + index

        # We convert it to a float seconds value for the function,
        # but with extremely high precision.
        unique_time_float = unique_id_ns / 1_000_000_000.0
        # unique_time_float = float(index)  # Absolut eindeutig: 0.0, 1.0, 2.0 ...

        # print(':st:🌞🌞🌞 worker dir:', worker_dir)
        # print(':st:🌞🌞🌞 test_base_dir_str:', test_base_dir_str)

        # process_text_in_background(
        #     null_logger, lang_code, raw_text,
        #     None,  # Standard output_dir (ignored)
        #     unique_time_float, lt_url,
        #     output_dir_override=worker_dir  # Explicit override
        # )

        process_text_in_background(
            null_logger, lang_code, raw_text,
            None,
            unique_time_float, lt_url,
            output_dir_override=worker_dir,
            session_id=index,
            chunk_id=1
        )



        # scripts/py/func/checks/self_tester.py:523


        core_logic_self_test_is_running_file = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"

        # After the first run: Set flag → Zip test white “now I can check”

        if not core_logic_self_test_is_running_file.exists():
            core_logic_self_test_is_running_file.write_text(str(int(time.time())))
            print(":st:Auto-Zip: Flag created process_text_in_background was finished before")

        # 5. Datei finden (nur in diesem privaten Task-Ordner!)

        output_files = list(worker_dir.glob("tts_output_*.txt"))

        # ÄNDERN (ca. Zeile 539):
        if not output_files:
            duration = time.perf_counter() - start_individual
            return False, raw_text, "[NO_FILE]", expected, description, duration, use_lt

        # output_files = list(worker_dir.glob("tts_output_*.txt"))
        # if not output_files:
        #     return False, raw_text, "[NO_FILE]", expected, description

        result_file = output_files[0]
        with open(result_file, 'r', encoding='utf-8-sig') as f:
            actual = f.read().strip()

        # Cleanup Signatures
        if hasattr(settings, 'signatur1'): actual = actual.replace(settings.signatur1, '')
        if hasattr(settings, 'signatur'): actual = actual.replace(settings.signatur, '')
        actual = actual.strip()

        # Aufräumen
        os.remove(result_file)
        try:
            worker_dir.rmdir()
        except Exception as e:
            print(f':st:717: {e}')
            pass



        pattern = r"(🗣|\-\-)"  # cut off signature . example: first sequence of digits
        m = re.search(pattern, actual)
        if m:
            actual2 = actual[:m.start()]
        else:
            actual2 = actual  # no match -> keep original


        duration = time.perf_counter() - start_individual

        return actual2 == expected, raw_text, actual2, expected, description, duration, use_lt

    #     logger.error(f"Core function {core_logic_function.__name__} failed during execution: {e}\n{traceback.format_exc()}")

    # Neu:
    except Exception as e:
        import traceback
        duration = time.perf_counter() - start_individual
        msg = f"Core function failed: {e}\n{traceback.format_exc()}"

        return False, "ERROR", msg, "ERROR", "Process execution failed", duration, use_lt

    # Alt:
    # except Exception as e:
    #     import traceback
    #     return False, "ERROR", f"{str(e)}\n{traceback.format_exc()}", "ERROR", "Process execution failed"

def run_single_test_202501311853(logger, index, test_data, lang_code, lt_url, test_base_dir):
    raw_text, expected, description = test_data

    # Create a UNIQUE folder for this specific test case
    # This is the ONLY way to prevent threads from stealing each other's files
    worker_dir = test_base_dir / f"task_{index}"
    worker_dir.mkdir(parents=True, exist_ok=True)

    print(':st:scripts/py/func/checks/self_tester.py:497 🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞')

    try:
        # Execute processing in the isolated folder
        # process_text_in_ background(
        #     logger, lang_code, raw_text, worker_dir,
        #     time.time(), lt_url, output_dir_override=worker_dir
        # )

        # In this private folder, there will only be ONE tts_output_*.txt file
        output_files = list(worker_dir.glob("tts_output_*.txt"))

        if not output_files:
            return False, raw_text, "[FILE_NOT_FOUND]", expected, description

        # Take the file found in the private folder
        result_file = output_files[0]
        with open(result_file, 'r', encoding='utf-8-sig') as f:
            actual = f.read().strip()

        # Clean signatures
        if hasattr(settings, 'signatur1'): actual = actual.replace(settings.signatur1, '')
        if hasattr(settings, 'signatur'): actual = actual.replace(settings.signatur, '')
        actual = actual.strip()

        # Cleanup this specific test folder
        os.remove(result_file)
        try:
            worker_dir.rmdir()
        except Exception as e:
            print(f':st:812: {e}')
            pass

        # -- Sent via Aura --'
        pattern = r"(🗣|\-\-)"  # cut off signature . example: first sequence of digits
        m = re.search(pattern, expected)
        if m:
            expected2 = expected[:m.start()]
        else:
            expected2 = expected  # no match -> keep original


        return actual == expected2, raw_text, actual, expected2, description

    except Exception as e:
        return False, raw_text, f"Error: {str(e)}", expected, description



# from pathlib import Path
# import time
import hashlib
# import shutil

def sha256(path: Path, chunk_size=1 << 20):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            h.update(data)
    return h.hexdigest()

def should_restore(backup: Path, target: Path,
                   mtime_tolerance_seconds: float = 5.0,
                   size_tolerance_bytes: int = 2):
    if not backup.exists() or not target.exists():
        return backup.exists() and not target.exists()

    b_mtime = backup.stat().st_mtime
    t_mtime = target.stat().st_mtime
    # If backup is sufficiently newer, consider restore
    if b_mtime - t_mtime > mtime_tolerance_seconds:
        return True

    # If mtimes are almost same, check size
    b_size = backup.stat().st_size
    t_size = target.stat().st_size
    if abs(b_size - t_size) > size_tolerance_bytes:
        # sizes differ more than tolerance: prefer not to overwrite if target is newer
        return b_size > t_size

    # If sizes are same (within tolerance) and mtimes close, optionally compare hashes
    return sha256(backup) != sha256(target)

# scripts/py/func/checks/self_tester.py:834
if __name__ == "__main__":
    import logging

    # Logger-Setup für die Konsole
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_logger = logging.getLogger("aura_self_test")

    # Pfade vorbereiten
    tmp_path = Path("/tmp/sl5_aura")
    tmp_path.mkdir(parents=True, exist_ok=True)

    # Standardwerte für GHA/CLI
    lt_url = "http://localhost:8082"
    lang = "de-DE"

    print(f":st: Starting self-test (CLI mode) using {lt_url}...")
    try:
        run_core_logic_self_test(test_logger, tmp_path, lt_url, lang)
    except Exception as e:
        print(f":st: CRITICAL ERROR: {e}")
        sys.exit(1)
