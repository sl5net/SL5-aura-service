# config/maps/plugins/0_aura_quickstart/de-DE/toggle_learning.py
import subprocess
from pathlib import Path

from scripts.py.func.config.dynamic_settings import settings

import re
from pathlib import Path

def get_leading_whitespace_of_line(line: str) -> str:
    """
    Gibt die führenden Whitespaces (Tabs oder Spaces) der übergebenen Zeile zurück.
    Leerstring, wenn keine führenden Whitespaces vorhanden sind.
    """
    m = re.match(r"\s*", line)
    return m.group() if m else ""

# Wenn du die Einrückung aus dem Inhalt ermitteln willst (z.B. letzte Listeneintrag-Zeile)
def get_leading_whitespace_before_pos(content: str, pos: int, fallback: str = "    ") -> str:
    """
    Suche die letzte nicht-leere Zeile vor pos und gib deren führende Whitespaces zurück.
    Wenn nichts passendes gefunden wird, wird fallback zurückgegeben.
    """
    # Begrenze pos sicher innerhalb content
    pos = max(0, min(len(content), pos))
    # Finde Zeilenanfang der Zeile, die pos enthält
    line_start = content.rfind("\n", 0, pos)
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1

    # Gehe rückwärts, bis wir eine nicht-leere Zeile finden oder am Anfang sind
    search_pos = line_start
    while True:
        # Finde Zeilenende
        next_nl = content.find("\n", search_pos)
        if next_nl == -1 or next_nl >= pos:
            next_nl = pos
        line = content[search_pos:next_nl]
        if line.strip() != "":
            return get_leading_whitespace_of_line(line)
        # gehe zur vorherigen Zeile
        prev_nl = content.rfind("\n", 0, search_pos - 1)
        if prev_nl == -1:
            # prüfe von Anfang bis search_pos
            if content[:search_pos].strip() == "":
                return fallback
            search_pos = 0
        else:
            search_pos = prev_nl + 1
        if search_pos == 0:
            # letzte Chance: erste Zeile
            first_line = content[:pos].splitlines()[0] if content[:pos].splitlines() else ""
            return get_leading_whitespace_of_line(first_line) if first_line else fallback

def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'en-US', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

def execute(match_data):
    # its from config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py
    # EXAMPLE: Lernmodus einschalten ausschalten

    # 2. Die Map-Datei in diesem Ordner finden
    import os
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    last_edited_file = tmp_dir / "sl5_aura" / "last_edited_map.txt"
    candidate_path = Path(last_edited_file.read_text(encoding="utf-8").strip()).expanduser()
    if not candidate_path.exists():
        speak(f"Can't find {last_edited_file}")
        print(f"Can't find {last_edited_file}")
        return f"Error reading last_edited_map.txt"


    # map_file = Path(__file__).parent / "FUZZY_MAP_pre.py"
    map_file = Path(candidate_path)
    if not map_file.exists():
        speak(f"No map file found at {candidate_path}")
        return f"No map file found at {candidate_path}"


    # is = map_file_is_modified  maybe the same when __file given  is the same


    content = map_file.read_text(encoding="utf-8")
    original_text = match_data.get('original_text', '').lower()

    # Wonach suchen wir in der Datei?
    training_plugin_string = "collect_unmatched.py"

    lines = content.splitlines()
    new_lines = []
    status = "Keine Änderung vorgenommen."

    # Logik: An- oder Ausschalten
    is_turning_off = any(word in original_text for word in ["aus", "ab", "stopp", "beende", "deakti"])

    if is_turning_off:
        try:
            if last_edited_file.exists():
                last_edited_file.unlink()
            speak("last edited file is deleted.")

        except Exception as e:
            speak(f"Error deleting {last_edited_file}")
            print(f"Error deleting {last_edited_file}")
            pass

    for line in lines:
        if training_plugin_string in line:
            if is_turning_off:
                if not line.strip().startswith("#"):

                    leading_ws = get_leading_whitespace_of_line(line)

                    new_lines.append(leading_ws + "# " + line.strip())
                    status = "Lernmodus DEAKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus is already deaktivated"
            else:
                # Aktivieren: Nur wenn es auskommentiert ist
                if line.strip().startswith("#"):
                    # Wir suchen die Position des ersten '#'
                    idx = line.find("#")
                    # Wir nehmen alles VOR dem '#' (die originale Einrückung)
                    prefix = line[:idx]
                    # Wir nehmen alles NACH dem '#' und entfernen EIN optionales Leerzeichen
                    suffix = line[idx+1:]
                    if suffix.startswith(" "):
                        suffix = suffix[1:]

                    # Wir setzen es wieder zusammen: Einrückung + originaler Code
                    new_lines.append(prefix + suffix)
                    status = "Lernmodus AKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus ist bereits aktiv."
        else:
            status = "Learn-modus rule not found. "
            if is_turning_off:
                new_lines.append(line)
            if not is_turning_off:

                status = "Learn-modus rule not found. it will be added now."
                new_lines.append(line)

                # Append new rule if list exists
                if "FUZZY_MAP_pre = [" in content:
                    idx = content.rfind("]")
                    if idx != -1:
                        leading_ws = get_leading_whitespace_before_pos(content, idx)

                        new_rule = leading_ws + r"(f'{str(__file__)}', r'^(.*)$', 10, {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']})," + "\n\n"
                        new_content = content[:idx] + new_rule + content[idx:]
                        map_file.write_text(new_content, encoding="utf-8")
                        if settings.AUDIO_GUIDANCE_ENABLED:
                            speak("unmatched is added to your map")
                        return f"unmatched is added to your map (20260711_2331) …{str(candidate_path)[-30:0]}"


    map_file.write_text("\n".join(new_lines), encoding="utf-8")



    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("unmatched is added to your map")


    return status

