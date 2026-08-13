# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/anki_quiz/de-DE/debug_json.py


import json
from pathlib import Path

POSSIBLE_PATHS = [
    Path("quiz_db.json"),
    Path("de-DE/quiz_db.json"),
    Path("config/maps/plugins/anki_quiz/de-DE/quiz_db.json"),
    Path("../config/maps/plugins/anki_quiz/de-DE/quiz_db.json"),
]

DB_PATH = None
for p in POSSIBLE_PATHS:
    if p.exists():
        DB_PATH = p
        break

if DB_PATH is None:
    print("DEBUG_JSON: DB_PATH is None -> skip Check.")
    pass
else:
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        json.loads(content)

        # print("SUCCESS: JSON valid!")


    except json.JSONDecodeError as e:
        print(f"\n🛑 CRITICAL ERROR in '{DB_PATH.resolve()}'")
        print(f"   {e.msg}")
        print(f" line: {e.lineno}, col: {e.colno} (pos: {e.pos})")

        START = max(0, e.pos - 60)
        END = min(len(content), e.pos + 60)

        print("\n--- (preview) ---")
        try:
            print(content[START:END])
            print(" " * (e.pos - START) + "^-- look")

        except Exception as e:
            print(f"{e}\n")
            pass
        print("-------------------------------------\n")

    except Exception as e:
        print(f"Error by read JSON: {e}")
