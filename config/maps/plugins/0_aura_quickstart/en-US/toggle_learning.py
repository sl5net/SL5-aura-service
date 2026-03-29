import os
from pathlib import Path

def execute(match_data):
    # Find map file in current folder
    map_file = Path(__file__).parent / "FUZZY_MAP_pre.py"
    if not map_file.exists():
        return "Error: FUZZY_MAP_pre.py not found."

    content = map_file.read_text(encoding="utf-8")
    original_text = match_data.get('original_text', '').lower()

    plugin_id = "collect_unmatched.py"
    is_off = any(word in original_text for word in ["off", "stop", "deactivate", "disable"])

    lines = content.splitlines()
    new_lines = []
    status = "No changes made."

    for line in lines:
        if plugin_id in line:
            if is_off:
                if not line.strip().startswith("#"):
                    new_lines.append("# " + line.lstrip())
                    status = "Learning mode DISABLED. Back to normal dictation."
                else:
                    new_lines.append(line)
                    status = "Learning mode was already off."
            else:
                if line.strip().startswith("#"):
                    new_lines.append(line.replace("#", "", 1).strip())
                    status = "Learning mode ENABLED. I am learning your new words now!"
                else:
                    new_lines.append(line)
                    status = "Learning mode is already active."
        else:
            new_lines.append(line)

    map_file.write_text("\n".join(new_lines), encoding="utf-8")
    return status
