# file: scripts/py/func/checks/self_tester.py

import os
import time
import glob
# from pathlib import Path

# Important: Add project root to sys.path to allow imports from other directories
# This assumes self_tester.py is in the project's root or a subdirectory.
# Adjust if necessary.
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# Note: In dictation_service.py this might be SCRIPT_DIR instead of project_root

from scripts.py.func.process_text_in_background import process_text_in_background
# from config.dynamic_settings import settings

def run_core_logic_self_test(logger, tmp_dir, lt_url, lang_code):
    """
    Runs a series of predefined tests against the core text processing logic.
    This function simulates inputs and checks the output files.
    """
    logger.info(f"DEV_MODE: Running core logic self-test... lang is: {lang_code} e.g. maybe de-DE")
    test_output_dir = tmp_dir / "sl5_aura_self_test"
    test_output_dir.mkdir(parents=True, exist_ok=True)

    # --- Test Cases ---
    # Format: (input_text, expected_output, description)
    logger.info('test_cases = ...')
    test_cases = [
        ('punkt', '.', 'Exact MAP match', 'de-DE'),
        ('komma', ',', 'Exact MAP match'),
        ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        ('git at', 'git add .', 'Fuzzy map REGEX match', 'de-DE'),
        ('geht status', 'git status', 'Fuzzy map FUZZY string match', 'de-DE'),
        ('ein test von sebastian laufer', 'Ein Test von Sebastian Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', 'de-DE'),
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
        ('eins zwei drei', '1 2 3', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),
        ('vier fünf sechs', '4 5 6', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),
        ('sieben acht neun', '7 8 9', 'maps/plugins/numbers_to_digits/de-DE/', 'de-DE'),
        ('sieben', '7', 'Numbers as digits', 'de-DE'),
        ('acht', '8', 'Numbers as digits', 'de-DE'),
        ('neun', '9', 'Numbers as digits', 'de-DE'),
        ('zehn', '10', 'Number as digit', 'de-DE'),
        ('hundert euro', '100 Euro', 'Number with unit', 'de-DE'),
        # ('zweitausendunddreiundzwanzig', '2023', 'Year as digit', 'de-DE'),
        ('fünf komma zwei', '5, 2', 'Decimal number', 'de-DE'),
        ('minus drei', '- 3', 'Negative number', 'de-DE'),

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
        ('wo ist die toilette', 'Wo ist die Toilette', 'Direct question', 'de-DE'),
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
        ('bitte reservieren sie einen tisch für zwei personen um acht uhr',
         'Bitte reservieren Sie einen Tisch für 2 Personen um 8 Uhr', 'Polite request with time and number',
         'de-DE'),
        ('das wetter wird morgen sonnig mit temperaturen um die zwanzig grad',
         'Das Wetter wird morgen sonnig mit Temperaturen um die 20 Grad', '"digits_to_numbers": True', 'de-DE'),
        # ('der chef hat gesagt wir sollen die präsentation bis freitag fertigstellen',
        #  'Der Chef hat gesagt, wir sollen die Präsentation bis Freitag fertigstellen.', 'Indirect speech with comma',
        #  'de-DE'),
    ]


    passed_count = 0
    failed_count = 0

    logger.info('45: for test_case in test_cases ...')
    for test_case in test_cases:
        expected = None
        if len(test_case) == 4:
            raw_text, expected, description, check_only_this_lang_code = test_case
            if check_only_this_lang_code != lang_code:
                continue
        elif len(test_case) == 3:
            raw_text, expected, description = test_case

        # Clean up old output files to ensure we read the new one
        for f in glob.glob(str(tmp_dir / "sl5_aura" / "tts_output_*.txt")):
            os.remove(f)

        # Run the actual processing function
        # process_text_in_background(logger, lang_code, raw_text, tmp_dir, time.time(), lt_url)
        logger.info('59: process_text_in_background ...')
        process_text_in_background(logger, lang_code, raw_text, test_output_dir, time.time(), lt_url, output_dir_override=test_output_dir)

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
            actual = "[NO OUTPUT FILE CREATED]"

        # Check result, ignoring any leading whitespace in the actual output
        if actual.lstrip() == expected:
            logger.info(f"  ✅ PASS: {description}")
            passed_count += 1
        else:
            logger.error(f"  ❌ FAIL: {description}")
            logger.error(f"     - Input:    '{raw_text}'")
            logger.error(f"     - Expected: '{expected}'")
            logger.error(f"     - Got:      '{actual}'")
            failed_count += 1

    # --- Summary ---
    logger.info("-" * 40)
    if failed_count == 0:
        logger.info(f"✅ Core Logic Self-Test: All {passed_count} tests passed!")
        if passed_count == 0:
            logger.error(f"❌ FAIL: Self-Test was tested: 0 of 0 ! Probably wrong. Makes no sense")
            exit(1)
    else:
        logger.error(f"❌ Core Logic Self-Test: {failed_count} of {passed_count + failed_count} tests ❌ FAILed.")
    logger.info("-" * 40)

