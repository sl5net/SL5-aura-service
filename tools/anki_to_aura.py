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

# Richtig!Falsch, nochmal!

import html
import re


import re
import html


import re
import html

import html
import re

def clean_html(text):
    if not text:
        return ""

    # Richtig!Richtig!

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
            # HIER muss die Säuberung passieren:
            question = clean_html(fields[0])
            correct_answer = clean_html(fields[1])

            # Falsch, nochmal!Richtig!

            wrong_candidates = list(set([a for a in all_answers if a != correct_answer]))
            # Nimm max 2 falsche Antworten
            sampled_wrongs = random.sample(wrong_candidates, min(len(wrong_candidates), 2))

            options = [correct_answer] + sampled_wrongs
            random.shuffle(options)

            # Auffüllen, falls weniger als 3 Optionen vorhanden sind
            while len(options) < 3:
                options.append("---")

            quiz_data.append({
                "display": f"{question}\n\n1) {options[0]}\n2) {options[1]}\n3) {options[2]}",
                "correct": options.index(correct_answer) + 1
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

def generate_mc_rules(notes):
    rules = ["# Auto-generated Multiple Choice Quiz\nFUZZY_MAP_pre = ["]
    # all_answers = [n[0].split('\x1f')[1] for n in notes]
    all_answers = [clean_html(n[0].split('\x1f')[1]) for n in notes if len(n[0].split('\x1f')) >= 2]

    # Richtig!

    for i, note in enumerate(notes):
        fields = note[0].split('\x1f')
        question, correct_answer = fields[0], fields[1]

        # RICHTIGE ANTWORT FILTERN
        correct_answer_clean = clean_html(correct_answer)

        # FALSCHEN ANTWORTEN FILTERN IST SCHON OK
        wrong_answers = random.sample([a for a in all_answers if a != correct_answer_clean], 2)
        options = [correct_answer_clean] + wrong_answers
        random.shuffle(options)

        correct_index = options.index(correct_answer_clean) + 1

        display_text = f"{question}\\n\\n1) {options[0]}\\n2) {options[1]}\\n3) {options[2]}"

        # Trigger: Wenn der User die richtige Nummer sagt
        # Nutzt 'spoken_numbers_to_digits' Plugin Logik (eins -> 1)
        rules.append(f"    ('Richtig!', r'^{correct_index}$', 0, {{'on_match_exec': ['anki_next.py']}}),")

        subprocess.run(["copyq", "show"], check=True)


    rules.append("]")
    return rules



# Generiere die Aura-Regel (reagiert auf jede Zahl)
rules = [
    "from .anki_logic import check_answer\n",
    "FUZZY_MAP_pre = [",
    "    ('', r'^(1|2|3)$', 0, {'on_match_exec': [check_answer]}),",
    "]"
]


if __name__ == "__main__":
    extract_anki()

