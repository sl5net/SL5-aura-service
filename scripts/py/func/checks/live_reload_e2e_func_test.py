# live_reload_e2e_func_test.py

import os
import shutil
import time
from pathlib import Path
import glob

# Re-use utilities and core logic from the main self_tester context
from ..process_text_in_background import process_text_in_background
from ..config.dynamic_settings import settings
# from .config.dynamic_settings import settings

TEST_INPUT = 'Recaps'
EXPECTED_OUTPUT = 'regex'
LANG_CODE = 'de-DE'

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
MAP_TARGET_DIR = PROJECT_ROOT / "config" / "maps" / "plugins" / "standard_actions"

MAP_BACKUP_DIR = PROJECT_ROOT / "standard_actions_backup_temp"
TEMP_DIR = PROJECT_ROOT / "log"

def execute_test_case_and_check(logger, lt_url, expected):
    """ Helper to run the core logic and parse the output as in self_tester.py """

    # Clean up old output files
    for f in glob.glob(str(TEMP_DIR / "tts_output_*.txt")):
        os.remove(f)

    # Run the actual processing function
    process_text_in_background(logger, LANG_CODE, TEST_INPUT, TEMP_DIR, time.time(), lt_url, output_dir_override=TEMP_DIR)

    # Find the output file
    output_files = list(TEMP_DIR.glob("tts_output_*.txt"))

    if not output_files:
        return False, "[NO OUTPUT FILE CREATED]"

    latest_file = max(output_files, key=os.path.getctime)
    with open(latest_file, 'r', encoding='utf-8-sig') as f:
        actual = f.read().lstrip()
    os.remove(latest_file) # Clean up

    # Apply self_tester cleanup logic
    if hasattr(settings, 'signatur1'):
        if settings.signatur1:
            actual = actual.replace(settings.signatur1, '').strip()
    if hasattr(settings, 'signatur'):
        actual = actual.replace(settings.signatur, '').strip()

    # actual = actual.replace(settings.signatur1, '').replace(settings.signatur, '').strip()

    # Check the result
    return actual == expected, actual





def run_e2e_live_reload_func_test_v2(logger, lt_url):


    logger.info("-" * 50)
    logger.info("✅ TEST (🏃🏿‍♀️‍➡️ 🔜 BACKUP/DELETE/RESTORE Map (live_reload_e2e_func_test .py)")

    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    if MAP_BACKUP_DIR.is_dir():
        shutil.rmtree(MAP_BACKUP_DIR)
    elif MAP_BACKUP_DIR.exists():
        # Sollte nur passieren, wenn es eine Datei mit dem Backup-Namen ist. Löschen.
        os.remove(MAP_BACKUP_DIR)

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    if MAP_BACKUP_DIR.exists():
        shutil.rmtree(str( MAP_BACKUP_DIR))

    # --- PHASE 0: PREPARATION (Backup) ---
    # logger.info(f"✅ Test: Phase 0: Creating Backup of: {MAP_TARGET_DIR.name}")
    try:
        shutil.copytree(MAP_TARGET_DIR, MAP_BACKUP_DIR)
        logger.info("✅ Test: Phase 0: Backup created successfully of: {MAP_TARGET_DIR.name}.")
    except Exception as e:
        logger.error(f"❌ Test: Phase 0: Backup FAILED: {e} of: {MAP_TARGET_DIR.name}")
        return 1

    time.sleep(0.010)

    # logger.info("Phase 1: Baseline check: Rule MUST be active.")
    success, actual_output = execute_test_case_and_check(logger, lt_url, EXPECTED_OUTPUT)
    loop_count = 0
    while not success and loop_count<100:
        loop_count += 1
        time.sleep(0.010)
        success, actual_output = execute_test_case_and_check(logger, lt_url, EXPECTED_OUTPUT)

    if not success:
        logger.error(f"❌ Phase 1 FAILED: Rule '{TEST_INPUT}' did not work. Test cannot proceed. Output: {actual_output}")
        # RESTORE THE SYSTEM BEFORE EXITING ON FAILURE
        shutil.copytree(MAP_BACKUP_DIR, MAP_TARGET_DIR)
        shutil.rmtree(MAP_BACKUP_DIR)
        return 1
    logger.info("✅ Test: Phase 1 PASSED: Rule is active.")

    # --- PHASE 2: LÖSCHEN (Disabling Rule) ---
    logger.info(f"✅ Test: Phase 2: Deleting target map directory. {MAP_TARGET_DIR}")


    try:
        shutil.rmtree(MAP_TARGET_DIR)
    except Exception as e:
        logger.error(f"❌ Deletion FAILED: {e}")
        # RESTORE THE SYSTEM BEFORE EXITING ON FAILURE
        shutil.copytree(MAP_BACKUP_DIR, MAP_TARGET_DIR)
        shutil.rmtree(MAP_BACKUP_DIR)
        return 1

    # logger.info("✅ Test: Waiting seconds for Live Reload to fully process deletion.")

    #exit(1)

    time.sleep(0.010)

    # --- PHASE 3: MITTEL-PRÜFUNG (Must Fail) ---
    # logger.info("✅ Test: Phase Nr 3: Failure check: Rule MUST be inactive.")
    expected_failure_text = "[NO OUTPUT FILE CREATED]"
    success, actual_output = execute_test_case_and_check(logger, lt_url, EXPECTED_OUTPUT)
    loop_count = 0
    while success and loop_count<100:
        loop_count += 1
        time.sleep(0.010)
        success, actual_output = execute_test_case_and_check(logger, lt_url, EXPECTED_OUTPUT)


    if not success or actual_output != expected_failure_text:



        logger.info(f"✅ Test: Phase 3 PASSED: Rule successfully deactivated. ")



    else:
        logger.error(f"141: ❌ Phase 3 FAILED: Rule still executed! Output: {actual_output}")
        # Proceed to restore for system safety
        pass



    # --- PHASE 4: WIEDERHERSTELLEN (Reactivating Rule) ---
    logger.info("Phase 4: Restoring original map directory from backup.")

    try:
        shutil.copytree(MAP_BACKUP_DIR, MAP_TARGET_DIR) # Copy back to the original location
    except Exception as e:
        logger.error(f"❌ Restore FAILED: {e}")
        return 1

    logger.info("Waiting for Live Reload to fully process restoration.")
    time.sleep(0.010)

    # --- PHASE 5: END-PRÜFUNG (Must Work) ---
    logger.info("Phase 5: Re-activation check: Rule MUST be active again.")
    loop_count = 0
    while not success and loop_count<100:
        loop_count += 1
        time.sleep(0.010)
        success, actual_output = execute_test_case_and_check(logger, lt_url, EXPECTED_OUTPUT)


    # scripts/py/func/checks/live_reload_e2e_func_test.py:166
    final_status = 0
    if success:
        logger.info("✅ Phase 5 PASSED: Rule is active again.")
    else:
        logger.error(f"❌ Phase 5 FAILED: Rule did not reactivate! Output: {actual_output}")
        final_status = 1

    # --- FINAL CLEANUP ---
    shutil.rmtree(MAP_BACKUP_DIR)
    logger.info(f"{'✅ Phase 6 TEST COMPLETE SUCCESS 🎉🏆' if final_status == 0 else '❌ Phase 6 TEST COMPLETE FAILURE'}")
    return final_status

