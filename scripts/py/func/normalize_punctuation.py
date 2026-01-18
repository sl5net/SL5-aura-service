# script/py/func/normalize_punctuation.py

import re
from typing import Tuple

from .log_memory_details import log4DEV

from scripts.py.func.config.dynamic_settings import DynamicSettings

settings = DynamicSettings()


def normalize_punctuation(text: str, punctuation_map: dict, logger2) -> Tuple[str, bool]:
    global settings # noqa: F824
    log4DEV(f'📍 START normalize_punctuation: "{text}"', logger2)

    if not punctuation_map:
        log4DEV(f'📍 Map is empty, skipping.', logger2)
        return text, False

    lower_map = {k.lower(): v for k, v in punctuation_map.items()}
    search_text = text.strip().lower()
    if getattr(settings, "DEV_MODE_all_processing", False):
        log4DEV(f'📍 Available Keys: {list(lower_map.keys())[:10]}... (Total: {len(lower_map)})', logger2)

    # Exact Match Check
    if search_text in lower_map:
        res = lower_map[search_text]
        log4DEV(f'📍 EXACT MATCH: "{search_text}" -> "{res}"', logger2)
        return res, True

    # Partial/Regex Match
    try:
        keys = sorted(lower_map.keys(), key=len, reverse=True)
        pattern = r'\b(' + '|'.join(re.escape(k) for k in keys) + r')\b'
        log4DEV(f'📍 REGEX Pattern build with {len(keys)} keys.', logger2)

        processed = re.sub(
            pattern,
            lambda m: lower_map.get(m.group(1).lower(), m.group(1)),
            text,
            flags=re.IGNORECASE
        )
        log4DEV(f'📍 RESULT: "{processed}" (was_exact=False)', logger2)
        return processed, False
    except Exception as e:
        log4DEV(f'📍 ERROR during normalization: {e}', logger2)
        return text, False
