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

# config/maps/plugins/anki_quiz/de-DE/anki_logic.py:1

import json
import os

import platform
import shutil
# from datetime import datetime

from pathlib import Path
import re


from bs4 import BeautifulSoup
import subprocess

UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}


import time


# import time


# from nltk import clean_html


if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
else:
    TMP_DIR = Path("/tmp")

# Paths within the plugin folder

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "quiz_db.json"
STATE_PATH = BASE_DIR / "state.json"
QUIZ_TAB = "Aura-Quiz"
# Time intervals for the boxes (in seconds)

# Box 0: immediately, Box 1: 5 minutes, Box 2: 4 hours, Box 3: 1 day, Box 4: 3 days

BOX_INTERVALS = [0, 300, 14400, 86400, 259200]


copyq_exe = "copyq"
if platform.system() == "Windows":
    # Check typical installation paths

    potential_paths = [
        r"C:\program Files\CopyQ\copyq.exe",
        r"C:\program Files (x86)\CopyQ\copyq.exe"
    ]
    for p in potential_paths:
        if os.path.exists(p):
            copyq_exe = p
            break




def get_state():
    with open(STATE_PATH, "r") as f:
        state = json.load(f)
    return state

def save_state(state):
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)

def find_next_due_card(db, state):
    now = time.time()
    progress = state["progress"]

    # 1. Find cards that are "due" (next_review <= now)

    due_cards = []
    for idx_str in range(len(db)):
        idx = str(idx_str)
        card_data = progress.get(idx, {"box": 0, "next_review": 0})

        if card_data["next_review"] <= now:
            due_cards.append(int(idx))

    if not due_cards:
        return None # Nichts zu tun! (Oder wir nehmen die mit der kleinsten Wartezeit)

    # Take the first card due (or random)

    return due_cards[0]


def show_current_question(user_choice):
    with open(DB_PATH, "r") as f: db = json.load(f)
    with open(STATE_PATH, "r") as f: state = json.load(f)
    state = get_state()
    next_id = find_next_due_card(db, state)

    if next_id is None:
        # No tickets due!

        msg = "Glückwunsch! Alle Karten für jetzt erledigt."


        if shutil.which(copyq_exe):
            subprocess.run([copyq_exe, "tab", QUIZ_TAB, "add", msg])
            subprocess.run([copyq_exe, "show"])
        else:
            # fallback behavior or log a clear error

            print("copyq not found; skipping copyq-based actions")

        return

    # Save that we're looking at this map

    state["current_id"] = next_id
    save_state(state)




    # Refresh display in CopyQ


    if shutil.which(copyq_exe):
        subprocess.run([copyq_exe, "tab", QUIZ_TAB, "remove", "0"], stderr=subprocess.DEVNULL)
    else:
        # fallback behavior or log a clear error

        print("copyq not found; skipping copyq-based actions")


    # current_id was stored as a number (next_id) — use it as an index

    current_id = state.get("current_id", next_id)
    t = db[int(current_id)]["display"]



    soup = BeautifulSoup(t, "html.parser")  # or "lxml"
    cleaned = soup.get_text(strip=True)

    # remove NBSP and zero-width spaces

    cleaned = re.sub(r"[\u00A0\u200B\u200C\u200D]+", "", cleaned)


    symbol1 = UNICODE_NUMS.get(1, f"{1})")
    symbol2 = UNICODE_NUMS.get(2, f"{2})")
    symbol3 = UNICODE_NUMS.get(3, f"{3})")


    safe_p = r'(^|[^"\'\.,\(=+\-*/\[])(\s*)'
    safe_p2 = r'(?!\))'

    cleaned = re.sub(safe_p + r'(1\))' + safe_p2, rf'\1\2 \n```\n {symbol1} ', cleaned)
    cleaned = re.sub(safe_p + r'(2\))' + safe_p2, rf'\1\2 \n {symbol2} ', cleaned)
    cleaned = re.sub(safe_p + r'(3\))' + safe_p2, rf'\1\2 \n {symbol3} ', cleaned)

    if shutil.which(copyq_exe):
        subprocess.run([copyq_exe, "tab", QUIZ_TAB, "add", cleaned], check=True)
    else:
        # fallback behavior or log a clear error

        print("copyq not found; skipping copyq-based actions")

    log_question(cleaned,user_choice)

    if shutil.which(copyq_exe):
        subprocess.run([copyq_exe, "show"])
    else:
        # fallback behavior or log a clear error

        print("copyq not found; skipping copyq-based actions")


# In anki_logic.py

LOG_FILE = BASE_DIR / "QuizProtokoll.md"

def log_question(text,user_choice):

    # text = r'(^|[^,\(=+\-*/\[])(\s*)'


    text = re.sub(r'\n[ ]*\n' , '\n', text)
    text = re.sub(r'\n[ ]*\n' , '\n', text)


    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if user_choice:
            f.write(f"Richtig! Ja {user_choice} war richtig. ")
        f.write("Nächste Aufgabe:\n")

        f.write("/" + "‾"*40 + "\n")
        # f.write(f"Time: {datetime.now().strftime('%H:%M:%S')}\n")

        f.write("```python\n")
        f.write(text + "\n")
        f.write("\\" + "_"*40 + "\n")

def execute(match_data):
    spoken = match_data['regex_match_obj'].group(0).lower()
    if "start" in spoken:
        with open(STATE_PATH, "w") as f: json.dump({"index": 0}, f)
        show_current_question(None)
        return "Quiz gestartet"

    user_choice = int(match_data['regex_match_obj'].group(1))

    with open(DB_PATH, "r") as f:
        db = json.load(f)

    state = get_state()
    current_id = str(state.get("current_id", "0"))

    if "progress" not in state:
        state["progress"] = {}

    # Load previous map progress

    card_prog = state["progress"].get(current_id, {"box": 0, "next_review": 0})

    correct_answer = db[int(current_id)]["correct"]

    if user_choice == correct_answer:
        new_box = card_prog["box"] + 1
        if new_box >= len(BOX_INTERVALS):
            new_box = len(BOX_INTERVALS) - 1 # Max Level erreicht

        wait_time = BOX_INTERVALS[new_box]
        card_prog["box"] = new_box
        card_prog["next_review"] = int(time.time() + wait_time)

        # feedback = "Correct! (Box " + str(new_box) + ")"


        # Save & Next Question

        state["progress"][current_id] = card_prog
        save_state(state)
        show_current_question(user_choice)


        return " " # oder feedback

    else:
        card_prog["box"] = 0
        # card_prog["next_review"] = time.time() # Repeat immediately

        card_prog["next_review"] = int(time.time())

        state["progress"][current_id] = card_prog
        save_state(state)

        print("DEBUG current_id (state):", current_id, "type:", type(current_id))
        print("DEBUG db len:", len(db))
        print("DEBUG db entry index int(current_id):", int(current_id), "correct:", db[int(current_id)].get("correct"))


        return (f"Falsch! Du wähltest {user_choice}. "
                f"Richtig ist {correct_answer}. "
                f"(Das ist Frage-ID {current_id})")
