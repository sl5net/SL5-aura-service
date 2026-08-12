#!/usr/bin/env python3
# scripts/py/func/get_current_search_language.py
"""CLI wrapper: prints the current LanguageTool language code
derived from config/model_name.txt, for use by shell scripts."""
import logging
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[2]
VOSK_MODEL_FILE = PROJECT_ROOT / "config" / "model_name.txt"

sys.path.insert(0, str(PROJECT_ROOT))
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model


def main():
    logger = logging.getLogger("get_current_search_language")
    logger.addHandler(logging.NullHandler())

    try:
        model_name = VOSK_MODEL_FILE.read_text(encoding="utf-8").strip()
    except OSError:
        model_name = ""

    if not model_name:
        print("de-DE")
        return

    print(guess_lt_language_from_model(logger, model_name))


if __name__ == "__main__":
    main()

