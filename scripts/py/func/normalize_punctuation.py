# File: script/py/func/normalize_punctuation.py
import re

from config.languagetool_server.PUNCTUATION_MAP import PUNCTUATION_MAP

def normalize_punctuation(text: str) -> str:
    pattern = r'\b(' + '|'.join(re.escape(k) for k in sorted(PUNCTUATION_MAP, key=len, reverse=True)) + r')\b'
    return re.sub(pattern, lambda m: PUNCTUATION_MAP[m.group(1).lower()], text, flags=re.IGNORECASE)

#