# scripts/py/func/checks/self_tester.py
import contextlib

import platform
import re
import concurrent.futures
import shutil
import sys
# import concurrent.futures

import os
import warnings
from pathlib import Path

# from .auto_zip_startup_test import run_auto_zip_sanity_check

from ..audio_manager import speak_inclusive_fallback
# from ..log_memory_details import log4DEV
from ..process_text_in_background import process_text_in_background

# # scripts/py/func/global_state.py
from .. import global_state

from ..config.dynamic_settings import settings

is_ci = os.getenv('CI') == 'true'

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
else:
    TMP_DIR = Path("/tmp")


from enum import IntEnum

class TestPrio(IntEnum):
    ALWAYS = 1     # 100% Chance
    HIGH = 2       # 80% Chance
    OPTIONAL = 3   # 30% Chance
    NEVER = 0   # 0% Chance

def check_translator_hijack_is_active(logger):
    tmp_dir = TMP_DIR # Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())


    path = PROJECT_ROOT / "config"  / "maps" / "plugins" / "standard_actions" / "language_translator" / "de-DE" / "FUZZY_MAP_pre.py"

    if not path.exists():
        if global_state.LOGGING_ENABLED:
            logger.info(f"st:HIJACK: path {path} not exists!")
        return False

    pattern = re.compile(r"#[ ]*TRANSLATION_RULE[ ]*\n[^\n]*#")
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if pattern.search(line):
            if global_state.LOGGING_ENABLED:
                logger.info(f"st:🚨 HIJACK: Rule in ..{str(path)[-30:]}{lineno} is active!")
            return lineno

    return False

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Note: In aura_engine.py this might be SCRIPT_DIR instead of project_root

from .run_function_with_throttling import run_function_with_throttling
# from ..config.dynamic_settings import settings


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
        if global_state.LOGGING_ENABLED:
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
    if global_state.LOGGING_ENABLED:
        logger.info(f":st:⏳ Waiting for LanguageTool at {health_url} ...")

    start = time.perf_counter()
    while time.perf_counter() - start < timeout:
        try:
            with urllib.request.urlopen(health_url, timeout=3) as resp:
                if resp.status == 200:
                    elapsed = time.perf_counter() - start
                    if global_state.LOGGING_ENABLED:
                        logger.info(f":st:✅ LanguageTool ready after {elapsed:.1f}s")
                    return True
        except Exception:
            pass
        time.sleep(interval)

    if global_state.LOGGING_ENABLED:
        logger.error(f":st: ❌ LanguageTool not ready after {timeout}s – aborting.")
        logger.error(f":st: LanguageTool not ready after {timeout}s – aborting.")
        logger.info(f":st: LanguageTool not ready after {timeout}s – aborting.")
    print(f":st: LanguageTool not ready after {timeout}s – aborting.")
    sys.exit(1)




