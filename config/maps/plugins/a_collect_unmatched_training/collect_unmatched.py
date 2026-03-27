
from pathlib import Path
import re
import sys


FUZZY_MAP_FILE = Path(__file__).parent / "de-DE" / "FUZZY_MAP_pre.py"
COLLECT_FILE   = Path(__file__).parent / ".." / ".." / ".." / "unmatched_list.txt"

def execute(match_data: dict):
    # text = match_data.get('original_text', '').strip()

    text = match_data['regex_match_obj'].group(0).strip()

    if not text:
        print(f'ERROR: text empty {text}')
        return None
    _add_variant_to_fuzzy_map(text)
    sys.exit(1)

def _add_variant_to_fuzzy_map(text: str):
    if not FUZZY_MAP_FILE.exists():
        return
    content = FUZZY_MAP_FILE.read_text(encoding="utf-8")
    pattern = re.compile(r"(r'\^\()([^)]+)(\)\$')")
    match = pattern.search(content)
    if not match:
        return
    variants = match.group(2).split("|")
    if text in variants:
        return
    variants.append(text)
    new_content = content[:match.start(2)] + "|".join(variants) + content[match.end(2):]
    FUZZY_MAP_FILE.write_text(new_content, encoding="utf-8")
