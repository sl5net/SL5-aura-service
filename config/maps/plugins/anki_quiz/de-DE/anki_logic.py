#
import json
import subprocess
from pathlib import Path

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
    subprocess.run(["copyq", "tab", QUIZ_TAB, "add", db[state["index"]]["display"]])

def update_display(text):
    """Löscht das Tab und schreibt die neue Frage rein."""
    subprocess.run(["copyq", "tab", QUIZ_TAB, "remove", "0"], stderr=subprocess.DEVNULL)
    subprocess.run(["copyq", "tab", QUIZ_TAB, "add", text], check=True)
    subprocess.run(["copyq", "show"], check=True)

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
        return "Richtig!"
    return "Falsch, nochmal!"



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

