# scripts/py/func/checks/file4replacement_e2e_test.py
"""
E2E check for file-based FUZZY_MAP_pre replacements (resolve_file_replacement).

Verifies two resolution paths:
  1. Relative path (leading '.'), file located inside the plugin's own
     de-DE directory.
  2. Absolute path, file located outside the plugin directory
     (tools/tests/TEST_FILE4REPLACEMENT.txt).

Runs in-process (no HTTP call to the service), following the same
pattern as catch_all_training_e2e_test.py: activate the disabled
(space-prefixed) plugin dir, ensure fixture files exist, run
process_text_in_background() directly, read the resulting
tts_output_*.txt, compare against the fixture file's own content,
then deactivate the plugin dir again in a finally block.

Unlike catch_all_training_e2e_test.py, this test does NOT mutate
FUZZY_MAP_pre.py at runtime, so no map backup/restore is needed --
the rules are static, only the resolved replacement text is checked.
"""
import os
import platform
import time
from pathlib import Path

from ..config.dynamic_settings import settings
from ..process_text_in_background import process_text_in_background

LANG_CODE = "de-DE"

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")

from scripts.py.func.get_project_root import get_aura_project_root

SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

PLUGIN_PARENT_DIR = SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "TEST"
ACTIVE_DIR_NAME = "file4replacement"
DISABLED_DIR_NAME = ". file4replacement"  # leading ". " keeps this out of
                                            # normal map loading between test
                                            # runs; see catch_all_training_e2e_test.py
ACTIVE_DIR = PLUGIN_PARENT_DIR / ACTIVE_DIR_NAME
DISABLED_DIR = PLUGIN_PARENT_DIR / DISABLED_DIR_NAME

MAP_TARGET_FILE = ACTIVE_DIR / "de-DE" / "FUZZY_MAP_pre.py"
ZEBRA_FIXTURE_FILE = ACTIVE_DIR / "de-DE" / ".Zebra.txt"
ZEBRA_FIXTURE_CONTENT = "Zebra file replacement content"

# Absolute-path fixture lives outside the plugin dir on purpose, reused
# as-is from the legacy tools/tests/TEST_FILE4REPLACEMENT.sh setup.
EXTERNAL_FIXTURE_FILE = SL5NET_AURA_PROJECT_ROOT / "tools" / "tests" / "TEST_FILE4REPLACEMENT.txt"

DEFAULT_MAP_CONTENT = '''# config/maps/plugins/TEST/file4replacement/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401
import os
from pathlib import Path

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = Path((tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

TEST_FILE4_path = SL5NET_AURA_PROJECT_ROOT / "tools" / "tests" / "TEST_FILE4REPLACEMENT.txt"

FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     ),
    (f'{TEST_FILE4_path}', r'^(Blumenkohl|7)$', 85,
     {'command_flags': re.IGNORECASE,
      'cache': False,
      }
     )
]
'''


def _activate_plugin_dir(logger) -> None:
    """Rename the disabled (space-prefixed) plugin dir to its active name, if present."""
    if ACTIVE_DIR.exists():
        logger.warning(
            f"file4replacementTest: {ACTIVE_DIR} already exists (stale from a previous "
            "crashed run?). Proceeding without renaming."
        )
        return
    if DISABLED_DIR.exists():
        logger.info(f"file4replacementTest: Activating plugin dir: {DISABLED_DIR} -> {ACTIVE_DIR}")
        DISABLED_DIR.rename(ACTIVE_DIR)


def _deactivate_plugin_dir(logger) -> None:
    """Rename the active plugin dir back to its disabled (space-prefixed) name."""
    if not ACTIVE_DIR.exists():
        return
    if DISABLED_DIR.exists():
        logger.error(
            f"file4replacementTest: Cannot deactivate: both {ACTIVE_DIR} and {DISABLED_DIR} "
            "exist. Leaving as-is for manual inspection."
        )
        return
    logger.info(f"file4replacementTest: Deactivating plugin dir: {ACTIVE_DIR} -> {DISABLED_DIR}")
    ACTIVE_DIR.rename(DISABLED_DIR)


