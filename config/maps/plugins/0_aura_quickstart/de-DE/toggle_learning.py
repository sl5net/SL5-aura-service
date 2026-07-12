# config/maps/plugins/0_aura_quickstart/de-DE/toggle_learning.py
import subprocess
from pathlib import Path

from scripts.py.func.config.dynamic_settings import settings
from scripts.py.func.utils.get_leading_whitespace import get_leading_whitespace_before_pos

def speak(text):
    try:
        subprocess.run(['espeak', '-v', 'en-US', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

def execute(match_data):
    # its from config/maps/plugins/0_aura_quickstart/de-DE/FUZZY_MAP_pre.py
    # german EXAMPLE: Lernmodus einschalten ausschalten
    # english EXAMPLE: learn-mode enable disable

    import os
    tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
    last_edited_file = tmp_dir / "sl5_aura" / "last_edited_map.txt"
    candidate_path = Path(last_edited_file.read_text(encoding="utf-8").strip()).expanduser()
    if not candidate_path.exists():
        speak(f"Can't find {last_edited_file}")
        print(f"Can't find {last_edited_file}")
        return "Error reading last_edited_map.txt"


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

    is_turning_off = any(word in original_text for word in ["aus", "ab", "stopp", "beende", "dea", "dis"])

    if is_turning_off:
        try:
            if last_edited_file.exists():
                last_edited_file.unlink()
            if settings.AUDIO_GUIDANCE_ENABLED:
                speak("last edited file is deleted.")

        except Exception:
            speak(f"Error deleting {last_edited_file}")
            print(f"Error deleting {last_edited_file}")
            pass

    for line in lines:
        if training_plugin_string in line:
            if is_turning_off:
                if not line.strip().startswith("#"):

                    # leading_ws = get_leading_whitespace_of_line(line)

                    # new_lines.append(leading_ws + "# " + line.strip())
                    # we just not add this line anymore. map is then less messy

                    status = "Lernmodus DEAKTIVIERT."
                else:
                    new_lines.append(line)
                    status = "Lernmodus is already deaktivated"
            else:
                # remove comment
                if line.strip().startswith("#"):
                    idx = line.find("#")
                    prefix = line[:idx]
                    suffix = line[idx+1:]
                    if suffix.startswith(" "):
                        suffix = suffix[1:]
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
                        return f"unmatched is added to your map …{str(map_file)[-30:0]} (20260711_2331)"

    map_file.write_text("\n".join(new_lines), encoding="utf-8")

    if settings.AUDIO_GUIDANCE_ENABLED:
        speak("unmatched is added to your map")
    return status
