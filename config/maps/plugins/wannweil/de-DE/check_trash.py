import os
import datetime
import re

import sys


import pdfplumber



# Testen:
"""
cd ~/projects/py/STT/config/maps/plugins/wannweil/de-DE/
~/projects/py/STT/.venv/bin/python3 check_trash.py test
"""

import subprocess
import threading

def espeak(text_to_speak, language_code):
    # Sprachcode bereinigen: espeak mag oft 'de' statt 'de-DE'
    # Wir nehmen nur die ersten zwei Buchstaben (z.B. 'de')
    short_lang = language_code.split('-')[0]

    # espeak-ng

    command = [
        'espeak-ng',
        '-v', short_lang,  # HIER war der Fehler: Hier muss die Sprache hin!
        text_to_speak      # Hier kommt der eigentliche Text hin
    ]

    def run_command():
        try:
            # shell=False ist Standard bei Liste, was gut gegen Injection ist
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print(f"Fehler: 'espeak' wurde nicht gefunden. Installiere es mit 'sudo pacman -S espeak'")
        except Exception as e:
            print(f"Espeak Fehler: {e}")

    thread = threading.Thread(target=run_command)
    thread.daemon = True
    thread.start()




def parse_abfall_pdf(pdf_path):
    termine = []
    # Monate auf Deutsch für das Parsing
    monate = ["Januar", "Februar", "März", "April", "Mai", "Juni",
              "Juli", "August", "September", "Oktober", "November", "Dezember"]

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')

            aktueller_monat = None
            for line in lines:
                # Prüfe, welcher Monat gerade bearbeitet wird
                for i, m in enumerate(monate):
                    if m in line:
                        aktueller_monat = i + 1

                # Suche nach Mustern wie "12 Di R" oder "05 Mi B, P"
                # Erläuterung: Tag (1-2 Stellen), Wochentag (2 Stellen), Abfall-Kürzel
                match = re.search(r'(\d{1,2})\s+[A-Z][a-z]\s+([R,B,P,G,\s]+)', line)

                if match and aktueller_monat:
                    tag = int(match.group(1))
                    typen_raw = match.group(2)

                    # Bereinige die Abfalltypen
                    typen = [t.strip() for t in typen_raw.replace(',', ' ').split()]

                    # Nur gültige Typen filtern
                    valid_types = [t for t in typen if t in ['R', 'B', 'P', 'G']]

                    if valid_types:
                        datum = datetime.date(2026, aktueller_monat, tag)
                        termine.append({"datum": datum, "typen": valid_types})
    return termine

def check_and_notify(force_test=False):
    # Ermittle den Ordner, in dem dieses Skript liegt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, "Abfallterminuebersicht-01-12-2026-1.pdf")

    # Prüfen, ob Datei existiert
    if not os.path.exists(pdf_path):
        print(f"Fehler: PDF nicht gefunden unter {pdf_path}")
        return

    termine = parse_abfall_pdf(pdf_path)

    morgen = datetime.date.today() + datetime.timedelta(days=1)

    mapping = {
        'R': 'Restmüll 🗑️',
        'B': 'Biotonne 🍎',
        'P': 'Papiertonne 📄',
        'G': 'Gelber Sack 🟡'
    }

    gefundene_termine = [t for t in termine if t['datum'] == morgen]

    if gefundene_termine:
        t = gefundene_termine[0]
        inhalt = " & ".join([mapping[typ] for typ in t['typen']])
        msg = f"Morgen wird abgeholt: {inhalt}"
        print(f"TERMIN GEFUNDEN: {msg}")
        os.system(f'notify-send "MÜLL-ALARM" "{msg}" --urgency=critical')
    elif force_test:
        test_msg = "Test erfolgreich! Das Skript läuft, aber morgen ist kein Mülltermin (2026er PDF!)."
        print(test_msg)
        espeak(f"{test_msg}", 'de-DE')
        os.system(f'notify-send "MÜLL-TEST" "{test_msg}"')

    else:
        print(f"Kein Termin für morgen ({morgen}) in der 2026-Liste gefunden.")



if __name__ == "__main__":
    # Wenn wir "test" als Argument übergeben, erzwingen wir eine Meldung
    is_test = "test" in sys.argv
    check_and_notify(force_test=is_test)

