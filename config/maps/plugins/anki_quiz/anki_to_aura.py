import sqlite3
import zipfile
#import os
import shutil
from pathlib import Path
import random
import json
# import re
from bs4 import BeautifulSoup

UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}


# PADE ANPASSEN falls nötig
# Wir suchen die APKG Datei im Plugin Ordner oder relativ
BASE_DIR = Path(__file__).parent
PLUGIN_DIR = Path("config/maps/plugins/anki_quiz")
PLUGIN_DIR = Path("./")
# Falls wir im 'tools' ordner sind, müssen wir hoch
if not PLUGIN_DIR.exists():
    PLUGIN_DIR = Path("../config/maps/plugins/anki_quiz")

APKG_FILE = PLUGIN_DIR / "Python_fundamentals.apkg"
DB_OUTPUT = PLUGIN_DIR / "de-DE/quiz_db.json"
TEMP_DIR = Path("temp_anki_extract")

def clean_html(text):
    if not text: return ""

    # 1. HTML parsen
    soup = BeautifulSoup(text, "html.parser")

    # 2. Text extrahieren (Tags wie <br> werden zu Newlines)
    text = soup.get_text(separator="\n", strip=True)

    # 3. WICHTIG: Alles entfernen, was kein druckbares Zeichen ist (außer Newline)
    # Entfernt Backspaces, Null-Bytes, etc., die JSON zerstören könnten.
    # Wir erlauben auch Tabs (\t).
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")

    return text

def extract_anki():
    print(f"Suche Anki-Datei: {APKG_FILE.resolve()}")
    if not APKG_FILE.exists():
        print("FEHLER: .apkg Datei nicht gefunden!")
        return

    # Alte DB löschen, um Mix-Ups zu verhindern
    if DB_OUTPUT.exists():
        print("Lösche alte Datenbank...")
        DB_OUTPUT.unlink()

    # Entpacken
    if TEMP_DIR.exists(): shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(exist_ok=True)

    with zipfile.ZipFile(APKG_FILE, 'r') as zip_ref:
        # Anki Datenbank finden (anki2 oder anki21)
        db_name = "collection.anki21" if "collection.anki21" in zip_ref.namelist() else "collection.anki2"
        zip_ref.extract(db_name, TEMP_DIR)

    conn = sqlite3.connect(TEMP_DIR / db_name)
    notes = conn.execute("SELECT flds FROM notes").fetchall()

    print(f"Gefundene Notizen: {len(notes)}")

    # Alle Antworten sammeln (für falsche Optionen)
    all_answers = []
    valid_notes = []

    for note in notes:
        fields = note[0].split('\x1f')
        if len(fields) >= 2:
            ans = clean_html(fields[1])
            if ans: # Nur nicht-leere Antworten nehmen
                all_answers.append(ans)
                valid_notes.append(fields)

    quiz_data = []

    for fields in valid_notes:
        question = clean_html(fields[0])
        correct_ans = clean_html(fields[1])

        # Falls durch das Cleaning die Frage leer wurde, überspringen
        if not question or not correct_ans:
            continue

        # Falsche Antworten finden (die nicht gleich der richtigen sind)
        wrong_candidates = list(set([a for a in all_answers if a != correct_ans]))

        # Wenn wir nicht genug falsche Antworten haben, nimm Platzhalter
        sample_size = min(len(wrong_candidates), 2)
        if sample_size > 0:
            options = [correct_ans] + random.sample(wrong_candidates, sample_size)
        else:
            options = [correct_ans, "Keine Ahnung", "42"]

        random.shuffle(options)

        # Auf 3 auffüllen falls nötig
        while len(options) < 3:
            options.append("---")

        # Index der richtigen Antwort finden (1-basiert)
        try:
            correct_idx = options.index(correct_ans) + 1
        except ValueError:
            # Sollte nicht passieren, aber sicher ist sicher
            print(f"WARNUNG: Richtige Antwort '{correct_ans}' ging beim Shuffle verloren?")
            continue

        # Anzeige bauen
        display_text = f"{question}\n\n"
        for i, opt in enumerate(options, 1):
            display_text += f"{i}) {opt}\n"

        quiz_data.append({
            "display": display_text,
            "correct": correct_idx
        })

    # JSON Schreiben (Mit indent=2 für Lesbarkeit und Debugging)
    print(f"Schreibe {len(quiz_data)} Fragen nach: {DB_OUTPUT}")
    DB_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    try:
        with open(DB_OUTPUT, "w", encoding="utf-8") as f:
            json.dump(quiz_data, f, indent=2, ensure_ascii=False)
        print("Erfolg! Datenbank neu erstellt.")
    except Exception as e:
        print(f"FEHLER beim Schreiben der JSON: {e}")

    conn.close()
    shutil.rmtree(TEMP_DIR)

if __name__ == "__main__":
    extract_anki()
