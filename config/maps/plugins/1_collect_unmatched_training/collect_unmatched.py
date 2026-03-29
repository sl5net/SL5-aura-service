
from pathlib import Path
import re
import sys


FUZZY_MAP_FILE = Path(__file__).parent / "de-DE" / "FUZZY_MAP_pre.py"
COLLECT_FILE   = Path(__file__).parent / ".." / ".." / ".." / "unmatched_list.txt"

def execute(match_data: dict):
    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']

    print(f'file_rule_path: {file_rule_path}')

    if not text:
        print(f'ERROR: text empty {text}')
        return None
    _add_variant_to_fuzzy_map(file_rule_path, text)
    sys.exit(1)

def _add_variant_to_fuzzy_map(file_rule_path: str, text: str):
    FUZZY_MAP_FILE = Path(file_rule_path)
    if not FUZZY_MAP_FILE.exists():
        return
    content = FUZZY_MAP_FILE.read_text(encoding="utf-8")

    pattern = re.compile(r"(r'\^\()([^)]+)(\)\$')")

    # Nur nicht-kommentierte Zeilen durchsuchen
    match = None
    match_line_start = None
    for line_match in re.finditer(r'^[^#\n][^\n]*', content, re.MULTILINE):
        m = pattern.search(line_match.group(), )
        if m:
            match = m
            match_line_start = line_match.start()
            break

    if not match:
        return

    # Absoluten Offset im Gesamtinhalt berechnen
    # abs_start = match_line_start + match.start()
    abs_end_g2 = match_line_start + match.end(2)
    abs_start_g2 = match_line_start + match.start(2)

    variants = match.group(2).split("|")
    if text in variants:
        return
    variants.append(text)

    new_content = content[:abs_start_g2] + "|".join(variants) + content[abs_end_g2:]
    FUZZY_MAP_FILE.write_text(new_content, encoding="utf-8")

