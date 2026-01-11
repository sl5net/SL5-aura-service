#
import json
import re
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup
import subprocess

from nltk import clean_html

# Pfade innerhalb des Plugin-Ordners
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "quiz_db.json"
STATE_PATH = BASE_DIR / "state.json"
QUIZ_TAB = "Aura-Quiz"

def show_current_question():
    with open(DB_PATH, "r") as f: db = json.load(f)
    with open(STATE_PATH, "r") as f: state = json.load(f)
    # Anzeige in CopyQ aktualisieren
    subprocess.run(["copyq", "tab", QUIZ_TAB, "remove", "0"], stderr=subprocess.DEVNULL)
    t= db[state["index"]]["display"]

    # t = re.sub(r'(\d+\))', ' \n \\1', t)
    # t = re.sub(r'(\d+\))', r' \n\n \1 ', t)
    # Richtig!
    # Falsch, nochmal!2026-0111-0449Falsch, nochmal!Der eintritt, ist freiRichtig!
    #Richtig!hirntod ist 3Die Antwort ist treiben die Antwort ist 2Falsch, nochmal!Tja und hat, ist ein
    #Falsch, nochmal!Falsch, nochmal!Richtig!
    # Die Antwort ist anUnd hat, ist einFalsch, nochmal!Falsch, nochmal!Der eintopf ist einRichtig!

    soup = BeautifulSoup(t, "html.parser")  # oder "lxml"
    cleaned = soup.get_text(strip=True)
    cleaned = re.sub(r'(\d+\))', r' \n\n \1 ', cleaned)
    # antwort bis 3Falsch, nochmal!Richtig!

    subprocess.run(["copyq", "tab", QUIZ_TAB, "add", cleaned], check=True)

    # Falsch, nochmal!Falsch, nochmal! tja und hat Richtig!ich 2die antwort ist 2 die antwort ist 1Falsch, nochmal!

    # t = clean_html(t)
    # subprocess.run(["copyq", "tab", QUIZ_TAB, "add", t])

# Antwort bis dahinRichtig!Richtig!Falsch, nochmal!irgendwas ist 3Falsch, nochmal!Richtig!

def update_display(text):
    """Löscht das Tab und schreibt die neue Frage rein."""
    subprocess.run(["copyq", "tab", QUIZ_TAB, "remove", "0"], stderr=subprocess.DEVNULL)

    text = clean_html(text)
    # Falsch, nochmal!Der Antrag ist beiFalsch, nochmal!Richtig!Richtig!
    subprocess.run(["copyq", "tab", QUIZ_TAB, "add", text], check=True)
    subprocess.run(["copyq", "show"])

def execute(match_data):
    spoken = match_data['regex_match_obj'].group(0).lower()
    if "start" in spoken:
        with open(STATE_PATH, "w") as f: json.dump({"index": 0}, f)
        show_current_question()
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
        show_current_question()
        # return " "
        return "Richtig!"
    # return " "
    return "Falsch, nochmal!"

#Richtig!

def execute_202601101708(match_data):
    # 1. Gesprochene Zahl holen (Gruppe 1 aus dem Regex ^(1|2|3)$)
    user_choice = int(match_data['regex_match_obj'].group(1))

    # 2. Datenbank und aktuellen Stand laden
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)

    state = {"index": 0}
    if STATE_PATH.exists():
        with open(STATE_PATH, "r") as f:
            state = json.load(f)

    current_idx = state["index"]
    correct_choice = db[current_idx]["correct"]

    # 3. Logik: Richtig oder Falsch?
    if user_choice == correct_choice:
        feedback = "Richtig!"
        # Nächsten Index berechnen (Loop am Ende)
        state["index"] = (current_idx + 1) % len(db)
        with open(STATE_PATH, "w") as f:
            json.dump(state, f)

        # Neue Frage anzeigen
        update_display(db[state["index"]]["display"])
    else:
        feedback = "Falsch, versuch es nochmal!"

    # 4. Feedback über Aura/Espeak ausgeben
    subprocess.run(["espeak", "-v", "de", feedback])
    return feedback

