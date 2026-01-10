import sqlite3
import zipfile
import os
import shutil
from pathlib import Path
import random

APKG_FILE = "Python_Tresor_Basis.apkg"
OUTPUT_MAP = Path("config/maps/plugins/anki_quiz/de-DE/FUZZY_MAP_pre.py")
TEMP_DIR = Path("temp_anki")

def extract_anki():
    if not os.path.exists(APKG_FILE): return
    TEMP_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(APKG_FILE, 'r') as zip_ref:
        # Check if it's the old or new filename
        db_name = "collection.anki21" if "collection.anki21" in zip_ref.namelist() else "collection.anki2"
        zip_ref.extract(db_name, TEMP_DIR)

    conn = sqlite3.connect(TEMP_DIR / db_name)

    # conn = sqlite3.connect(TEMP_DIR / "collection.anki21")
    cursor = conn.cursor()

    # Get all notes (fields are separated by \x1f)
    cursor.execute("SELECT flds FROM notes")
    notes = cursor.fetchall()

    rules = ["# Auto-generated from Anki\nFUZZY_MAP_pre = ["]
    for note in notes:
        fields = note[0].split('\x1f')
        if len(fields) >= 2:
            question, answer = fields[0], fields[1]
            # Create a rule: if user says the answer, trigger 'Correct!' logic
            # For now, we map Answer -> Question as a simple check
            rules.append(f"    ('Richtig!', r'^{answer}$', 0, {{'on_match_exec': ['anki_next.py']}}),")

    rules.append("]")
    OUTPUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MAP.write_text("\n".join(rules), encoding="utf-8")

    conn.close()
    shutil.rmtree(TEMP_DIR)
    print(f"Aura-Map generiert: {OUTPUT_MAP}")

def generate_mc_rules(notes):
    rules = ["# Auto-generated Multiple Choice Quiz\nFUZZY_MAP_pre = ["]
    all_answers = [n[0].split('\x1f')[1] for n in notes]

    for i, note in enumerate(notes):
        fields = note[0].split('\x1f')
        question, correct_answer = fields[0], fields[1]

        # 2 falsche Antworten suchen
        wrong_answers = random.sample([a for a in all_answers if a != correct_answer], 2)
        options = [correct_answer] + wrong_answers
        random.shuffle(options)

        correct_index = options.index(correct_answer) + 1

        # In CopyQ anzuzeigender Text
        display_text = f"{question}\\n\\n1) {options[0]}\\n2) {options[1]}\\n3) {options[2]}"

        # Trigger: Wenn der User die richtige Nummer sagt
        # Nutzt 'spoken_numbers_to_digits' Plugin Logik (eins -> 1)
        rules.append(f"    ('Richtig!', r'^{correct_index}$', 0, {{'on_match_exec': ['anki_next.py']}}),")

    rules.append("]")
    return rules


quiz_data = []
for note in notes:
    # ... (Zufalls-Optionen generieren wie im letzten Schritt) ...
    display_text = f"{question}\n\n1) {options[0]}\n2) {options[1]}\n3) {options[2]}"
    quiz_data.append({
        "display": display_text,
        "correct": options.index(correct_answer) + 1
    })

# Speicher die Fragen als Datenbank für das Plugin
with open(OUTPUT_MAP.parent / "quiz_db.json", "w") as f:
    json.dump(quiz_data, f)

# Generiere die Aura-Regel (reagiert auf jede Zahl)
rules = [
    "from .anki_logic import check_answer\n",
    "FUZZY_MAP_pre = [",
    "    ('', r'^(1|2|3)$', 0, {'on_match_exec': [check_answer]}),",
    "]"
]


if __name__ == "__main__":
    extract_anki()

