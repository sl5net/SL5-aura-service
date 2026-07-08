# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
import subprocess
from pathlib import Path
import re

from scripts.py.func.config.dynamic_settings import settings
# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py:6


def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'en-US', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")


FUZZY_MAP_FILE = Path(__file__).parent / "de-DE" / "FUZZY_MAP_pre.py"
# COLLECT_FILE   = Path(__file__).parent / ".." / ".." / ".." / "unmatched_list.txt"

def execute(match_data: dict):
    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("collect unmatched")

    text = match_data['original_text']
    file_rule_path = match_data['text_after_replacement']

    print(f'file_rule_path: {file_rule_path}')

    if not text:
        print(f'ERROR: text empty {text}')
        return None
    _add_variant_to_fuzzy_map(file_rule_path, text)
    raise Exception('no text after replacement')


def _add_variant_to_fuzzy_map(file_rule_path: str, text: str):
    FUZZY_MAP_FILE = Path(file_rule_path)
    if not FUZZY_MAP_FILE.exists():
        return
    content = FUZZY_MAP_FILE.read_text(encoding="utf-8")

    # Pattern A: rule already has an alternation group  →  r'^(a|b)$'
    pattern_with_alts = re.compile(r"(r'\^\()([^)]+)(\)\$')")
    # Pattern B: rule has a plain literal (no group yet)  →  r'^hello$'
    pattern_simple = re.compile(r"r'\^([^('\\][^']*?)\$'")

    match = None
    match_type = None
    match_line_start = None

    for line_match in re.finditer(r'^[^#\n][^\n]*', content, re.MULTILINE):
        line = line_match.group()

        # ── Fix 2: skip the plugin's own catch-all entry ──────────────────
        if 'collect_unmatched' in line:
            continue

        # ── Fix 1a: prefer rules that already carry an alternation group ──
        m = pattern_with_alts.search(line)
        if m:
            if m.group(2) == '.*':          # also skip bare catch-all (.*)
                continue
            match, match_type, match_line_start = m, 'alts', line_match.start()
            break

        # ── Fix 1b: also accept plain-literal rules without a group yet ───
        m = pattern_simple.search(line)
        if m:
            match, match_type, match_line_start = m, 'simple', line_match.start()
            break

    if not match:
        return

    if match_type == 'alts':
        # existing: r'^(foo|bar)$'  →  r'^(foo|bar|text)$'
        abs_start_g2 = match_line_start + match.start(2)
        abs_end_g2   = match_line_start + match.end(2)
        variants = match.group(2).split("|")
        if text in variants:
            return
        variants.append(text)
        new_content = content[:abs_start_g2] + "|".join(variants) + content[abs_end_g2:]

    else:  # match_type == 'simple'
        # existing: r'^hello$'  →  r'^(hello|text)$'
        existing = match.group(1)
        if existing == text:
            return
        abs_start = match_line_start + match.start()
        abs_end   = match_line_start + match.end()
        new_content = content[:abs_start] + f"r'^({existing}|{text})$'" + content[abs_end:]

    FUZZY_MAP_FILE.write_text(new_content, encoding="utf-8")
    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("unmatched is added to your map")
