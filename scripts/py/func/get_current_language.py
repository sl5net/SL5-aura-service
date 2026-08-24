# scripts/py/func/get_current_language.py
import logging
from pathlib import Path
from .guess_lt_language_from_model import guess_lt_language_from_model


def get_current_language(logger=None, project_root: Path | None = None) -> str:
    if logger is None:
        logger = logging.getLogger("get_current_language")
        logger.addHandler(logging.NullHandler())
    """
    Returns the active language code derived from config/model_name.txt.
    Defaults to 'de-DE' if unavailable.
    """
    if project_root is None:
        project_root = Path(__file__).resolve().parents[3]
    model_file = project_root / "config" / "model_name.txt"
    try:
        model_name = model_file.read_text(encoding="utf-8").strip()
    except OSError:
        model_name = ""
    if not model_name:
        return "de-DE"
    return guess_lt_language_from_model(logger, model_name)
