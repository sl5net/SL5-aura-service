import sqlite3
import zipfile
import os
import shutil
from pathlib import Path

APKG_FILE = "Python_Tresor_Basis.apkg"
OUTPUT_MAP = Path("config/maps/plugins/anki_quiz/de-DE/FUZZY_MAP_pre.py")
TEMP_DIR = Path("temp_anki")

def extract_anki():
    if not os.path.exists(APKG_FILE): return
    TEMP_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(APKG_FILE, 'r') as zip_ref:
        zip_ref.extract("collection.anki21", TEMP_DIR) # Newer Anki format

    conn = sqlite3.connect(TEMP_DIR / "collection.anki21")
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
            rules.append(f"    ('{question}', r'^{answer}$'),")

    rules.append("]")
    OUTPUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MAP.write_text("\n".join(rules), encoding="utf-8")

    conn.close()
    shutil.rmtree(TEMP_DIR)
    print(f"Aura-Map generiert: {OUTPUT_MAP}")

if __name__ == "__main__":
    extract_anki()
