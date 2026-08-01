# scripts/py/func/checks/catch_all_training_e2e_test.py
"""
E2E check for the catch-all "unmatched word training" feature.

Verifies that when an unrecognized word (e.g. "Sandbank") hits a
catch-all FUZZY_MAP_pre rule wired to
config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py,
the word is written into the preceding rule's regex group as a new
alternative -- instead of being typed out into the active window.

Runs in-process (no HTTP call to the service), following the same
pattern as live_reload_e2e_func_test.py: backup the target map file,
mutate it, run process_text_in_background() directly, assert on the
resulting file content, then restore from backup in a finally block.

Note: unlike live_reload_e2e_func_test.py, this test does NOT check
tts_output_*.txt files. The collect_unmatched plugin intentionally
raises Exception('no text after replacement') on success, so no
output file is ever created for the catch-all path. Success is
verified by re-reading the map file and checking that the test word
was added to the preceding rule.
"""
import os
import platform
import shutil
import time
from pathlib import Path

from ..process_text_in_background import process_text_in_background

TEST_UNMATCHED_WORD = "Sandbank"
LANG_CODE = "de-DE"

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
PROJECT_ROOT = Path((TMP_DIR / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

PLUGIN_PARENT_DIR = PROJECT_ROOT / "config" / "maps" / "plugins" / "TEST"
ACTIVE_DIR_NAME = "catch_all_training_e2e_test"
DISABLED_DIR_NAME = ". catch_all_training_e2e_test"  # leading ". " keeps this out of
                                                        # normal map loading between test
                                                        # runs; see verification note in
                                                        # module docstring.
ACTIVE_DIR = PLUGIN_PARENT_DIR / ACTIVE_DIR_NAME
DISABLED_DIR = PLUGIN_PARENT_DIR / DISABLED_DIR_NAME

MAP_TARGET_FILE = ACTIVE_DIR / "de-DE" / "FUZZY_MAP_pre.py"
MAP_BACKUP_FILE = TMP_DIR / "sl5_aura" / "catch_all_training_e2e_test_FUZZY_MAP_pre_backup.py"

CATCH_ALL_ON_MATCH_EXEC_PATH = (
    PROJECT_ROOT / "config" / "maps" / "plugins" / "1_collect_unmatched_training" / "collect_unmatched.py"
)


def _activate_plugin_dir(logger) -> None:
    """Rename the disabled (space-prefixed) plugin dir to its active name, if present."""
    if ACTIVE_DIR.exists():
        logger.warning(
            f"catchAllTest: {ACTIVE_DIR} already exists (stale from a previous crashed run?). "
            "Proceeding without renaming."
        )
        return
    if DISABLED_DIR.exists():
        logger.info(f"catchAllTest: Activating plugin dir: {DISABLED_DIR} -> {ACTIVE_DIR}")
        DISABLED_DIR.rename(ACTIVE_DIR)


def _deactivate_plugin_dir(logger) -> None:
    """Rename the active plugin dir back to its disabled (space-prefixed) name."""
    if not ACTIVE_DIR.exists():
        return
    if DISABLED_DIR.exists():
        logger.error(
            f"catchAllTest: Cannot deactivate: both {ACTIVE_DIR} and {DISABLED_DIR} exist. "
            "Leaving as-is for manual inspection."
        )
        return
    logger.info(f"catchAllTest: Deactivating plugin dir: {ACTIVE_DIR} -> {DISABLED_DIR}")
    ACTIVE_DIR.rename(DISABLED_DIR)


def _insert_catch_all_rule(map_file: Path) -> None:
    """
    Insert the catch-all rule as the last element INSIDE the
    FUZZY_MAP_pre = [...] list literal.

    Must be inside the literal, not appended via FUZZY_MAP_pre.append(),
    since get_fuzzy_map_entries.py (AST-based) only parses entries that
    are part of the list literal itself.
    """
    content = map_file.read_text(encoding="utf-8")

    catch_all_entry = (
        "    (f'{str(__file__)}', r'^(.*)$', 10, {\n"
        f"        'on_match_exec': [Path(r'{CATCH_ALL_ON_MATCH_EXEC_PATH}')]\n"
        "    })\n"
    )

    idx = content.rfind("]")
    if idx == -1:
        raise RuntimeError(f"No closing ']' found for FUZZY_MAP_pre list in {map_file}")

    new_content = (
        content[:idx].rstrip().rstrip(",") + ",\n"
        "    # Catch-All rule inserted for catch_all_training_e2e_test\n"
        + catch_all_entry
        + content[idx:]
    )
    map_file.write_text(new_content, encoding="utf-8")

DEFAULT_MAP_CONTENT = '''# config/maps/plugins/TEST/catch_all_training_e2e_test/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
import os
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

TEST_FILE4_path = PROJECT_ROOT / "tools" / "tests" / "TEST_FILE4REPLACEMENT.txt"

FUZZY_MAP_pre = [
    (f'{TEST_FILE4_path}', r'^(Blumenkohl|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]
'''

def _ensure_map_file_exists(map_file: Path, logger) -> None:
    """Create the test map file with default content if it doesn't exist yet."""
    if map_file.exists():
        return
    logger.info(f"catchAllTest: Map file does not exist yet, creating it: {map_file}")
    map_file.parent.mkdir(parents=True, exist_ok=True)
    map_file.write_text(DEFAULT_MAP_CONTENT, encoding="utf-8")

def run_catch_all_training_e2e_test(logger, lt_url):
    """
    Returns 0 on success, 1 on failure. Mirrors the return-code
    convention of run_e2e_live_reload_func_test_v2().
    """
    logger.info("-" * 50)
    logger.info(f"catchAllTest [PID {os.getpid()}] Starting catch-all training e2e test...")

    _activate_plugin_dir(logger)
    _ensure_map_file_exists(MAP_TARGET_FILE, logger)


    try:

        # --- PHASE 0: BACKUP ---
        logger.info("catchAllTest: Phase 0: Backing up map file.")
        shutil.copy2(MAP_TARGET_FILE, MAP_BACKUP_FILE)
        
        # --- PHASE 1: INSERT CATCH-ALL RULE ---
        logger.info("catchAllTest: Phase 1: Inserting catch-all rule into map file.")
        _insert_catch_all_rule(MAP_TARGET_FILE)

        # --- PHASE 2: TRIGGER UNMATCHED WORD PROCESSING ---
        # logger.info(f"catchAllTest: Phase 2: Processing unmatched word '{TEST_UNMATCHED_WORD}'.")
        test_base_dir = TMP_DIR / "sl5_aura" / "sl5_aura_catch_all_test"
        test_base_dir.mkdir(parents=True, exist_ok=True)

        # The catch-all plugin raises Exception('no text after replacement')
        # by design once it has registered the word. That exception is
        # expected here and must not be treated as a test failure.
        try:
            process_text_in_background(
                logger, LANG_CODE, TEST_UNMATCHED_WORD,
                None, time.time(), lt_url,
                output_dir_override=test_base_dir,
            )
        except Exception as e:
            logger.info(f"catchAllTest: Phase 2: Expected control-flow exception caught: {e}")

        # --- PHASE 3: VERIFY WORD WAS REGISTERED IN MAP FILE ---
        logger.info("catchAllTest: Phase 3: Verifying word was added to map file.")
        updated_content = MAP_TARGET_FILE.read_text(encoding="utf-8")

        if TEST_UNMATCHED_WORD not in updated_content:
            logger.error(
                f"catchAllTest: Phase 3 FAILED: '{TEST_UNMATCHED_WORD}' was not found in "
                f"{MAP_TARGET_FILE} after processing."
            )
            return 1

        print(':catchAllTest:🌞🌞🌞🌞🌞 ')
        logger.info("############################################")
        logger.info(f"👍 catchAllTest: Phase 3 PASSED: '{TEST_UNMATCHED_WORD}' was registered in the map file.")
        logger.info("############################################")
        return 0

    finally:
        # --- PHASE 4: RESTORE ---
        logger.info("catchAllTest: Phase 4: Restoring original map file from backup.")
        try:
            shutil.copy2(MAP_BACKUP_FILE, MAP_TARGET_FILE)
            MAP_BACKUP_FILE.unlink(missing_ok=True)
        except Exception as e:
            logger.error(f"catchAllTest: Phase 4: Restore FAILED: {e}")

        # --- PHASE 5: DEACTIVATE ---
        _deactivate_plugin_dir(logger)

if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    test_logger = logging.getLogger("catch_all_training_e2e_test")
    test_logger.propagate = False

    lt_url_cli = "http://localhost:8082"
    status = run_catch_all_training_e2e_test(test_logger, lt_url_cli)
    if status == 0:
        print(f':catchAllTest: status="{status}" 🌞🌞🌞🌞 ')
    else:
        print(f':catchAllTest: status="{status}" 💥🚨💥🚨 ')

    raise SystemExit(status)
