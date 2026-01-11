# tools/anki_to_aura.py:1
import sqlite3
import zipfile
import os
import shutil
from pathlib import Path
import random
import json

# APKG_FILE = "Python_Tresor_Basis.apkg"
APKG_FILE = Path("config/maps/plugins/anki_quiz/Python_fundamentals.apkg")
OUTPUT_MAP = Path("config/maps/plugins/anki_quiz/de-DE/FUZZY_MAP_pre.py")
TEMP_DIR = Path("temp_anki")


BASE_DIR = OUTPUT_MAP.parent
LOG_FILE = BASE_DIR / "QuizProtokoll.md"
# UNICODE_NUMS = {1: "⓵", 2: "⓶", 3: "⓷"}

UNICODE_NUMS = {1: "1️", 2: "2️", 3: "3️"}



LOG_FILE = BASE_DIR / "QuizProtokoll.md"

import html
import re

def strip_existing_numbering_OFF(text):
    # Entfernt Muster wie "1)", "1.", "(1)", "a)" am Zeilenanfang
    return re.sub(r'^\s*[\(\[0-9a-z]\s*[\)\.]\s*', '', text, flags=re.IGNORECASE).strip()

def clean_html(text):
    if not text:
        return ""

    text = clean_html_old(text)
    text = clean_html2(text)
    text = clean_html4(text)
    # Erst kodierte Zeichen (Entitäten) decodieren!
    text = html.unescape(text)
    # Dann wirklich ALLE Tags (<...>) rausschneiden
    text = re.sub(r'<.*?>', '', text)
    # Mehrfach-Leerzeichen und Umbrüche bereinigen
    return ' '.join(text.split()).strip()

def clean_html4(text):
    if not text:
        return ""
    # HTML-Entities zuerst umwandeln (so bleibt das meiste Klartext)
    text = html.unescape(text)
    # ALLE HTML-Tags restlos entfernen (auch mehrere hintereinander, div/pre/code etc.)
    text = re.sub(r'<.*?>', ' ', text)
    # Leerzeichen normalisieren
    return ' '.join(text.split()).strip()

# Falsch, nochmal! ist 2 Richtig!Falsch, nochmal!Richtig!
#Falsch, nochmal!Richtig!Die Antwort ist freiDie Antwort ist frei
# <pre><code class="lang-python">t = 'AaBbCcDd'
# print(t[::2])
# print(t[1::2])</code></pre>
#
# 1) <pre><code class="lang-python">print("N{thumbs up sign}")</code></pre>
# 2) <div>ABCD</div><div>abcd</div>
# 3) <b>sys.argv</b>


def clean_html2(text):
    if not text:
        return ""
    # 1. HTML-Entities (&lt;, &gt;, &quot;) in echte Zeichen umwandeln
    text = html.unescape(text)
    # 2. Alle HTML-Tags entfernen (<...>)
    text = re.sub(r'<[^>]+>', ' ', text)
    # 3. Überflüssige Leerzeichen und Zeilenumbrüche trimmen
    return ' '.join(text.split()).strip()


    # Scheint war düster 1Falsch, nochmal!Richtig!<pre><code class="lang-python">text = "abababab"
    # i = text.count("abab")
    # print(i)</code></pre>
    #
    # 1) <div>ABCD</div><div>abcd</div>
    # 2) 2
    # 3) <pre><code class="lang-python">from functools import lru_cache
    #
    # @lru_cache
    # def costly_function(x, y, z):
    #     "May be invoked millions of times with different args."
    #     pass</code></pre>


def clean_html_old(text):
    if not text: return ""
    # 1. HTML-Entities (&lt;, &gt;, &quot;) in echte Zeichen umwandeln
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'<.*?>', ' ', text, flags=re.DOTALL)
    text = html.unescape(text)
    # 2. Alle Tags (wie <pre>, <b>, <code>) restlos entfernen
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'<.*?>', ' ', text, flags=re.DOTALL)
    # 3. Überflüssige Leerzeichen und Zeilenumbrüche trimmen
    return text.strip()
#Richtig!Richtig!

def extract_anki():
    if not os.path.exists(APKG_FILE): return
    TEMP_DIR.mkdir(exist_ok=True)
    with zipfile.ZipFile(APKG_FILE, 'r') as zip_ref:
        db_name = "collection.anki21" if "collection.anki21" in zip_ref.namelist() else "collection.anki2"
        zip_ref.extract(db_name, TEMP_DIR)

    conn = sqlite3.connect(TEMP_DIR / db_name)
    notes = conn.execute("SELECT flds FROM notes").fetchall()

    # Alle Antworten sammeln für die Zufallsauswahl falscher Optionen
    # all_answers = [n[0].split('\x1f')[1] for n in notes if len(n[0].split('\x1f')) >= 2]
    all_answers = [clean_html(n[0].split('\x1f')[1]) for n in notes if len(n[0].split('\x1f')) >= 2]

    quiz_data = []

    # Innerhalb der Schleife in extract_anki:
    for note in notes:
        fields = note[0].split('\x1f')
        if len(fields) >= 2:
            question = clean_html(fields[0])
            correct_ans = clean_html(fields[1])

            # Filter: Falsche Antworten säubern und Dubletten vermeiden
            wrong_candidates = list(set([a for a in all_answers if a != correct_ans]))
            options = [correct_ans] + random.sample(wrong_candidates, min(len(wrong_candidates), 2))
            random.shuffle(options)
            while len(options) < 3: options.append("---")

            # Index der richtigen Antwort finden (für das Quiz-Plugin)
            correct_idx = options.index(correct_ans) + 1

            # --- Unicode Anzeige-Logik ---
            display_text = f"{question}\n\n"
            for i, opt in enumerate(options, 1):  # <--- WICHTIG: Start bei 1
                symbol = UNICODE_NUMS.get(i, f"XXXX {i})")
                display_text += f"YYYY {symbol} {opt}\n"

            quiz_data.append({
                "display": display_text,
                "correct": correct_idx
            })




    # Dateien schreiben
    with open(OUTPUT_MAP.parent / "quiz_db.json", "w", encoding="utf-8") as f:
        json.dump(quiz_data, f)

    # rules = [
    #     "from .anki_logic import execute\n",
    #     "FUZZY_MAP_pre = [",
    #     "    ('', r'^(1|2|3)$', 0, {'on_match_exec': [execute]}),",
    #     "]"
    # ]
    OUTPUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    # OUTPUT_MAP.write_text("\n".join(rules), encoding="utf-8")

    conn.close()
    shutil.rmtree(TEMP_DIR)
    print(f"Aura-Quiz bereit: {len(quiz_data)} Fragen in {OUTPUT_MAP.parent}")

# Generiere die Aura-Regel (reagiert auf jede Zahl)
rules = [
    "from .anki_logic import check_answer\n",
    "FUZZY_MAP_pre = [",
    "    ('', r'^(1|2|3)$', 0, {'on_match_exec': [check_answer]}),",
    "]"
]


if __name__ == "__main__":
    extract_anki()

