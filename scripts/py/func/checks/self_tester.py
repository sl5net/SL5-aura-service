# file: scripts/py/func/checks/self_tester.py
import re
from pathlib import Path
from logging import FileHandler

import os
import time
import glob
# from pathlib import Path

# Important: Add project root to sys.path to allow imports from other directories
# This assumes self_tester.py is in the project's root or a subdirectory.
# Adjust if necessary.
import sys



def check_translator_hijack(logger):
    proj_dir = Path(__file__).parents[4]

    path = proj_dir / "config"  / "maps" / "plugins" / "standard_actions" / "language_translator" / "de-DE" / "FUZZY_MAP_pre.py"
    if path.exists():
        # [ \t]* matches only horizontal whitespace
        content = path.read_text()
        pattern = r"#[ ]*TRANSLATION_RULE[ ]*\n[^\n]*#"
        if re.search(pattern, content):
            logger.info(f"25:🚨 HIJACK: Rule in ..{str(path)[-30:]} is activ!")
            logger.info(content)
            return False
    else:
        logger.info(f"31:🚨 HIJACK: path {str(path)} not exists!")

    return True

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Note: In dictation_service.py this might be SCRIPT_DIR instead of project_root

from scripts.py.func.process_text_in_background import process_text_in_background
from scripts.py.func.checks.run_function_with_throttling import run_function_with_throttling
from config.dynamic_settings import settings
# from config.settings import signatur # ,signatur_ar,signatur_en,signatur_pt_br


def get_logger_file_path(logger_instance):
    """Retrieves the Path object for the first FileHandler."""
    for handler in logger_instance.handlers:
        if isinstance(handler, FileHandler):
            return Path(handler.baseFilename)
    return None

def simple_clear_log(log_path: Path):
    """
    Clears the log file using 'w' mode.
    NOTE: This does NOT close the logger handler, risking a race condition.
    """
    if log_path is None:
        print("Error: No log file path found.")
        return

    try:
        # Open in write mode ('w') to truncate the file
        with open(log_path, 'w', encoding='utf-8'):
            pass
        print(f"Log '{log_path}' cleared successfully.")
    except Exception as e:
        # This catch handles FileNotFoundError and PermissionError/Lock issues
        print(f"Warning: Could not clear log file {log_path}. Error: {e}", file=sys.stderr)


