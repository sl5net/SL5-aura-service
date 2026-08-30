# scripts/test/test_map_language_filter.py
from pathlib import Path

from scripts.py.func.get_current_language import get_current_language
from scripts.py.func.is_map_path_for_current_language import (
    is_map_path_for_current_language,
)

VERBOSE_OUTPUT = True

def _log_step(message: str) -> None:
    if VERBOSE_OUTPUT:
        print(f"  - {message}")

def test_map_language_filter():
    active_lang = "de-DE"

    _log_step("----------------")
    _log_step("PYTHONPATH=. python3 scripts/test/test_map_language_filter.py")
    _log_step("Verifying matching active language maps are accepted…")
    assert is_map_path_for_current_language(Path("wake-up/de-DE/FUZZY_MAP.py"), active_lang) is True
    assert is_map_path_for_current_language(Path("plugins/action/de-DE/rule.py"), active_lang) is True

    _log_step("Verifying foreign language maps are skipped…")
    assert is_map_path_for_current_language(Path("wake-up/en-US/FUZZY_MAP.py"), active_lang) is False
    assert is_map_path_for_current_language(Path("wake-up/fr-FR/FUZZY_MAP.py"), active_lang) is False
    assert is_map_path_for_current_language(Path("plugins/action/es-ES/rule.py"), active_lang) is False

    _log_step("Verifying language-neutral maps are accepted…")
    assert is_map_path_for_current_language(Path("common/rules.py"), active_lang) is True
    assert is_map_path_for_current_language(Path("quickstart.py"), active_lang) is True

    _log_step("Verifying language detection from model configuration…")
    detected = get_current_language()
    assert isinstance(detected, str) and len(detected) >= 2
    _log_step(f"Detected language: '{detected}'")


if __name__ == "__main__":
    test_map_language_filter()
    print("ALL_TESTS_PASSED")