def _ensure_fixtures_exist(logger) -> None:
    """Create the test map file and the relative-path Zebra fixture if they don't exist yet."""
    if not MAP_TARGET_FILE.exists():
        logger.info(f"file4replacementTest: Map file does not exist yet, creating it: {MAP_TARGET_FILE}")
        MAP_TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
        MAP_TARGET_FILE.write_text(DEFAULT_MAP_CONTENT, encoding="utf-8")

    if not ZEBRA_FIXTURE_FILE.exists():
        logger.info(f"file4replacementTest: Zebra fixture does not exist yet, creating it: {ZEBRA_FIXTURE_FILE}")
        ZEBRA_FIXTURE_FILE.write_text(ZEBRA_FIXTURE_CONTENT, encoding="utf-8")


def _clean_signature(actual: str) -> str:
    if hasattr(settings, 'signatur1'):
        actual = actual.replace(settings.signatur1, '')
    if hasattr(settings, 'signatur'):
        actual = actual.replace(settings.signatur, '')
    return actual.strip()


def _run_case(logger, lt_url, input_text: str, expected_text: str, description: str):
    """Run one input through process_text_in_background and compare against expected_text."""
    test_base_dir = TMP_DIR / "sl5_aura" / "sl5_aura_file4replacement_test"
    test_base_dir.mkdir(parents=True, exist_ok=True)
    for f in test_base_dir.glob("tts_output_*.txt"):
        f.unlink()

    process_text_in_background(
        logger, LANG_CODE, input_text,
        None, time.time(), lt_url,
        output_dir_override=test_base_dir,
    )

    output_files = list(test_base_dir.glob("tts_output_*.txt"))
    if not output_files:
        return False, "[NO OUTPUT FILE CREATED]", expected_text, description

    latest_file = max(output_files, key=lambda p: p.stat().st_ctime)
    with open(latest_file, 'r', encoding='utf-8-sig') as f:
        actual = f.read().strip()
    latest_file.unlink()

    actual = _clean_signature(actual)
    return actual == expected_text, actual, expected_text, description


def run_file4replacement_e2e_test(logger, lt_url):
    """
    Returns 0 on success, 1 on failure. Mirrors the return-code
    convention of run_e2e_live_reload_func_test_v2() /
    run_catch_all_training_e2e_test().
    """
    logger.info("-" * 50)
    logger.info(f"file4replacementTest [PID {os.getpid()}] Starting file4replacement e2e test…")

    _activate_plugin_dir(logger)
    _ensure_fixtures_exist(logger)

    try:
        if not EXTERNAL_FIXTURE_FILE.exists():
            logger.error(f"file4replacementTest: External fixture missing: {EXTERNAL_FIXTURE_FILE}")
            return 1
        external_expected = EXTERNAL_FIXTURE_FILE.read_text(encoding="utf-8").strip()

        results = [
            _run_case(logger, lt_url, "Zebra", ZEBRA_FIXTURE_CONTENT,
                      "Zebra (relative, '.' prefix, inside plugin dir)"),
            _run_case(logger, lt_url, "Blumenkohl", external_expected,
                      "Blumenkohl (absolute path, outside plugin dir)"),
        ]

        failed = [r for r in results if not r[0]]
        if failed:
            for success, actual, expected, description in failed:
                logger.error(
                    f"file4replacementTest: FAILED: {description} | "
                    f"expected='{expected}' actual='{actual}'"
                )
            return 1

        print(':file4replacementTest:🌞🌞🌞🌞🌞 ')
        logger.info("############################################")
        logger.info("👍 file4replacementTest: All cases PASSED.")
        print(':file4replacementTest:👍 file4replacementTest: All cases PASSED.')
        logger.info("############################################")
        return 0

    finally:
        _deactivate_plugin_dir(logger)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    test_logger = logging.getLogger("file4replacement_e2e_test")
    test_logger.propagate = False

    lt_url_cli = "http://localhost:8082"
    status = run_file4replacement_e2e_test(test_logger, lt_url_cli)
    raise SystemExit(status)
