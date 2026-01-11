import sqlite3
import zipfile
from pathlib import Path
import os

TEMP_DIR = Path("temp_debug")


# Versuch, die Datei relativ zum Skript oder zum Arbeitsverzeichnis zu finden
# analyze_anki.py:10
POSSIBLE_PATHS = [
    Path("config/maps/plugins/anki_quiz/Python_fundamentals.apkg"),
    Path("../config/maps/plugins/anki_quiz/Python_fundamentals.apkg"),
    Path("Python_fundamentals.apkg"), # Falls sie direkt da liegt
]

APKG_FILE = None
for p in POSSIBLE_PATHS:
    if p.exists():
        APKG_FILE = p
        break

if not APKG_FILE:
    print(f"Fehler: .apkg Datei nicht gefunden in: {[str(p) for p in POSSIBLE_PATHS]}")
    # Hier brichst du ab oder suchst manuell
else:
    print(f"Datei gefunden: {APKG_FILE}")



#  find . -name "Python_fundamentals.apkg"                                                                                                               INT ✘  11s 
# ./config/maps/plugins/anki_quiz/Python_fundamentals.apkg

def analyze():
    if not os.path.exists(APKG_FILE):
        print("Datei nicht gefunden!")
        return

    TEMP_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(APKG_FILE, 'r') as zip_ref:
        db_name = "collection.anki21" if "collection.anki21" in zip_ref.namelist() else "collection.anki2"
        zip_ref.extract(db_name, TEMP_DIR)

    conn = sqlite3.connect(TEMP_DIR / db_name)

    # Wir holen uns ein paar Beispiele
    notes = conn.execute("SELECT flds FROM notes LIMIT 20").fetchall()
    notes = conn.execute("SELECT flds FROM notes").fetchall() # KEIN LIMIT!

    print(f"\n--- ANALYSE DER ERSTEN 20 KARTEN ---\n")

    found = False
    for i, note in enumerate(notes):
        if "abcabcabc" in note[0]:
            fields = note[0].split('\x1f')
            print(f"\n--- PROBLEM-KARTE GEFUNDEN (Index {i}) ---")
            print(f"ANZAHL FELDER: {len(fields)}")
            print(f"FELD 0 (Frage?):   {fields[0]}")
            print(f"FELD 1 (Antwort?): {fields[1]}")
            if len(fields) > 2:
                print(f"FELD 2 (Extra?):   {fields[2]}")
            found = True
            break

    if not found:
            print("Karte mit 'abcabcabc' nicht gefunden!")


    conn.close()
    # Aufräumen (optional)
    # import shutil
    # shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    analyze()

