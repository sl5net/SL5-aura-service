# config/maps/plugins/1_collect_unmatched_training/collect_unmatched.py
import subprocess
from pathlib import Path
import re
import sys

from scripts.py.func.config.dynamic_settings import settings

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

    # Ignore empty text and system status messages
    if not text or "Lernmodus" in text:
        return None

    file_rule_path = match_data['text_after_replacement']
    print(f'file_rule_path: {file_rule_path}')

    if not text:
        print(f'ERROR: text empty {text}')
        return None
    success = _add_variant_to_fuzzy_map(file_rule_path, text)
    if success:
        sys.exit(1)
    return None


def _add_variant_to_fuzzy_map(file_rule_path: str, text: str) -> bool:
    import os
    import datetime
    target_path = None

    # 1. Prioritize last edited map path
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    last_edited_file = tmp_dir / "sl5_aura" / "last_edited_map.txt"
    if last_edited_file.exists():
        try:
            candidate_path = Path(last_edited_file.read_text(encoding="utf-8").strip()).expanduser()
            if candidate_path.exists():
                target_path = candidate_path
        except Exception as e:
            print(f"Error reading last_edited_map.txt: {e}")

    # 2. Fall back to the explicitly passed path
    if not target_path and file_rule_path:
        expanded_path = Path(file_rule_path).expanduser()
        if expanded_path.exists() and "FUZZY_MAP_pre.py" in str(expanded_path):
            target_path = expanded_path

    if not target_path:
        msg = "Fehler: Keine Karte zum Lernen bekannt."
        print(f"ERROR: {msg}")
        try:
            speak(msg)
        except Exception:
            pass
        return False

    FUZZY_MAP_FILE = target_path
    try:
        tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
        root_file = tmp_dir / "sl5_aura" / "sl5net_aura_project_root"
        if root_file.exists():
            project_root = Path(root_file.read_text(encoding="utf-8").strip())
            log_file = project_root / "log" / "collect_unmatched.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"{timestamp} - Added '{text}' to {FUZZY_MAP_FILE}\n")
    except Exception as e:
        print(f"Error logging collection: {e}")

    content = FUZZY_MAP_FILE.read_text(encoding="utf-8")
    pattern_with_alts = re.compile(r"(r'\^\()([^)]+)(\)\$')")
    pattern_simple = re.compile(r"r'\^([^('\\][^']*?)\$'")
    match = None
    match_type = None
    match_line_start = None
    for line_match in re.finditer(r'^[^#\n][^\n]*', content, re.MULTILINE):
        line = line_match.group()
        if 'collect_unmatched' in line:
            continue
        m = pattern_with_alts.search(line)
        if m:
            if m.group(2) == '.*':
                continue
            match, match_type, match_line_start = m, 'alts', line_match.start()
            break
        m = pattern_simple.search(line)
        if m:
            match, match_type, match_line_start = m, 'simple', line_match.start()
            break

    if not match:
        return False

    if match_type == 'alts':
        abs_start_g2 = match_line_start + match.start(2)
        abs_end_g2   = match_line_start + match.end(2)
        variants = match.group(2).split("|")
        if text in variants:
            return False
        variants.append(text)
        new_content = content[:abs_start_g2] + "|".join(variants) + content[abs_end_g2:]
    else:
        existing = match.group(1)
        if existing == text:
            return False
        abs_start = match_line_start + match.start()
        abs_end   = match_line_start + match.end()
        new_content = content[:abs_start] + f"r'^({existing}|{text}|Programm geladen. Viel Spaß|Program loaded)$'" + content[abs_end:]

    FUZZY_MAP_FILE.write_text(new_content, encoding="utf-8")
    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("unmatched is added to your map")
    return True