# file: scripts/py/func/checks/self_tester.py:50
def run_core_logic_self_test(logger, tmp_dir: Path, lt_url, lang_code):
    """
    Runs a series of predefined tests, guarded by a persistent throttle mechanism.
    """

    if check_translator_hijack(logger):
        logger.info(f"self_tester.py exit exit exit")
        logger.info(f"75:🚨 HIJACK: rule is activ!")
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
def _execute_self_test_core(logger, tmp_dir, lt_url, lang_code):
    """
    Runs a series of predefined tests against the core text processing logic.
    This function simulates inputs and checks the output files.
    """


    start_with_empty_logger = True
    # start_with_empty_logger = False

    if start_with_empty_logger:
        log_path = get_logger_file_path(logger)
        simple_clear_log(log_path)  # Call the simple function

    logger.info(f"______________________________________________________")
    logger.info(f"self_tester.py DEV_MODE: Running core logic self-test... lang is: {lang_code} e.g. maybe de-DE")
    logger.info(f"______________________________________________________")
    logger.info(f"___ best disable before run: match all to nothing. like: .+ -> or .* -> '' ___")
    logger.info(f"______________________________________________________")
    test_output_dir = tmp_dir / "sl5_aura_self_test"
    test_output_dir.mkdir(parents=True, exist_ok=True)


    # ('geht cobit', 'git commit', 'git', 'de-DE'),

    # --- Test Cases ---
    # Format: (input_text, expected_output, description)
    # logger.info('self_tester.py:31 test_cases = ...')

    """
    'konsole' based on pattern '\b(Konsole)\b'
    12:50:58,197 - INFO     - Line 223: regex_match_found: break
    12:50:58,197 - WARNING  - Nach der Plugin-Verarbeitung gab es keinen Text zum Ausgeben.
    """

    test_cases = [

        ('Sebastian mit nachnamen', 'Sebastian mit Nachnamen', 'LT correction Uppercase', 'de-DE'),

        case(input_text='null', expected='0', context='git'),
        case(input_text='über die konsole zu bedienen', expected='über die konsole zu bedienen', context='git'),
        case(input_text='geht cobit', expected='git commit', context='git'),
        ('geht staates', 'git status', '19.11.25 10:19 Wed', 'de-DE'),
        ('ausrufezeichen', '!', 'Exact MAP match for punctuation', 'de-DE'),
        ('good Morning people', 'hey all out there people', 'use a postRule. Funny useless rule ;) just for testing',
         'en-US'),
        ('colours', 'colors', 'fix by LT','en-US'),
        ('underilnes', 'underlines', 'fix by LT', 'en-US'),
        ('too have', 'to have', 'fix by LT', 'en-US'),
        ('colours', 'colors', 'fix by LT', 'en-US'),
        ('5 PM in the afternoon', '5 PM', 'fix by LT', 'en-US'),

        ('good nigt Mum', 'Good night Mum', 'Funny useless rule ;) just for testing',
         'en-US'),

        # ﻿good evening dead ﻿Good evening them ﻿Good evening ought to get

        ('thousand dollars.', '1000 dollars.', 'Number with unit',
         'en-US'),
        ('one and thousand dollars.', '1 and 1000 dollars.', 'Number with unit',
         'en-US'),


        ('tausend euro. Und euro großgeschrieben.', '1000 Euro. Und Euro großgeschrieben.', 'Number with unit', 'de-DE'),

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
        ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
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
        ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
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
        ('zum beispiel', 'Zum Beispiel', 'Common abbreviation', 'de-DE'),  # Oder 'zum Beispiel' je nach gewünschtem Output
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


    passed_count = 0
    failed_count = 0

    # logger.info(f'self_tester.py:161: for test_case in {len(test_cases)} test_cases ...')
    for test_case in test_cases:
        expected = ''
        if len(test_case) == 4:
            raw_text, expected, description, check_only_this_lang_code = test_case
            if check_only_this_lang_code != lang_code:
                # logger.info(f'self_tester.py:167 {check_only_this_lang_code} != {lang_code}')
                continue
        elif len(test_case) == 3:
            raw_text, expected, description = test_case

        # Clean up old output files to ensure we read the new one
        for f in glob.glob(str(tmp_dir / "sl5_aura" / "tts_output_*.txt")):
            os.remove(f)

        # Run the actual processing function
        # process_text_in_background(logger, lang_code, raw_text, tmp_dir, time.time(), lt_url)
        # logger.info(f"self_tester.py:59: test_case:{test_case}")
        """
        def process_text_in_background(logger,
                           LT_LANGUAGE,
                           raw_text,
                           TMP_DIR,
                           recording_time,
                           active_lt_url,
                          output_dir_override = None):
        """
        # from scripts.py.func.process_text_in_background import process_text_in_background
        # checks/self_tester.py:333
        process_text_in_background(logger,
                                   lang_code,
                                   raw_text,
                                   test_output_dir,
                                   time.time(),
                                   lt_url,
                                   output_dir_override=test_output_dir)

        # Find the output file - there should be only one
        try:
            # output_files = list(glob.glob(str(tmp_dir / "sl5_aura" / "tts_output_*.txt")))
            output_files = list(test_output_dir.glob("tts_output_*.txt"))

            if not output_files:
                raise FileNotFoundError
            latest_file = max(output_files, key=os.path.getctime)
            with open(latest_file, 'r', encoding='utf-8-sig') as f:
                actual = f.read().lstrip()
            os.remove(latest_file) # Clean up
        except (FileNotFoundError, IndexError):
            actual = "self_tester.py:208 [NO OUTPUT FILE CREATED]"

        # Check result, ignoring any leading whitespace in the actual output

        # logger.info(f"self_tester.py:211: test_case:{test_case} actual:{actual}")

        actual = actual.replace(settings.signatur1, '')
        actual = actual.replace(settings.signatur, '')
        actual = actual.strip()

        if actual.lstrip() == expected:
            passed_count += 1
            if failed_count > 0:
                logger.info(f"self_tester.py:216 ✅ "
                            f" {failed_count} ❌ FAILed of"
                            f" {passed_count + failed_count}tested of"
                            f" {len(test_cases)} tests (lang={lang_code})")
            else:
                logger.info(f"self_tester.py:216 ✅ "
                            f" {passed_count + failed_count}tested of"
                            f" {len(test_cases)} tests (lang={lang_code})")

        else:
            logger.error(f"     - Input:    '{raw_text}'")
            logger.error(f"     - Expected: '{expected}'")
            logger.error(f"     - Got:      '{actual}'")
            failed_count += 1
            logger.error(f"self_tester.py:222 ❌ FAIL: {failed_count} of {passed_count + failed_count}tested of {len(test_cases)} tests ❌ FAILed (lang={lang_code})")

            exit(1)


    # --- Summary ---
    logger.info("-" * 40)
    if failed_count == 0:
        logger.info(f"self_tester.py:229✅ Core Logic Self-Test: All {passed_count}tested of {len(test_cases)} tests(all lang) passed! 🏆🥇 🎊 🎉 Great no test failed")
        if passed_count == 0:
            logger.error(f"self_tester.py:232 ❌ FAIL was tested: 0 of 0 ! Probably wrong. Makes no sense")
            exit(1)
    else:
        logger.error(f"self_tester.py:235 ❌ Core Logic Self-Test: {failed_count} of {passed_count + failed_count}tested of {len(test_cases)} tests ❌ FAILed.")
    logger.info("-" * 40)

