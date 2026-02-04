# scripts/py/func/checks/self_tester.py
import re
import concurrent.futures
import sys
# import concurrent.futures
import os
from pathlib import Path

from ..audio_manager import speak_fallback

def check_translator_hijack_is_active(logger):

    proj_dir = Path(__file__).parents[4]
    path = proj_dir / "config"  / "maps" / "plugins" / "standard_actions" / "language_translator" / "de-DE" / "FUZZY_MAP_pre.py"

    if not path.exists():
        logger.info(f"HIJACK: path {path} not exists!")
        return False

    pattern = re.compile(r"#[ ]*TRANSLATION_RULE[ ]*\n[^\n]*#")
    for lineno, line in enumerate(path.read_text().splitlines(), start=1):
        if pattern.search(line):
            logger.info(f"🚨 HIJACK: Rule in ..{str(path)[-30:]}{lineno} is active!")
            return lineno

    return False

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Note: In aura_engine.py this might be SCRIPT_DIR instead of project_root

from scripts.py.func.process_text_in_background import process_text_in_background
from scripts.py.func.checks.run_function_with_throttling import run_function_with_throttling
from ..config.dynamic_settings import DynamicSettings
settings = DynamicSettings()

# def get_logger_file_path(logger_instance):
    # "Retrieves the Path object for the first FileHandler."""
    # for handler in logger_instance.handlers:
    #     if isinstance(handler, FileHandler):
    #         return Path(handler.baseFilename)
    # return None

# def simple_clear_log(log_path: Path):
#     """
#     Clears the log file using 'w' mode.
#     NOTE: This does NOT close the logger handler, risking a race condition.
#     """
#     if log_path is None:
#         print("Error: No log file path found.")
#         return
#
#     try:
#         # Open in write mode ('w') to truncate the file
#         with open(log_path, 'w', encoding='utf-8'):
#             pass
#         print(f"Log '{log_path}' cleared successfully.")
#     except Exception as e:
#         # This catch handles FileNotFoundError and PermissionError/Lock issues
#         print(f"Warning: Could not clear log file {log_path}. Error: {e}", file=sys.stderr)


# file: scripts/py/func/checks/self_tester.py:50
def run_core_logic_self_test(logger, tmp_dir: Path, lt_url, lang_code):
    """
    Runs a series of predefined tests, guarded by a persistent throttle mechanism.
    """
    # config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py
    lineno = check_translator_hijack_is_active(logger)
    if lineno and lineno>0:
        logger.info(f"self_tester.py exit exit exit")
        logger.info(f"""
        75:🚨 HIJACK: rule is activ during self_test! maybe check: 
        config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py:{lineno} 
        (check_translator_hijack) --> exit(1)
        """)
        exit(1)



    # 1. Collect all parameters needed by _execute_self_test_core
    core_params = {
        'logger': logger,
        'tmp_dir': tmp_dir,
        'lt_url': lt_url,
        'lang_code': lang_code
    }

    # 2. Call the generic wrapper function

    test_executed = run_function_with_throttling(
        logger,
        state_dir=tmp_dir,
        core_logic_function=_execute_self_test_core,
        func_params=core_params,
        state_file_name="self_test_throttle_state.json"  # Provide a specific file name for this function
    )

    if not test_executed:
        logger.warning("Self-test skipped due to persistent throttling.")

    return test_executed

# helper for use named Parameters
def case(input_text, expected, context='', lang='de-DE'):
    return (input_text, expected, context, lang)

# file: scripts/py/func/checks/self_tester.py:79

# import concurrent.futures


