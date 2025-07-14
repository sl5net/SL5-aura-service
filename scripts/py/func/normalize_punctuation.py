# File: script/py/func/normalize_punctuation.py
import re

def normalize_punctuation(text: str, punctuation_map) -> str:

    lower_punctuation_map = {k.lower(): v for k, v in punctuation_map.items()}
    pattern = r'\b(' + '|'.join(re.escape(k) for k in sorted(lower_punctuation_map, key=len, reverse=True)) + r')\b'
    return re.sub(pattern, lambda m: lower_punctuation_map.get(m.group(1).lower(), m.group(1)), text, flags=re.IGNORECASE)

