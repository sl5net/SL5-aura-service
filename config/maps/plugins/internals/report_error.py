# config/maps/plugins/internals/report_error.py:1
from datetime import datetime
from pathlib import Path



from scripts.py.func import global_state

def between_first_last_hash_manual(s: str) -> str:
    try:
        start = s.index('#') + 1
        end = s.rindex('#')
    except ValueError:
        return ''
    return s[start:end].strip()

def execute(match_data):
    from scripts.py.func.audio_manager import speak_inclusive_fallback
    root = Path(__file__).resolve().parents[4]
    report_file = root / "docs" / "bugfix" / "TODO" / "misrecognitions.md"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_file.parent.mkdir(parents=True, exist_ok=True)

    history = global_state.last_recognitions

    if len(history) >= 2:
        # Index 0 is the "previous" entry (the one that failed)
        # Index 1 is the current "report error" command
        error_line = history[0]
    elif len(history) == 1:
        error_line = history[0]
    else:
        error_line = "No recent input found in memory."
        print(error_line)
        returns= "Error in Log found (20260718_1100)."
        speak_inclusive_fallback(f"{returns}", 'de-DE')
        return returns


    # write in the TODO-list
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(f"📢 {timestamp}:\n{error_line}\n")
    return " internals>misrecognitions "

