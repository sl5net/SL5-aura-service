# config/maps/plugins/anki_quiz/de-DE/anki_logic.py:1
import json
import time

import platform
from datetime import datetime
from pathlib import Path
import re


from bs4 import BeautifulSoup
import subprocess

# from nltk import clean_html

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
else:
    TMP_DIR = Path("/tmp")

# Pfade innerhalb des Plugin-Ordners
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "quiz_db.json"
STATE_PATH = BASE_DIR / "state.json"
QUIZ_TAB = "Aura-Quiz"

# UNICODE_NUMS = {1: "⓵", 2: "⓶", 3: "⓷"}
# UNICODE_NUMS = {1: "⓵", 2: "⓶", 3: "⓷"}
# UNICODE_NUMS = {1: "⓵", 2: "➋", 3: "⒊"}
UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}
# ① ② ③
# 🄌 ➊ ➋ ➌ ➍ ➎ ➏ ➐ ➑ ➒ ➓
# 🄀 ⒈ ⒉ ⒊ ⒋ ⒌ ⒍ ⒎ ⒏ ⒐ ⒑ ⒒ ⒓ ⒔ ⒕ ⒖ ⒗ ⒘ ⒙ ⒚ ⒛
# 0️# 1️# 2️# 3️
# 0 1 2 3


def show_current_question(user_choice):
    with open(DB_PATH, "r") as f: db = json.load(f)
    with open(STATE_PATH, "r") as f: state = json.load(f)
    # Anzeige in CopyQ aktualisieren
    subprocess.run(["copyq", "tab", QUIZ_TAB, "remove", "0"], stderr=subprocess.DEVNULL)
    t= db[state["index"]]["display"]

    soup = BeautifulSoup(t, "html.parser")  # oder "lxml"
    cleaned = soup.get_text(strip=True)

    # remove NBSP and zero-width spaces
    cleaned = re.sub(r"[\u00A0\u200B\u200C\u200D]+", "", cleaned)


    symbol1 = UNICODE_NUMS.get(1, f"{1})")
    symbol2 = UNICODE_NUMS.get(2, f"{2})")
    symbol3 = UNICODE_NUMS.get(3, f"{3})")


    safe_p = r'(^|[^,\(=+\-*/\[])(\s*)'
    safe_p2 = r'(?!\))'

    cleaned = re.sub(safe_p + r'(1\))' + safe_p2, rf'\1\2 \n```\n {symbol1} ', cleaned)
    cleaned = re.sub(safe_p + r'(2\))' + safe_p2, rf'\1\2 \n {symbol2} ', cleaned)
    cleaned = re.sub(safe_p + r'(3\))' + safe_p2, rf'\1\2 \n {symbol3} ', cleaned)



    # cleaned = re.sub(r'([1]\))', rf' ZZZZ \n\n {symbol1} ', cleaned)
    # cleaned = re.sub(r'([2]\))', rf' ZZZZ \n\n {symbol2} ', cleaned)
    # cleaned = re.sub(r'([3]\))', rf' ZZZZ \n\n {symbol3} ', cleaned)
    # cleaned = re.sub(r'([2-3]\))', r' ZZZZ \n\n \1 ', cleaned)
    # cleaned = re.sub(r'([1-3]\))', r' ZZZZ \n\n \1 ', cleaned)



    # antwort bis 3Falsch, nochmal!Richtig!

    subprocess.run(["copyq", "tab", QUIZ_TAB, "add", cleaned], check=True)

    # Falsch, nochmal!Falsch, nochmal! tja und hat Richtig!ich 2die antwort ist 2 die antwort ist 1Falsch, nochmal!

    # t = clean_html(t)
    # subprocess.run(["copyq", "tab", QUIZ_TAB, "add", t])

    # backup_AUTO_ENTER_AFTER_DICTATION_global = settings.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS


    log_question(cleaned,user_choice)

    # try:
    #     AUTO_ENTER_AFTER_DICTATION_global = backup_AUTO_ENTER_AFTER_DICTATION_global
    #     auto_enter_flag_path = "/tmp/sl5_auto_enter.flag"
    #     with open(auto_enter_flag_path, "w") as f:
    #         f.write(str(AUTO_ENTER_AFTER_DICTATION_global)) # Writes 1 or 0
    #     # logger.info(f"Set auto-enter flag to: {AUTO_ENTER_AFTER_DICTATION_global}")
    # except Exception as e:
    #     print(f"Could not write auto-enter flag file: {e}")
        # logger.error(f"Could not write auto-enter flag file: {e}")


    subprocess.run(["copyq", "show"])



# Antwort bis dahinRichtig!Richtig!Falsch, nochmal!irgendwas ist 3Falsch, nochmal!Richtig!


# In anki_logic.py
LOG_FILE = BASE_DIR / "QuizProtokoll.md"

def log_question(text,user_choice):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        if user_choice:
            f.write(f"Richtig! Ja {user_choice} war richtig.\n")
        f.write("\nNächste Aufgabe:\n")

        f.write("\n/" + "‾"*40 + "\n")
        f.write(f"Zeit: {datetime.now().strftime('%H:%M:%S')}\n")
        f.write("\n```python\n")
        f.write(text + "\n")
        # f.write("```\n")
        f.write("\\" + "_"*40 + "\n\n")



# def unique_output_file_write_text(text):
#     timestamp = time.time()
#     unique_output_file = TMP_DIR / f"sl5_aura/tts_output_anki_{timestamp}.txt"
#     unique_output_file.write_text(text, encoding="utf-8-sig")




def execute(match_data):
    spoken = match_data['regex_match_obj'].group(0).lower()
    if "start" in spoken:
        with open(STATE_PATH, "w") as f: json.dump({"index": 0}, f)
        show_current_question(None)
        return "Quiz gestartet"

    # Antwort-Logik
    user_choice = int(match_data['regex_match_obj'].group(1))
    with open(DB_PATH, "r") as f:
        db = json.load(f)
    with open(STATE_PATH, "r") as f:
        state = json.load(f)

    if user_choice == db[state["index"]]["correct"]:
        state["index"] = (state["index"] + 1) % len(db)
        with open(STATE_PATH, "w") as f: json.dump(state, f)
        show_current_question(user_choice)
        return " "
        # return "Richtig!"
    # return " "
    return "Falsch, nochmal!"



