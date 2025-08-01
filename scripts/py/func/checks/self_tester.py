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
# from config import settings

def run_core_logic_self_test(logger, tmp_dir, lt_url, lang_code):
    """
    Runs a series of predefined tests against the core text processing logic.
    This function simulates inputs and checks the output files.
    """
    logger.info(f"DEV_MODE: Running core logic self-test... lang is: {lang_code} e.g. maybe de-DE")
    test_output_dir = tmp_dir / "sl5_dictation_self_test"
    test_output_dir.mkdir(parents=True, exist_ok=True)

    # --- Test Cases ---
    # Format: (input_text, expected_output, description)
    test_cases = [
        ('punkt', '.', 'Exact MAP match', 'de-DE'),
        ('komma', ',', 'Exact MAP match'),
        ('das ist ein test', 'Das ist ein Test', 'LanguageTool grammar/capitalization', 'de-DE'),
        ('git at', 'git add .', 'Fuzzy map REGEX match', 'de-DE'),
        ('geht status', 'git status', 'Fuzzy map FUZZY string match', 'de-DE'),
        ('ein test von sebastian laufer', 'Ein Test von Sebastian Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian mit nachnamen laufer', 'Sebastian mit Nachnamen Lauffer', 'Partial map + LT correction', 'de-DE'),
        ('sebastian laufer', 'Sebastian Lauffer', 'Exact MAP match', 'de-DE')
    ]
    passed_count = 0
    failed_count = 0

    for test_case in test_cases:
        if len(test_case) == 4:
            raw_text, expected, description, check_only_this_lang_code = test_case
            if check_only_this_lang_code != lang_code:
                continue
        elif len(test_case) == 3:
            raw_text, expected, description = test_case

        # Clean up old output files to ensure we read the new one
        for f in glob.glob(str(tmp_dir / "sl5_dictation" / "tts_output_*.txt")):
            os.remove(f)

        # Run the actual processing function
        # process_text_in_background(logger, lang_code, raw_text, tmp_dir, time.time(), lt_url)
        process_text_in_background(logger, lang_code, raw_text, test_output_dir, time.time(), lt_url, output_dir_override=test_output_dir)

        # Find the output file - there should be only one
        try:
            # output_files = list(glob.glob(str(tmp_dir / "sl5_dictation" / "tts_output_*.txt")))
            output_files = list(test_output_dir.glob("tts_output_*.txt"))

            if not output_files:
                raise FileNotFoundError
            latest_file = max(output_files, key=os.path.getctime)
            with open(latest_file, 'r', encoding='utf-8-sig') as f:
                actual = f.read()
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
    else:
        logger.error(f"❌ Core Logic Self-Test: {failed_count} of {passed_count + failed_count} tests failed.")
    logger.info("-" * 40)
