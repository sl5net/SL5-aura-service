# script/py/func/normalize_punctuation.py

import re
from typing import Tuple


def normalize_punctuation(text: str, punctuation_map: dict) -> Tuple[str, bool]:
    """
    Replaces text based on a map, returning the new text and a flag.

    Args:
        text: The input string.
        punctuation_map: A dictionary of phrases to replace.

    Returns:
        A tuple: (processed_text: str, was_exact_match: bool).
        The boolean is True only if the entire input text was an exact key
        in the map, signaling that no further processing should occur.
    """
    lower_punctuation_map = {k.lower(): v for k, v in punctuation_map.items()}

    # First, check for an exact, case-insensitive match of the whole string
    if text.strip().lower() in lower_punctuation_map:
        return lower_punctuation_map[text.strip().lower()], True

    # If no exact match, proceed with regex for partial replacements
    pattern = r'\b(' + '|'.join(re.escape(k) for k in sorted(lower_punctuation_map, key=len, reverse=True)) + r')\b'

    processed_text = re.sub(
        pattern,
        lambda m: lower_punctuation_map.get(m.group(1).lower(), m.group(1)),
        text,
        flags=re.IGNORECASE
    )

    return processed_text, False