from pathlib import Path
from .guess_lt_language_from_model import (
    LANG_DEFAULT_REGION_MAP,
    LANG_REGION_PAIR_MAP,
)

ALL_KNOWN_LANGUAGE_CODES = (
    set(LANG_REGION_PAIR_MAP.values())
    | set(LANG_DEFAULT_REGION_MAP.values())
    | set(LANG_DEFAULT_REGION_MAP.keys())
)


def is_map_path_for_current_language(relative_map_path: Path, current_language: str) -> bool:
    """
    Checks whether a map file path belongs to current_language or is language-neutral.
    Cross-platform compatibility is guaranteed via Path.parts.
    """
    parts = relative_map_path.parts
    found_languages = [part for part in parts if part in ALL_KNOWN_LANGUAGE_CODES]
    if not found_languages:
        return True
    return current_language in found_languages