def _execute_self_test_core(logger, tmp_dir_aura, lt_url, lang_code):
    """

    """


    _wait_for_languagetool_ready(lt_url, logger)

    backup_tts_enabled = settings.PLUGIN_HELPER_TTS_ENABLED
    settings.PLUGIN_HELPER_TTS_ENABLED = False

    if not settings.LOG_in_selftest or is_ci:
        global_state.LOGGING_ENABLED = False


    # /home/seeh/projects/py/STT/scripts/py/func/checks/self_tester.py

    # Base directory for all tests

    print(':st:🌞🌞🌞🌞🌞 4.5.26 15:17 Mon 🌞🌞🌞🌞🌞🌞🌞 tmp_dir=', tmp_dir_aura)
    if global_state.LOGGING_ENABLED:
        logger.info(f':st:🌞🌞🌞🌞🌞 4.5.26 15:17 Mon 🌞🌞🌞🌞🌞🌞🌞 tmp_dir={tmp_dir_aura}')

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

        # --- LT (cached) + MAP Kombinationen ---
        case('Sebastian mit nachnamen', 'Sebastian mit Nachnamen',
             'LT (cached) Uppercase. may check --> FUZZY_MAP_pre.py', lt=True, prio=TestPrio.HIGH),
        case(input_text='null', expected='0', context='MAP git', lt=False, prio=TestPrio.OPTIONAL),
        case(input_text='über die konsole zu bedienen', expected='Über die Konsole zu bedienen', context='git', lt=True,
             prio=TestPrio.HIGH),
        case(input_text='geht cobit', expected='git commit', context='FUZZY_MAP_pre git', lt=False, prio=TestPrio.OPTIONAL),

        # --- en-US ---
        case('colours', 'colors', 'fix by LT (cached)', lang='en-US', lt=True, prio=TestPrio.OPTIONAL),
        case('underilnes', 'underlines', 'fix by LT (cached)', lang='en-US', lt=True, prio=TestPrio.OPTIONAL),
        case('too have', 'to have', 'fix by LT (cached)', lang='en-US', lt=True, prio=TestPrio.ALWAYS),
        case('5 PM in the afternoon', '5 PM', 'fix by LT (cached)', lang='en-US', lt=True, prio=TestPrio.HIGH),
        case('good nigt Mum', 'Good night Mum', 'Funny useless rule ;) just for testing', lang='en-US', lt=True,
             prio=TestPrio.ALWAYS),
        case('thousand dollars.', '1000 dollars.', 'Number with unit', lang='en-US', lt=False, prio=TestPrio.HIGH),
        case('one and thousand dollars.', '1 and 1000 dollars.', 'Number with unit', lang='en-US', lt=False, prio=TestPrio.ALWAYS),

        # --- de-DE MAP + LT (cached) ---
        case('tausend euro. Und euro großgeschrieben.', r'1000 Euro\. Und Euro großgeschrieben.',
             'Number with unit', lt=True, prio=TestPrio.HIGH),
        case('lieblingszahlen sind fünf und drei', 'Lieblingszahlen sind 5 und 3', 'numbers 5 and 3', lt=True, prio=TestPrio.ALWAYS),
        case('was ist fünf plus drei', r'Das Ergebnis von 5 plus 3 ist 8\.', 'calc in MAP Wannweil', lt=False, prio=TestPrio.ALWAYS),
        case('wie ist das wetter', r'Aktuell in \w+ sind es.*', 'weather plugin', lt=False, prio=TestPrio.ALWAYS),
        case('bitte reservieren sie einen tisch für zwei personen um acht uhr',
             'Bitte reservieren Sie einen Tisch für 2 Personen um 8 Uhr',
             'Polite request with time and number', lt=True, prio=TestPrio.HIGH),

        # --- Zahlen ---
        case('eins', '1', 'numbers_to_digits', lt=False, prio=TestPrio.OPTIONAL),
        case('eins zwei', '12', 'numbers_to_digits', lt=False, prio=TestPrio.ALWAYS),
        case('sieben acht neun', '789', 'numbers_to_digits', lt=False, prio=TestPrio.OPTIONAL),
        case('zwei zwei', '22', 'Multiple replacement check', lt=False, prio=TestPrio.OPTIONAL),
        case('sieben', '7', 'Numbers as digits', lt=False, prio=TestPrio.OPTIONAL),
        case('acht', '8', 'Numbers as digits', lt=False, prio=TestPrio.OPTIONAL),
        case('neun', '9', 'Numbers as digits', lt=False, prio=TestPrio.OPTIONAL),
        case('zehn', '10', 'Number as digit', lt=False, prio=TestPrio.OPTIONAL),
        case('komma', ',', 'Exact MAP punctuation', lt=False, prio=TestPrio.OPTIONAL),
        case('fünf komma', '5 ,', 'Decimal number', lt=False, prio=TestPrio.HIGH),
        case('fünf komma drei', '5 , 3', 'Decimal number', lt=False, prio=TestPrio.OPTIONAL),

        # --- Grundlegende Satzzeichen ---
        case('punkt', r'\.', 'Exact MAP .', lt=False, prio=TestPrio.OPTIONAL),
        case('fragezeichen', r'\?', 'Exact MAP ?', lt=False, prio=TestPrio.HIGH),
        case('ausrufezeichen', '!', 'Exact MAP !', lt=False, prio=TestPrio.HIGH),
        case('doppelpunkt', ':', 'Exact MAP :', lt=False, prio=TestPrio.HIGH),
        case('semikolon', ';', 'Exact MAP ;', lt=False, prio=TestPrio.HIGH),
        case('bindestrich', r'\-', 'Exact MAP -', lt=False, prio=TestPrio.HIGH),
        case('gedankenstrich', '–', 'Exact MAP --', lt=False, prio=TestPrio.HIGH),
        case('klammer auf', r'\(', 'Exact MAP (', lt=False, prio=TestPrio.HIGH),
        case('klammer zu', r'\)', 'Exact MAP )', lt=False, prio=TestPrio.HIGH),

        # --- MAP Wannweil ---
        case('Sekunde Lauffer', 'Sigune Lauffer', 'MAP Wannweil', lt=False, prio=TestPrio.OPTIONAL),
        case('Sekunde lauf war', 'Sigune Lauffer war', 'MAP Wannweil', lt=False, prio=TestPrio.HIGH),

        # --- Partial MAP + LT (cached) ---
        case('mit nachnamen laufer', 'Mit Nachnamen Lauffer', 'Partial map + LT (cached)', lt=True, prio=TestPrio.HIGH),
        case('Sebastian mit nachnamen', 'Sebastian mit Nachnamen', 'Partial map + LT (cached)', lt=True, prio=TestPrio.HIGH),
        case('von sebastian laufer', 'Von Sebastian Lauffer', 'Partial map + LT (cached)', lt=True, prio=TestPrio.HIGH),
        case('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT (cached)', lt=True, prio=TestPrio.HIGH),
        case('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', lt=False, prio=TestPrio.OPTIONAL),

        # --- FUZZY_MAP_pre ---
        case('git at', 'git add .', 'Fuzzy map REGEX match', lt=False, prio=TestPrio.OPTIONAL),
        case('geht status', 'git status', 'Fuzzy map FUZZY string', lt=False, prio=TestPrio.ALWAYS),
        case('geht cobit', 'git commit', 'FUZZY_MAP_pre', lt=False, prio=TestPrio.OPTIONAL),

        # --- Großschreibung via LT (cached) ---
        case('ich heiße max', 'Ich heiße Max', 'Capitalization pronoun + proper noun', lt=True, prio=TestPrio.HIGH),
        case('der hund bellt', 'Der Hund bellt', 'Capitalization article + noun', lt=True, prio=TestPrio.OPTIONAL),
        case('die katze schläft', 'Die Katze schläft', 'Capitalization article + noun', lt=True, prio=TestPrio.HIGH),
        case('ein haus und ein garten', 'Ein Haus und ein Garten', 'Capitalization nouns', lt=True, prio=TestPrio.HIGH),
        case('heute ist montag', 'Heute ist Montag', 'Capitalization day', lt=True, prio=TestPrio.OPTIONAL),
        case('heute ist ein schöner tag', 'Heute ist ein schöner Tag', 'Capitalization day', lt=True, prio=TestPrio.HIGH),
        case('heute ist ein schöner tag zwei drei', 'Heute ist ein schöner Tag 23','Capitalization + number', lt=True, prio=TestPrio.HIGH),
        case('zwei drei hunde sind im wald', '23 Hunde sind im Wald', 'Number at start + LT (cached)', lt=True, prio=TestPrio.OPTIONAL),
        case('die antwort ist ein test', 'Die Antwort ist ein Test', 'Window filter provocation', lt=True, prio=TestPrio.HIGH),
        case('im sommer ist es warm', 'Im Sommer ist es warm', 'Capitalization season', lt=True, prio=TestPrio.HIGH),

        # --- Häufige Phrasen ---
        case('danke schön', 'Danke schön', 'Common thanks', lt=True, prio=TestPrio.HIGH),
        case('bitte schön', 'Bitte schön', 'Common courtesy', lt=True, prio=TestPrio.HIGH),
        case('entschuldigung', 'Entschuldigung', 'Common apology', lt=True, prio=TestPrio.HIGH),
        case('ich verstehe', 'Ich verstehe', 'Common confirmation', lt=True, prio=TestPrio.ALWAYS),
        case('ich weiß nicht', 'Ich weiß nicht', 'Common uncertainty', lt=True, prio=TestPrio.HIGH),
        case('alles klar', 'Alles klar', 'Common affirmation', lt=True, prio=TestPrio.HIGH),
        case('auf wiedersehen', 'Auf Wiedersehen', 'Common farewell', lt=True, prio=TestPrio.HIGH),
        case('bis später', 'Bis später', 'Common farewell', lt=True, prio=TestPrio.HIGH),
        case('es ist kalt draußen', 'Es ist kalt draußen', 'Simple sentence', lt=True, prio=TestPrio.HIGH),
        case('was machst du heute', 'Was machst du heute', 'Common question', lt=True, prio=TestPrio.HIGH),
        case('kein problem', 'Kein Problem', 'Common phrase', lt=True, prio=TestPrio.HIGH),
        case('zum beispiel', 'Zum Beispiel', 'Common phrase', lt=True, prio=TestPrio.HIGH),
        case('und so weiter', 'Und so weiter', 'Common phrase', lt=True, prio=TestPrio.HIGH),
        case('einer nach dem anderen', 'Einer nach dem anderen', 'Idiomatic', lt=True, prio=TestPrio.HIGH),

        # --- Umlaute ---
        case('schön', 'schön', 'Umlaut – unverändert', lt=False, prio=TestPrio.HIGH),
        case('überall', 'überall', 'Umlaut – unverändert', lt=False, prio=TestPrio.HIGH),
        case('für', 'für', 'Umlaut – unverändert', lt=False, prio=TestPrio.HIGH),
        case('größer', 'größer', 'Umlaut+Eszett – unverändert', lt=False, prio=TestPrio.HIGH),
        case('weiß', 'weiß', 'Eszett – unverändert', lt=True, prio=TestPrio.HIGH),
        case('müde', 'müde', 'Umlaut – unverändert', lt=True, prio=TestPrio.HIGH),
        case('straße', 'Straße', 'Eszett + Großschreibung', lt=True, prio=TestPrio.HIGH),
        case('füße', 'Füße', 'Umlaut + Großschreibung', lt=True, prio=TestPrio.HIGH),
        case('hände', 'Hände', 'Umlaut + Großschreibung', lt=True, prio=TestPrio.HIGH),

        # --- Abkürzungen ---
        case('respektive', 'respektive', 'unverändert', lt=False, prio=TestPrio.HIGH),
        case('circa', 'circa', 'unverändert', lt=False, prio=TestPrio.HIGH),
        case('unter anderem', 'Unter anderem', 'Common abbreviation', lt=True, prio=TestPrio.HIGH),
        case('doktor', 'Doktor', 'Title abbreviation', lt=True, prio=TestPrio.HIGH),
        case('professor', 'Professor', 'Title abbreviation', lt=True, prio=TestPrio.HIGH),
        case('zum schluss', 'Zum Schluss', 'Custom abbreviation', lt=True, prio=TestPrio.HIGH),

        # --- Fragen und Ausrufe ---
        case('wie spät ist es', 'Wie spät ist es', 'Direct question', lt=True, prio=TestPrio.HIGH),
        case('wo finde ich toilette', 'Wo finde ich Toilette', 'Direct question', lt=True, prio=TestPrio.HIGH),
        case('das ist unglaublich', 'Das ist unglaublich', 'Exclamatory', lt=True, prio=TestPrio.HIGH),
        case('hilfe', 'Hilfe', 'word', lt=True, prio=TestPrio.HIGH),
        case('was für ein tag', 'Was für ein Tag', 'Exclamatory phrase', lt=True, prio=TestPrio.HIGH),
        case('stopp', 'stopp', 'unverändert', lt=False, prio=TestPrio.HIGH),

        # --- Befehle ---
        case('gehe nach links', 'Gehe nach links', 'Simple command: gehe nach links', lt=True, prio=TestPrio.HIGH),
        case('schalte das licht ein', 'Schalte das Licht ein', 'Simple command: schalte das licht ein', lt=True, prio=TestPrio.HIGH),
        case('öffne die tür', 'Öffne die Tür', 'Simple command', lt=True, prio=TestPrio.HIGH),
        case('wiederhole das bitte', 'Wiederhole das bitte', 'Request', lt=True, prio=TestPrio.HIGH),

        # --- Komplexere Sätze ---
        case('die sonne scheint auf die blumen', 'Die Sonne scheint auf die Blumen',
             'Compound sentence', lt=True, prio=TestPrio.HIGH),
        case('obwohl es regnet ist die stimmung gut', 'Obwohl es regnet, ist die Stimmung gut',
             'Subordinate clause + comma', lt=True, prio=TestPrio.OPTIONAL),
        case('der kleine hund spielt mit seinem neuen spielzeug',
             'Der kleine Hund spielt mit seinem neuen Spielzeug',
             'Detailed sentence', lt=True, prio=TestPrio.HIGH),
        case('das wetter wird morgen sonnig mit temperaturen um die zwanzig grad',
             'Das Wetter wird morgen sonnig mit Temperaturen um die 20 Grad',
             'digits_to_numbers + LT (cached)', lt=True, prio=TestPrio.HIGH),
    ]


    # test_cases = [
    #     # ('was is 5 mal 1', 'Das Ergebnis von 5 mal 2 ist 10.', 'Partial map + LT (cached) correction', 'de-DE'),
    #     ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT (cached) correction', 'de-DE'),
    # ]

    # 1. Filter test cases for the current language
    PRIO_CHANCE = {
        TestPrio.ALWAYS: 1.0,
        TestPrio.HIGH: 0.8,
        TestPrio.OPTIONAL: 0.3,
        TestPrio.NEVER: 0.0,
    }
    import random


    if is_ci:
        rng = random.Random(42) # deterministic for reproducible runs
    else:
        rng = random.Random()

    active_tests = []
    skipped_lt_count = 0
    for test_case in test_cases:
        raw_text, expected, description, check_lang, use_lt, prio = test_case
        if check_lang != lang_code:
            continue
        if is_ci and use_lt:
            skipped_lt_count += 1
            continue  # Skip lt in CI
        if is_ci:
            chance = 1
        else:
            chance = PRIO_CHANCE.get(prio, 0.0)
        if rng.random() <= chance:
            active_tests.append((raw_text, expected, description, use_lt))
            # if not is_ci:logger.info(f':st:🌞🌞🌞🌞🌞 append({raw_text}, {expected})')

    if is_ci:

        print(f":st: DEBUG lang_code={lang_code} active_tests={len(active_tests)}")
        if global_state.LOGGING_ENABLED:
            logger.info(f':st: DEBUG active_tests count={len(active_tests)}')

    if is_ci:
        print(f':st: DEBUG active_tests count={len(active_tests)}')



    if global_state.LOGGING_ENABLED:
        logger.info(f":st:Running {len(active_tests)} tests in parallel using PROCESSES...")

    # 3. Parallel Execution
    passed_count = 0
    failed_count = 0

    import multiprocessing
    if is_ci:
        print(":st: DEBUG multiprocessing imported")

    os.environ["AURA_SELF_TEST_RUNNING"] = "1"  # inherited by fork
    start_time = time.perf_counter()
    # ctx = multiprocessing.get_context("fork")
    if is_ci:
        print(":st: DEBUG before ctx fork")
    ctx = multiprocessing.get_context("fork")
    if is_ci:
        print(f":st: DEBUG ctx={ctx} os.cpu_count()={os.cpu_count()}")
    num_workers = os.cpu_count()
    if is_ci:
        print(f":st: DEBUG ctx={ctx} num_workers={num_workers}")

    lt_tests = [(r, e, d, True) for r, e, d, use_lt in active_tests if use_lt]
    if is_ci:
        print(f":st: DEBUG lt_tests={len(lt_tests)}")

    non_lt_tests = [(r, e, d, False) for r, e, d, use_lt in active_tests if not use_lt]
    if is_ci:
        print(f":st: DEBUG lt_tests={len(lt_tests)} non_lt_tests={len(non_lt_tests)}")

    if global_state.LOGGING_ENABLED:
        logger.info(f":st: Phase 1 – {len(non_lt_tests)} deterministic tests (max_workers={num_workers})")
        logger.info(f":st: Phase 2 – {len(lt_tests)} LT-dependent tests   (max_workers=2)")

    test_metrics = []
    if is_ci:
        print(":st: DEBUG before _collect_results def")

    def _collect_results(futures_map):
        nonlocal passed_count, failed_count
        if is_ci:
            print(f":st: DEBUG collecting {len(futures_map)} results...")
        for future in concurrent.futures.as_completed(futures_map):
            if is_ci:
                print(":st: DEBUG future completed, getting result...")
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
                    if global_state.LOGGING_ENABLED:
                        logger.info(
                        f":st: ==> Passed: {passed_count}, Failed: {failed_count} ==> :) its oky no problem. try it better next time ;)")
            except Exception as e:
                failed_count += 1
                print(f":st: Process crashed: {e}")

    lt_workers = 1 if is_ci else num_workers

    if is_ci:
        print(f":st: DEBUG before Pool1: lt_workers = {lt_workers} , non_lt_tests={len(non_lt_tests)}")
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers, mp_context=ctx) as executor:
        futures = {}
        for i, t in enumerate(non_lt_tests):
            futures[executor.submit(run_single_test_process, i, t, lang_code, lt_url, str(test_base_dir))] = t
        _collect_results(futures)
    if is_ci:
        print(":st: DEBUG behind Pool1")

    with concurrent.futures.ProcessPoolExecutor(max_workers=lt_workers, mp_context=ctx) as executor:
        futures = {}
        for i, t in enumerate(lt_tests, start=len(non_lt_tests)):
            futures[executor.submit(run_single_test_process, i, t, lang_code, lt_url, str(test_base_dir))] = t
        _collect_results(futures)



    if not settings.LOG_in_selftest:
        global_state.LOGGING_ENABLED = True




    # scripts/py/func/checks/self_tester.py:420

    # 4.1 Detailed Performance Report at the very end
    if global_state.LOGGING_ENABLED:
        logger.info("=" * 40)
    # if not is_ci:
    logger.info(":st: PERFORMANCE REPORT (Slowest tests first):")
    if global_state.LOGGING_ENABLED:
        logger.info(f":st: {'STAT':<5} | {'TIME':<8} | {'LT':<4} | {'DESCRIPTION':<40} | {'INPUT'}")
    # Sort by duration descending
    sorted_metrics = sorted(test_metrics, key=lambda x: x['duration'], reverse=True)

    for m in sorted_metrics:
        status = "✅" if m['success'] else "❌"
        lt_flag = "LT" if m['use_lt'] else "--"
        if global_state.LOGGING_ENABLED:
            logger.info(f":st: {status:<1} | {m['duration']:>6.3f}s | {lt_flag:<2} | {m['desc'][:40]:<40} | '{m['input']}'")


    if global_state.LOGGING_ENABLED:
        logger.info("=" * 40)

    ci_hint = f" ({skipped_lt_count} LT (cached)-tests skipped in CI)" if is_ci and skipped_lt_count else ""


    # 4.2 Summary
    duration = time.perf_counter() - start_time
    if global_state.LOGGING_ENABLED:
        logger.info("=" * 40)
    # m1 =f"✅ of {len(test_cases)} are {len(active_tests)} tested, passed: {passed_count} | ❌ Failed: {failed_count}"
    if failed_count > 0:
        if global_state.LOGGING_ENABLED:
            # logger.info(
            # f":st: {len(active_tests)} of {len(test_cases)} tests active  |  ✅ Passed: {passed_count}  |  ❌ Failed: {failed_count}  (hint: search ❌ FAIL)")
            ci_hint = f" ({skipped_lt_count} LT (cached)-tests skipped in CI)" if is_ci and skipped_lt_count else ""
            logger.info(
                f":st: {len(active_tests)} of {len(test_cases)} tests active{ci_hint} |  ✅ Passed: {passed_count}  |  ❌ not passed: {failed_count}  (hint: search ❌ FAIL)")

            # logger.info(f":st:✅ of {len(test_cases)} are {len(active_tests)} tested, Passed: {passed_count} | ❌ not passed: {failed_count} Tests (hint search for: ❌ FAIL )")
        else:
            print(f":st: {len(active_tests)} of {len(test_cases)} tests active{ci_hint} Passed: {passed_count} | ❌ not passed: {failed_count} Tests (hint search for: ❌ FAIL )")
    else:
        msg = f":st: {len(active_tests)} of {len(test_cases)} tests active{ci_hint} ✅ Passed: all {passed_count} ✅ | {failed_count} not passed 🙂"
        logger.info(msg)
        print(msg)

    second_per_test = duration / len(active_tests)
    max_local = 0.078
    threshold = max_local * (10.0 if is_ci else 1.0)
    if second_per_test > threshold:
        m1 = f"🛑 ALERT tests_per_second: expected second per test  <= {max_local}, got {second_per_test:.3f} second per test"
        m2 = "🛑 mostly it was 6.45 to 7 seconds per 92 tests. Check README variable for more info."
        logger.critical(f"{m1} {m2}")
        if global_state.LOGGING_ENABLED:
            logger.info(f"{m1} {m2}")

        if second_per_test > 3 * threshold and not os.getenv('CI'):
            m1 = f"🛑 its DOUBLE of expected second per test, got {second_per_test:.3f} second per test. that maybe happens at the first run when RAM is clear"
            m2 = "🛑 ==> exit"
            logger.critical(f"{m1} {m2}")
            if global_state.LOGGING_ENABLED:
                logger.info(f"{m1} {m2}")
            # sys.exit(1)


    m2=f"⌚ Total Duration: {duration:.2f} seconds (second_per_test:{second_per_test:.2f} s/test)"
    if global_state.LOGGING_ENABLED:
        logger.info(f"pid:{os.getpid()} :st:{m2}")
    speak_inclusive_fallback(f"{m2}", 'de-DE') # 'en-US') # 'de-DE')

    import threading
    thread_name = threading.current_thread().name
    if global_state.LOGGING_ENABLED:
        logger.info(f"- {thread_name} :st:⌚ maybe check: run_always_no_throttling_ignore_times = True/False ?")
    if global_state.LOGGING_ENABLED:
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
    """ # noqa:F841

    if False and not is_ci:
        logger.info("-" * 40)
        formatted_readme = "\n".join([f"📜 {line}" for line in README.strip().splitlines()])
        logger.info(f"History:\n{formatted_readme}")

    # if not is_ci:logger.info(f"History:\n{formatted_readme}")

    settings.PLUGIN_HELPER_TTS_ENABLED = backup_tts_enabled

    # scripts/py/func/checks/self_tester.py:434
    # core_logic_self_test_is_running_FILE.unlink(missing_ok=True)

    core_logic_self_test_is_running_file = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"
    core_logic_self_test_is_running_file.unlink(missing_ok=True)


    if failed_count > 0:
        print(f':st: failed_count > 0: {failed_count} ==> exiting')
        if is_ci == 'true':
            sys.exit(1)

        # sys.exit(1)


# futures = {executor.submit(run_single_test, i, t, lang_code, lt_url, str(test_base_dir)): t
#            for i, t in enumerate(active_tests)}


import sys
import os
import time
# import traceback
# from pathlib import Path

warnings.filterwarnings("ignore", category=RuntimeWarning, module="psutil")

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

    def __getattr__(self, name): return lambda *args, **kwargs: None
    def __repr__(self): return ""

# if somebody is confused send him:
# find . -name "*settings.py"                                                                                                                                     ✔

def run_single_test_process(index, test_data, lang_code, lt_url, test_base_dir_str):

    # 1. CI-spezifische Noise-Unterdrückung
    if is_ci:
        os.environ["PSUTIL_DEBUG"] = "0"

    start_individual = time.perf_counter()
    raw_text, expected, description, use_lt = test_data

    try:
        worker_dir = Path(test_base_dir_str) / f"task_{index}"
        worker_dir.mkdir(parents=True, exist_ok=True)

        # 2. Output-Umleitung nur in der CI
        stack = contextlib.ExitStack()
        if is_ci:
            fnull = stack.enter_context(open(os.devnull, 'w'))
            stack.enter_context(contextlib.redirect_stdout(fnull))
            stack.enter_context(contextlib.redirect_stderr(fnull))

        with stack:
            null_logger = SimpleNullLogger()
            unique_time_float = (time.time_ns() + index) / 1_000_000_000.0

            process_text_in_background(
                null_logger, lang_code, raw_text,
                None,
                unique_time_float, lt_url,
                output_dir_override=worker_dir,
                session_id=index,
                chunk_id=1
            )

            output_files = list(worker_dir.glob("tts_output_*.txt"))
            if not output_files:
                duration = time.perf_counter() - start_individual
                return False, raw_text, "[NO_FILE]", expected, description, duration, use_lt

            result_file = output_files[0]
            with open(result_file, 'r', encoding='utf-8-sig') as f:
                actual = f.read().strip()

            # --- ORIGINAL SIGNATUR-BEREINIGUNG START ---
            if hasattr(settings, 'signatur1'):
                actual = actual.replace(settings.signatur1, '')
            if hasattr(settings, 'signatur'):
                actual = actual.replace(settings.signatur, '')
            actual = actual.strip()

            # Zusätzlicher Cut-off für Symbole (wie in deinem Original)
            pattern = r"(🗣|\-\-)"
            m = re.search(pattern, actual)
            if m:
                actual = actual[:m.start()].strip()
            # --- ORIGINAL SIGNATUR-BEREINIGUNG ENDE ---

            # Aufräumen
            try:
                os.remove(result_file)
                worker_dir.rmdir()
            except Exception:
                pass
            duration = time.perf_counter() - start_individual
            return bool(re.fullmatch(expected, actual)), raw_text, actual, expected, description, duration, use_lt

    except Exception as e791:
        import traceback
        duration = time.perf_counter() - start_individual
        return False, "ERROR", f"{e791}\n{traceback.format_exc()}", expected, description, duration, use_lt

def run_single_test_202501311853(logger, index, test_data, lang_code, lt_url, test_base_dir):
    raw_text, expected, description = test_data

    # Create a UNIQUE folder for this specific test case
    # This is the ONLY way to prevent threads from stealing each other's files
    worker_dir = test_base_dir / f"task_{index}"
    worker_dir.mkdir(parents=True, exist_ok=True)

    print(':st:scripts/py/func/checks/self_tester.py:497 🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞🌞')

    try:
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
        return bool(re.fullmatch(expected, actual)), raw_text, actual, expected2, description

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
    test_logger.propagate = False # no dopple Logs

    tmp_path = Path("/tmp/sl5_aura")
    tmp_path.mkdir(parents=True, exist_ok=True)

    root_file = tmp_path / "sl5net_aura_project_root"
    if not root_file.exists():
        root_file.write_text(str(Path.cwd().absolute()))



    lt_url = "http://localhost:8082"
    lang = "de-DE"

    from ..process_text_in_background import load_maps_for_language
    load_maps_for_language(lang, test_logger)

    print(f":st: Starting self-test (CLI mode) using {lt_url}...")
    try:
        run_core_logic_self_test(test_logger, tmp_path, lt_url, lang)
    except Exception as e:
        print(f":st: CRITICAL ERROR: {e}")
        sys.exit(1)