def _execute_self_test_core_202601311804(logger, tmp_dir, lt_url, lang_code):

    test_output_dir = tmp_dir / "sl5_aura_self_test"
    test_output_dir.mkdir(parents=True, exist_ok=True)


    settings = DynamicSettings()

    backup_tts_enabled = settings.PLUGIN_HELPER_TTS_ENABLED
    settings.PLUGIN_HELPER_TTS_ENABLED = False

    # Base directory for all tests
    test_base_dir = tmp_dir / "sl5_aura_self_test"
    test_base_dir.mkdir(parents=True, exist_ok=True)


    test_cases = [

        # case(input_text='->SPEECH_PAUSE_TIMEOUT<-', expected=f"{SPEECH_PAUSE_TIMEOUT_021}", context='proff if we can change settings 2026-0104-1435'),

        #     ('lehrwart', 'leerworttest1'),
        case(input_text='leerworttest', expected=f"leerworttest1", context='punctation map test', lang='de-DE'),

        case(input_text='->AUDIO_INPUT_DEVICE<-', expected=f"SYSTEM_DEFAULT",
             context='proff if we can change settings 2026-0104-1435'),
        # case(input_text='->SPEECH_PAUSE_TIMEOUT<-', expected='7890', context='proff if we can change settings 2026-0104-1435'),

        ('Sebastian mit nachnamen', 'Sebastian mit Nachnamen',
         'LT Uppercase. \n may check --> config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py',
         'de-DE'),

        case(input_text='null', expected='0', context='git'),
        case(input_text='über die konsole zu bedienen', expected='über die konsole zu bedienen', context='git'),
        case(input_text='geht cobit', expected='git commit', context='git'),
        ('geht staates', 'git status', '19.11.25 10:19 Wed', 'de-DE'),
        ('ausrufezeichen', '!', 'Exact MAP match for punctuation', 'de-DE'),

        # following differ when daytime chaning:
        # ('good Morning people', 'hey all out there people', 'use a postRule. Funny useless rule ;) just for testing','en-US'),
        ('colours', 'colors', 'fix by LT', 'en-US'),
        ('underilnes', 'underlines', 'fix by LT', 'en-US'),
        ('too have', 'to have', 'fix by LT', 'en-US'),
        ('colours', 'colors', 'fix by LT', 'en-US'),
        ('5 PM in the afternoon', '5 PM', 'fix by LT', 'en-US'),

        ('good nigt Mum', 'Good night Mum', 'Funny useless rule ;) just for testing',
         'en-US'),

        # good evening dead Good evening them Good evening ought to get

        ('thousand dollars.', '1000 dollars.', 'Number with unit',
         'en-US'),
        ('one and thousand dollars.', '1 and 1000 dollars.', 'Number with unit',
         'en-US'),

        ('tausend euro. Und euro großgeschrieben.', '1000 Euro. Und Euro großgeschrieben.', 'Number with unit',
         'de-DE'),

        ('was ist 5 plus 3', 'Das Ergebnis von 5 plus 3 ist 8.', 'calc in MAP Wannweil', 'de-DE'),

        ('bitte reservieren sie einen tisch für zwei personen um acht uhr',
         'Bitte reservieren Sie einen Tisch für 2 Personen um 8 Uhr', 'Polite request with time and number',
         'de-DE'),
        ('eins', '1', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),
        ('eins zwei', '1 2', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),

        ('Sekunde Lauffer', 'Sigune Lauffer', 'MAP Wannweil', 'de-DE'),
        ('mit nachnamen laufer', 'Mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('Sebastian mit nachnamen', 'Sebastian mit Nachnamen', 'Partial map + LT correction', 'de-DE'),
        ('von sebastian laufer', 'Von Sebastian Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('punkt', '.', 'Exact MAP match', 'de-DE'),
        ('komma', ',', 'Exact MAP match'),
        # ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        ('git at', 'git add .', 'Fuzzy map REGEX match', 'de-DE'),
        ('geht status', 'git status', 'Fuzzy map FUZZY string match', 'de-DE'),
        ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', 'de-DE'),
        ('Sekunde lauf war', 'Sigune Lauffer war', 'MAP Wannweil', 'de-DE'),

        # --- Grundlegende Satzzeichen ---
        ('punkt', '.', 'Exact MAP match for punctuation', 'de-DE'),
        ('komma', ',', 'Exact MAP match for punctuation', 'de-DE'),
        ('fragezeichen', '?', 'Exact MAP match for punctuation', 'de-DE'),
        ('ausrufezeichen', '!', 'Exact MAP match for punctuation', 'de-DE'),
        ('doppelpunkt', ':', 'Exact MAP match for punctuation', 'de-DE'),
        ('semikolon', ';', 'Exact MAP match for punctuation', 'de-DE'),
        ('bindestrich', '-', 'Exact MAP match for punctuation', 'de-DE'),
        ('gedankenstrich', '–', 'Exact MAP match for punctuation', 'de-DE'),  # Oder '-' je nach gewünschtem Output
        ('klammer auf', '(', 'Exact MAP match for punctuation', 'de-DE'),
        ('klammer zu', ')', 'Exact MAP match for punctuation', 'de-DE'),

        # --- Groß- und Kleinschreibung (Satzanfang, Nomen) ---
        # ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        # ('guten morgen', 'Guten Morgen', 'Capitalization of greeting and noun', 'de-DE'),
        ('ich heiße max', 'Ich heiße Max', 'Capitalization of pronoun and proper noun', 'de-DE'),
        ('der hund bellt', 'Der Hund bellt', 'Capitalization of article and noun', 'de-DE'),
        ('die katze schläft', 'Die Katze schläft', 'Capitalization of article and noun', 'de-DE'),
        ('ein haus und ein garten', 'Ein Haus und ein Garten', 'Capitalization of nouns', 'de-DE'),
        ('heute ist montag', 'Heute ist Montag', 'Capitalization of day of the week', 'de-DE'),
        ('im sommer ist es warm', 'Im Sommer ist es warm', 'Capitalization of season', 'de-DE'),

        # --- Zahlen und Ziffern ---
        ('sieben', '7', 'Numbers as digits', 'de-DE'),
        ('acht', '8', 'Numbers as digits', 'de-DE'),
        ('neun', '9', 'Numbers as digits', 'de-DE'),
        ('zehn', '10', 'Number as digit', 'de-DE'),
        # ('zweitausendunddreiundzwanzig', '2023', 'Year as digit', 'de-DE'),
        ('fünf komma', '5 ,', 'Decimal number', 'de-DE'),
        # ('minus drei', '- 3', 'Negative number', 'de-DE'),

        # --- Häufige Wörter und Phrasen ---
        # ('hallo wie geht es dir', 'Hallo, wie geht es dir', 'Common greeting and question', 'de-DE'),
        ('danke schön', 'Danke schön', 'Common thanks', 'de-DE'),
        ('bitte schön', 'Bitte schön', 'Common courtesy', 'de-DE'),
        ('entschuldigung', 'Entschuldigung', 'Common apology', 'de-DE'),
        ('ich verstehe', 'Ich verstehe', 'Common confirmation', 'de-DE'),
        ('ich weiß nicht', 'Ich weiß nicht', 'Common uncertainty', 'de-DE'),
        ('alles klar', 'Alles klar', 'Common affirmation', 'de-DE'),
        ('auf wiedersehen', 'Auf Wiedersehen', 'Common farewell', 'de-DE'),
        ('bis später', 'Bis später', 'Common farewell', 'de-DE'),
        # ('ja genau', 'Ja, genau', 'Affirmation with comma', 'de-DE'),
        # ('nein danke', 'Nein, danke', 'Refusal with thanks', 'de-DE'),
        ('es ist kalt draußen', 'Es ist kalt draußen', 'Simple descriptive sentence', 'de-DE'),
        ('was machst du heute', 'Was machst du heute', 'Common question', 'de-DE'),
        ('kein problem', 'Kein Problem', 'Common phrase', 'de-DE'),
        ('zum beispiel', 'Zum Beispiel', 'Common phrase', 'de-DE'),
        ('und so weiter', 'Und so weiter', 'Common phrase', 'de-DE'),
        ('einer nach dem anderen', 'Einer nach dem anderen', 'Idiomatic expression', 'de-DE'),

        # --- Wörter mit Umlauten und Sonderzeichen ---
        ('schön', 'schön', 'Word with Umlaut', 'de-DE'),
        ('überall', 'überall', 'Word with Umlaut', 'de-DE'),
        ('für', 'für', 'Word with Umlaut', 'de-DE'),
        ('größer', 'größer', 'Word with Umlaut and Eszett', 'de-DE'),
        ('straße', 'Straße', 'Word with Eszett and capitalization', 'de-DE'),
        ('weiß', 'weiß', 'Word with Eszett', 'de-DE'),
        ('füße', 'Füße', 'Word with Umlaut and capitalization', 'de-DE'),
        ('müde', 'müde', 'Word with Umlaut', 'de-DE'),
        ('hände', 'Hände', 'Word with Umlaut and capitalization', 'de-DE'),

        # --- Abkürzungen ---
        ('zum beispiel', 'Zum Beispiel', 'Common abbreviation', 'de-DE'),
        # Oder 'zum Beispiel' je nach gewünschtem Output
        ('unter anderem', 'Unter anderem', 'Common abbreviation', 'de-DE'),  # Oder 'unter anderem'
        ('respektive', 'respektive', 'Common abbreviation', 'de-DE'),  # Oder 'beziehungsweise'
        ('circa', 'circa', 'Common abbreviation', 'de-DE'),
        ('doktor', 'Doktor', 'Common title abbreviation', 'de-DE'),
        ('professor', 'Professor', 'Common title abbreviation', 'de-DE'),
        # ('und so weiter', 'usw.', 'Common abbreviation', 'de-DE'),
        ('zum schluss', 'Zum Schluss', 'Custom abbreviation example', 'de-DE'),  # Falls du eigene Abkürzungen hast

        # --- Fragen und Ausrufe ---
        ('wie spät ist es', 'Wie spät ist es', 'Direct question', 'de-DE'),
        ('wo finde ich toilette', 'Wo finde ich Toilette', 'Direct question', 'de-DE'),
        ('das ist unglaublich', 'Das ist unglaublich', 'Exclamatory sentence', 'de-DE'),
        ('hilfe', 'Hilfe', 'word', 'de-DE'),
        ('was für ein tag', 'Was für ein Tag', 'Exclamatory phrase', 'de-DE'),

        # --- Einfache Befehle/Anweisungen (falls relevant) ---
        ('gehe nach links', 'Gehe nach links', 'Simple command', 'de-DE'),
        ('schalte das licht ein', 'Schalte das Licht ein', 'Simple command', 'de-DE'),
        ('öffne die tür', 'Öffne die Tür', 'Simple command', 'de-DE'),
        ('stopp', 'stopp', 'Simple command/exclamation', 'de-DE'),
        ('wiederhole das bitte', 'Wiederhole das bitte', 'Request', 'de-DE'),

        # --- Komplexere Sätze ---
        # ('ich gehe heute abend ins kino mit freunden', 'Ich gehe heute Abend ins Kino mit Freunden',
        #  'Longer sentence with multiple nouns', 'de-DE'),
        ('die sonne scheint auf die blumen', 'Die Sonne scheint auf die Blumen',
         'Compound sentence', 'de-DE'),
        ('obwohl es regnet ist die stimmung gut', 'Obwohl es regnet, ist die Stimmung gut',
         'Sentence with subordinate clause and comma', 'de-DE'),
        ('der kleine hund spielt mit seinem neuen spielzeug',
         'Der kleine Hund spielt mit seinem neuen Spielzeug', 'Detailed sentence', 'de-DE'),
        # ('der kleine junge spielt mit seinem neuen spielzeug im park',
        #  'Der kleine Junge spielt mit seinem neuen Spielzeug im Park', 'Detailed sentence', 'de-DE'),
        ('das wetter wird morgen sonnig mit temperaturen um die zwanzig grad',
         'Das Wetter wird morgen sonnig mit Temperaturen um die 20 Grad', '"digits_to_numbers": True', 'de-DE'),
        # ('der chef hat gesagt wir sollen die präsentation bis freitag fertigstellen',
        #  'Der Chef hat gesagt, wir sollen die Präsentation bis Freitag fertigstellen.', 'Indirect speech with comma',
        #  'de-DE'),
    ]

    def run_single_thread_test(index, test_data):
        raw_text, expected, description = test_data

        # Isolation bleibt!
        worker_dir = test_output_dir / f"task_{index}"
        worker_dir.mkdir(parents=True, exist_ok=True)

        # Eindeutiger Zeitstempel für process_text_in_background
        unique_time = float(index)

        try:
            process_text_in_background(
                logger, lang_code, raw_text, worker_dir,
                unique_time, lt_url, output_dir_override=worker_dir
            )

            output_files = list(worker_dir.glob("tts_output_*.txt"))
            if not output_files:
                return False, raw_text, "[NO_FILE]", expected, description

            result_file = output_files[0]
            with open(result_file, 'r', encoding='utf-8-sig') as f:
                actual = f.read().strip()

            # Signatur-Bereinigung (settings sind hier verfügbar!)
            if hasattr(settings, 'signatur1'): actual = actual.replace(settings.signatur1, '')
            if hasattr(settings, 'signatur'): actual = actual.replace(settings.signatur, '')
            actual = actual.strip()

            # Cleanup
            os.remove(result_file)
            worker_dir.rmdir()

            pattern = r"(🗣|\-\-)"  # cut off signature . example: first sequence of digits
            m = re.search(pattern, actual)
            if m:
                actual2 = actual[:m.start()]
            else:
                actual2 = actual  # no match -> keep original

            return actual2 == expected, raw_text, actual2, expected, description
        except Exception as e:
            return False, raw_text, str(e), expected, description

    active_tests = []
    for test_case in test_cases:
        if len(test_case) == 4:
            raw_text, expected, description, check_lang = test_case
            if check_lang == lang_code:
                active_tests.append((raw_text, expected, description))
        elif len(test_case) == 3:
            raw_text, expected, description = test_case
            active_tests.append((raw_text, expected, description))

    passed_count = 0
    failed_count = 0

    # logger.info(f"Running {len(active_tests)} tests with 16 THREADS...")
    start_time = time.perf_counter()

    # os.cpu_count() will return 16 on your Ryzen 3700X
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = [executor.submit(run_single_thread_test, i, t) for i, t in enumerate(active_tests)]
        for future in concurrent.futures.as_completed(futures):
            success, raw, actual, expected, desc = future.result()
            if success:
                passed_count += 1
            else:
                failed_count += 1
                logger.error(f"❌ FAIL: {desc} | Input: '{raw}' | Expected: '{expected}' | Got: '{actual}'")
                logger.error(f"   Input:    '{raw}'")
                logger.error(f"   Expected: '{expected}'")
                logger.error(f"   Got:      '{actual}'")

    # 4. Summary
    duration = time.perf_counter() - start_time
    logger.info("-" * 40)
    # m1 =f"✅ Passed: {passed_count} | ❌ Failed: {failed_count}"
    logger.info(f"✅ Passed: {passed_count} | ❌ Failed: {failed_count}")
    m2=f"⌚ Total Duration: {duration:.2f} seconds"
    logger.info(f"⌚ Total Duration: {duration:.2f} seconds")
    speak_fallback(f"{m2}", 'de-DE') # 'en-US') # 'de-DE')
    logger.info("-" * 40)

    settings.PLUGIN_HELPER_TTS_ENABLED = backup_tts_enabled

    if failed_count > 0:
        sys.exit(1)


def _execute_self_test_core(logger, tmp_dir, lt_url, lang_code):
    """

    """
    settings = DynamicSettings()

    backup_tts_enabled = settings.PLUGIN_HELPER_TTS_ENABLED
    settings.PLUGIN_HELPER_TTS_ENABLED = False

    # Base directory for all tests
    test_base_dir = tmp_dir / "sl5_aura_self_test"
    test_base_dir.mkdir(parents=True, exist_ok=True)

    test_cases = [

        # case(input_text='->SPEECH_PAUSE_TIMEOUT<-', expected=f"{SPEECH_PAUSE_TIMEOUT_021}", context='proff if we can change settings 2026-0104-1435'),

        #     ('lehrwart', 'leerworttest1'),
        case(input_text='leerworttest', expected=f"leerworttest1", context='punctation map test', lang='de-DE'),

        case(input_text='->AUDIO_INPUT_DEVICE<-', expected=f"SYSTEM_DEFAULT",
             context='proff if we can change settings 2026-0104-1435'),
        # case(input_text='->SPEECH_PAUSE_TIMEOUT<-', expected='7890', context='proff if we can change settings 2026-0104-1435'),

        ('Sebastian mit nachnamen', 'Sebastian mit Nachnamen',
         'LT Uppercase. \n may check --> config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py',
         'de-DE'),

        case(input_text='null', expected='0', context='git'),
        case(input_text='über die konsole zu bedienen', expected='über die konsole zu bedienen', context='git'),
        case(input_text='geht cobit', expected='git commit', context='git'),
        ('geht staates', 'git status', '19.11.25 10:19 Wed', 'de-DE'),
        ('ausrufezeichen', '!', 'Exact MAP match for punctuation', 'de-DE'),

        # following differ when daytime chaning:
        # ('good Morning people', 'hey all out there people', 'use a postRule. Funny useless rule ;) just for testing','en-US'),
        ('colours', 'colors', 'fix by LT', 'en-US'),
        ('underilnes', 'underlines', 'fix by LT', 'en-US'),
        ('too have', 'to have', 'fix by LT', 'en-US'),
        ('colours', 'colors', 'fix by LT', 'en-US'),
        ('5 PM in the afternoon', '5 PM', 'fix by LT', 'en-US'),

        ('good nigt Mum', 'Good night Mum', 'Funny useless rule ;) just for testing',
         'en-US'),

        # good evening dead Good evening them Good evening ought to get

        ('thousand dollars.', '1000 dollars.', 'Number with unit',
         'en-US'),
        ('one and thousand dollars.', '1 and 1000 dollars.', 'Number with unit',
         'en-US'),

        ('tausend euro. Und euro großgeschrieben.', '1000 Euro. Und Euro großgeschrieben.', 'Number with unit',
         'de-DE'),

        ('was ist 5 plus 3', 'Das Ergebnis von 5 plus 3 ist 8.', 'calc in MAP Wannweil', 'de-DE'),

        ('bitte reservieren sie einen tisch für zwei personen um acht uhr',
         'Bitte reservieren Sie einen Tisch für 2 Personen um 8 Uhr', 'Polite request with time and number',
         'de-DE'),
        ('eins', '1', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),
        ('eins zwei', '1 2', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),

        ('Sekunde Lauffer', 'Sigune Lauffer', 'MAP Wannweil', 'de-DE'),
        ('mit nachnamen laufer', 'Mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('Sebastian mit nachnamen', 'Sebastian mit Nachnamen', 'Partial map + LT correction', 'de-DE'),
        ('von sebastian laufer', 'Von Sebastian Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('punkt', '.', 'Exact MAP match', 'de-DE'),
        ('komma', ',', 'Exact MAP match'),
        # ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        ('git at', 'git add .', 'Fuzzy map REGEX match', 'de-DE'),
        ('geht status', 'git status', 'Fuzzy map FUZZY string match', 'de-DE'),
        ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', 'de-DE'),
        ('Sekunde lauf war', 'Sigune Lauffer war', 'MAP Wannweil', 'de-DE'),

        # --- Grundlegende Satzzeichen ---
        ('punkt', '.', 'Exact MAP match for punctuation', 'de-DE'),
        ('komma', ',', 'Exact MAP match for punctuation', 'de-DE'),
        ('fragezeichen', '?', 'Exact MAP match for punctuation', 'de-DE'),
        ('ausrufezeichen', '!', 'Exact MAP match for punctuation', 'de-DE'),
        ('doppelpunkt', ':', 'Exact MAP match for punctuation', 'de-DE'),
        ('semikolon', ';', 'Exact MAP match for punctuation', 'de-DE'),
        ('bindestrich', '-', 'Exact MAP match for punctuation', 'de-DE'),
        ('gedankenstrich', '–', 'Exact MAP match for punctuation', 'de-DE'),  # Oder '-' je nach gewünschtem Output
        ('klammer auf', '(', 'Exact MAP match for punctuation', 'de-DE'),
        ('klammer zu', ')', 'Exact MAP match for punctuation', 'de-DE'),

        # --- Groß- und Kleinschreibung (Satzanfang, Nomen) ---
        # ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        # ('guten morgen', 'Guten Morgen', 'Capitalization of greeting and noun', 'de-DE'),
        ('ich heiße max', 'Ich heiße Max', 'Capitalization of pronoun and proper noun', 'de-DE'),
        ('der hund bellt', 'Der Hund bellt', 'Capitalization of article and noun', 'de-DE'),
        ('die katze schläft', 'Die Katze schläft', 'Capitalization of article and noun', 'de-DE'),
        ('ein haus und ein garten', 'Ein Haus und ein Garten', 'Capitalization of nouns', 'de-DE'),
        ('heute ist montag', 'Heute ist Montag', 'Capitalization of day of the week', 'de-DE'),
        ('im sommer ist es warm', 'Im Sommer ist es warm', 'Capitalization of season', 'de-DE'),

        # --- Zahlen und Ziffern ---
        ('sieben', '7', 'Numbers as digits', 'de-DE'),
        ('acht', '8', 'Numbers as digits', 'de-DE'),
        ('neun', '9', 'Numbers as digits', 'de-DE'),
        ('zehn', '10', 'Number as digit', 'de-DE'),
        # ('zweitausendunddreiundzwanzig', '2023', 'Year as digit', 'de-DE'),
        ('fünf komma', '5 ,', 'Decimal number', 'de-DE'),
        # ('minus drei', '- 3', 'Negative number', 'de-DE'),

        # --- Häufige Wörter und Phrasen ---
        # ('hallo wie geht es dir', 'Hallo, wie geht es dir', 'Common greeting and question', 'de-DE'),
        ('danke schön', 'Danke schön', 'Common thanks', 'de-DE'),
        ('bitte schön', 'Bitte schön', 'Common courtesy', 'de-DE'),
        ('entschuldigung', 'Entschuldigung', 'Common apology', 'de-DE'),
        ('ich verstehe', 'Ich verstehe', 'Common confirmation', 'de-DE'),
        ('ich weiß nicht', 'Ich weiß nicht', 'Common uncertainty', 'de-DE'),
        ('alles klar', 'Alles klar', 'Common affirmation', 'de-DE'),
        ('auf wiedersehen', 'Auf Wiedersehen', 'Common farewell', 'de-DE'),
        ('bis später', 'Bis später', 'Common farewell', 'de-DE'),
        # ('ja genau', 'Ja, genau', 'Affirmation with comma', 'de-DE'),
        # ('nein danke', 'Nein, danke', 'Refusal with thanks', 'de-DE'),
        ('es ist kalt draußen', 'Es ist kalt draußen', 'Simple descriptive sentence', 'de-DE'),
        ('was machst du heute', 'Was machst du heute', 'Common question', 'de-DE'),
        ('kein problem', 'Kein Problem', 'Common phrase', 'de-DE'),
        ('zum beispiel', 'Zum Beispiel', 'Common phrase', 'de-DE'),
        ('und so weiter', 'Und so weiter', 'Common phrase', 'de-DE'),
        ('einer nach dem anderen', 'Einer nach dem anderen', 'Idiomatic expression', 'de-DE'),

        # --- Wörter mit Umlauten und Sonderzeichen ---
        ('schön', 'schön', 'Word with Umlaut', 'de-DE'),
        ('überall', 'überall', 'Word with Umlaut', 'de-DE'),
        ('für', 'für', 'Word with Umlaut', 'de-DE'),
        ('größer', 'größer', 'Word with Umlaut and Eszett', 'de-DE'),
        ('straße', 'Straße', 'Word with Eszett and capitalization', 'de-DE'),
        ('weiß', 'weiß', 'Word with Eszett', 'de-DE'),
        ('füße', 'Füße', 'Word with Umlaut and capitalization', 'de-DE'),
        ('müde', 'müde', 'Word with Umlaut', 'de-DE'),
        ('hände', 'Hände', 'Word with Umlaut and capitalization', 'de-DE'),

        # --- Abkürzungen ---
        ('zum beispiel', 'Zum Beispiel', 'Common abbreviation', 'de-DE'),
        # Oder 'zum Beispiel' je nach gewünschtem Output
        ('unter anderem', 'Unter anderem', 'Common abbreviation', 'de-DE'),  # Oder 'unter anderem'
        ('respektive', 'respektive', 'Common abbreviation', 'de-DE'),  # Oder 'beziehungsweise'
        ('circa', 'circa', 'Common abbreviation', 'de-DE'),
        ('doktor', 'Doktor', 'Common title abbreviation', 'de-DE'),
        ('professor', 'Professor', 'Common title abbreviation', 'de-DE'),
        # ('und so weiter', 'usw.', 'Common abbreviation', 'de-DE'),
        ('zum schluss', 'Zum Schluss', 'Custom abbreviation example', 'de-DE'),  # Falls du eigene Abkürzungen hast

        # --- Fragen und Ausrufe ---
        ('wie spät ist es', 'Wie spät ist es', 'Direct question', 'de-DE'),
        ('wo finde ich toilette', 'Wo finde ich Toilette', 'Direct question', 'de-DE'),
        ('das ist unglaublich', 'Das ist unglaublich', 'Exclamatory sentence', 'de-DE'),
        ('hilfe', 'Hilfe', 'word', 'de-DE'),
        ('was für ein tag', 'Was für ein Tag', 'Exclamatory phrase', 'de-DE'),

        # --- Einfache Befehle/Anweisungen (falls relevant) ---
        ('gehe nach links', 'Gehe nach links', 'Simple command', 'de-DE'),
        ('schalte das licht ein', 'Schalte das Licht ein', 'Simple command', 'de-DE'),
        ('öffne die tür', 'Öffne die Tür', 'Simple command', 'de-DE'),
        ('stopp', 'stopp', 'Simple command/exclamation', 'de-DE'),
        ('wiederhole das bitte', 'Wiederhole das bitte', 'Request', 'de-DE'),

        # --- Komplexere Sätze ---
        # ('ich gehe heute abend ins kino mit freunden', 'Ich gehe heute Abend ins Kino mit Freunden',
        #  'Longer sentence with multiple nouns', 'de-DE'),
        ('die sonne scheint auf die blumen', 'Die Sonne scheint auf die Blumen',
         'Compound sentence', 'de-DE'),
        ('obwohl es regnet ist die stimmung gut', 'Obwohl es regnet, ist die Stimmung gut',
         'Sentence with subordinate clause and comma', 'de-DE'),
        ('der kleine hund spielt mit seinem neuen spielzeug',
         'Der kleine Hund spielt mit seinem neuen Spielzeug', 'Detailed sentence', 'de-DE'),
        # ('der kleine junge spielt mit seinem neuen spielzeug im park',
        #  'Der kleine Junge spielt mit seinem neuen Spielzeug im Park', 'Detailed sentence', 'de-DE'),
        ('das wetter wird morgen sonnig mit temperaturen um die zwanzig grad',
         'Das Wetter wird morgen sonnig mit Temperaturen um die 20 Grad', '"digits_to_numbers": True', 'de-DE'),
        # ('der chef hat gesagt wir sollen die präsentation bis freitag fertigstellen',
        #  'Der Chef hat gesagt, wir sollen die Präsentation bis Freitag fertigstellen.', 'Indirect speech with comma',
        #  'de-DE'),
    ]

    # 1. Filter test cases for the current language
    active_tests = []
    # Note: test_cases list remains as defined in your script
    for test_case in test_cases:
        if len(test_case) == 4:
            raw_text, expected, description, check_lang = test_case
            if check_lang == lang_code:
                active_tests.append((raw_text, expected, description))
        elif len(test_case) == 3:
            active_tests.append(test_case)
        # Add a default 'de-DE' for 2-tuple cases if they exist
        elif len(test_case) == 2 and lang_code == 'de-DE':
            active_tests.append((test_case[0], test_case[1], ''))


    logger.info(f"Running {len(active_tests)} tests in parallel using PROCESSES...")
    # logger.info(f"Running {len(active_tests)} tests in parallel (ThreadPool)...")
    start_time = time.perf_counter()

    # 2. Worker function with isolated sub-directory

    # 3. Parallel Execution
    passed_count = 0
    failed_count = 0

    # Use 20 workers to fully saturate the 16-core Ryzen CPU

    logger.info(f"Running {len(active_tests)} tests in parallel using PROCESSES...")

    # ProcessPoolExecutor nutzt echte CPU-Kerne parallel
    # Aber ACHTUNG: Das 'logger' Objekt kann oft nicht einfach in Prozesse kopiert werden.
    # Wir übergeben None als Logger oder nutzen ein einfaches Print-Logging innerhalb.

    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        # Wir reduzieren auf 8 Worker (echte physikalische Kerne),
        # das ist oft effizienter für CPU-lastige Aufgaben als 16 oder 20.
        futures = {executor.submit(run_single_test_process, i, t, lang_code, lt_url, str(test_base_dir)): t
                   for i, t in enumerate(active_tests)}

        for future in concurrent.futures.as_completed(futures):


            success, raw, actual, expected, desc = future.result()
            if success:
                passed_count += 1
            else:
                failed_count += 1
                logger.error(f"❌ FAIL: {desc}")
                logger.error(f"   Input:    '{raw}'")
                logger.error(f"   Expected: '{expected}'")
                logger.error(f"   Got:      '{actual}'")
                sys.exit(1)

    # 4. Summary
    duration = time.perf_counter() - start_time
    logger.info("=" * 40)
    # m1 =f"✅ Passed: {passed_count} | ❌ Failed: {failed_count}"
    logger.info(f"✅ Passed: {passed_count} | ❌ Failed: {failed_count}")
    m2=f"⌚ Total Duration: {duration:.2f} seconds"
    logger.info(f"⌚ Total Duration: {duration:.2f} seconds")
    speak_fallback(f"{m2}", 'de-DE')# 'en-US') # 'de-DE')

    logger.info("-" * 40)

    settings.PLUGIN_HELPER_TTS_ENABLED = backup_tts_enabled

    if failed_count > 0:
        sys.exit(1)


# futures = {executor.submit(run_single_test, i, t, lang_code, lt_url, str(test_base_dir)): t
#            for i, t in enumerate(active_tests)}


import sys
import os
import time
# import traceback
from pathlib import Path


# Dummy-Logger for Proses
class SimpleNullLogger:
    def info(self, msg):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def warning(self, msg):
        pass

    def debug(self, msg):
        pass

    def exception(self, msg, *args, **kwargs):
        pass

# if somebody is confused send him:
# find . -name "*settings.py"                                                                                                                                     ✔

def run_single_test_process(index, test_data, lang_code, lt_url, test_base_dir_str):
    try:
        import importlib.util
        import sys
        import os

        from pathlib import Path

        current_file = Path(__file__).resolve()

        # 1. Manueller Import
        ds_path = current_file.parents[1] / "config" / "dynamic_settings.py"
        spec = importlib.util.spec_from_file_location("dynamic_settings", str(ds_path))
        ds_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ds_mod)
        DynamicSettings = ds_mod.DynamicSettings

        # 2. Root setzen
        project_root = str(current_file.parents[4])
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        from scripts.py.func.process_text_in_background import process_text_in_background

        raw_text, expected, description = test_data

        # 3. Absolut isoliertes Verzeichnis (Task-Index im Namen)
        worker_dir = Path(test_base_dir_str) / f"task_{index}"
        worker_dir.mkdir(parents=True, exist_ok=True)

        settings = DynamicSettings()
        null_logger = SimpleNullLogger()

        # 4. NANOSEKUNDEN + INDEX für absolute Eindeutigkeit
        # time.time_ns() liefert z.B. 1705678901234567890
        # unique_id_ns = time.time_ns() + index

        # Wir konvertieren es in einen Float-Sekunden-Wert für die Funktion,
        # aber mit extrem hoher Präzision.
        # unique_time_float = unique_id_ns / 1_000_000_000.0
        unique_time_float = float(index)  # Absolut eindeutig: 0.0, 1.0, 2.0 ...

        process_text_in_background(
            null_logger, lang_code, raw_text, worker_dir,
            unique_time_float, lt_url, output_dir_override=worker_dir
        )

        # 5. Datei finden (nur in diesem privaten Task-Ordner!)
        output_files = list(worker_dir.glob("tts_output_*.txt"))
        if not output_files:
            return False, raw_text, "[NO_FILE]", expected, description

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
            print(f'717: {e}')
            pass



        pattern = r"(🗣|\-\-)"  # cut off signature . example: first sequence of digits
        m = re.search(pattern, actual)
        if m:
            actual2 = actual[:m.start()]
        else:
            actual2 = actual  # no match -> keep original



        return actual2 == expected, raw_text, actual2, expected, description

    except Exception as e:
        import traceback
        return False, "ERROR", f"{str(e)}\n{traceback.format_exc()}", "ERROR", "Process execution failed"
# def run_single_test_process(index, test_data, lang_code, lt_url, test_base_dir_str):
#     try:
#         import importlib.util
#         from pathlib import Path
#
#         current_file = Path(__file__).resolve()
#         # Pfad direkt zur Datei
#         ds_path = current_file.parents[1] / "config" / "dynamic_settings.py"
#
#         # 1. DynamicSettings manuell laden (ohne sys.path)
#         spec = importlib.util.spec_from_file_location("dynamic_settings", str(ds_path))
#         ds_mod = importlib.util.module_from_spec(spec)
#         spec.loader.exec_module(ds_mod)
#         DynamicSettings = ds_mod.DynamicSettings
#
#         # 2. Den Root zum Pfad hinzufügen für den Rest
#         project_root = str(current_file.parents[4])
#         if project_root not in sys.path:
#             sys.path.insert(0, project_root)
#
#         from scripts.py.func.process_text_in_background import process_text_in_background
#
#         # --- Rest des Ablaufs bleibt gleich ---
#         raw_text, expected, description = test_data
#         worker_dir = Path(test_base_dir_str) / f"task_{index}"
#         worker_dir.mkdir(parents=True, exist_ok=True)
#
#         settings = DynamicSettings()
#         null_logger = SimpleNullLogger()
#
#         process_text_in_background(
#             null_logger, lang_code, raw_text, worker_dir,
#             time.time(), lt_url, output_dir_override=worker_dir
#         )
#
#         output_files = list(worker_dir.glob("tts_output_*.txt"))
#         if not output_files:
#             return False, raw_text, "[NO_FILE]", expected, description
#
#         result_file = output_files[0]
#         with open(result_file, 'r', encoding='utf-8-sig') as f:
#             actual = f.read().strip()
#
#         if hasattr(settings, 'signatur1'): actual = actual.replace(settings.signatur1, '')
#         if hasattr(settings, 'signatur'): actual = actual.replace(settings.signatur, '')
#         actual = actual.strip()
#
#         os.remove(result_file)
#         try: worker_dir.rmdir()
#         except: pass
#
#         return actual == expected, raw_text, actual, expected, description
#
#     except Exception as e:
#         import traceback
#         return False, "ERROR", f"{str(e)}\n{traceback.format_exc()}", "ERROR", "Process execution failed"

def run_single_test_202501311853(logger, index, test_data, lang_code, lt_url, test_base_dir):
    raw_text, expected, description = test_data

    # Create a UNIQUE folder for this specific test case
    # This is the ONLY way to prevent threads from stealing each other's files
    worker_dir = test_base_dir / f"task_{index}"
    worker_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Execute processing in the isolated folder
        process_text_in_background(
            logger, lang_code, raw_text, worker_dir,
            time.time(), lt_url, output_dir_override=worker_dir
        )

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
            print(f'812: {e}')
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

