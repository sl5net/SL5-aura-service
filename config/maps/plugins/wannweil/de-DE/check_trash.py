# config/maps/plugins/wannweil/de-DE/check_trash.py
# Version 13.0 - "The 12-Month-Silo-System"
import os
import pdfplumber
import datetime
import re
import sys
import subprocess
import threading
import csv

# --- KONFIGURATION (Exakt kalibriert auf Wannweil-Matrix) ---
LANG_CODE = "de-DE"
MAPPING = {
    0: 'Gelber Sack 🟡',
    1: 'Papiertonne 📄',
    2: 'Restmüll 🗑️',
    3: 'Biotonne 🍎',
    4: 'Problemstoffe ⚠️'
}


def espeak(text_to_speak, language_code):
    short_lang = language_code.split('-')[0]
    command = ['espeak', '-v', short_lang, text_to_speak]
    threading.Thread(target=lambda: subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL),
                     daemon=True).start()


def get_column_index(rel_x):
    """
    Ordnet den Abstand rel_x einer Spalte zu (0-4).
    Kalibrierung: ~5px=G, ~14px=P, ~23px=R, ~31px=B, ~39px=S
    """
    if rel_x < 10: return 0  # Gelber Sack
    if rel_x < 19: return 1  # Papiertonne
    if rel_x < 27: return 2  # Restmüll
    if rel_x < 35: return 3  # Biotonne
    return 4  # Problemstoffe


def parse_wannweil_silo_logic(pdf_path, debug=False):
    year_match = re.search(r'20\d{2}', pdf_path)
    pdf_year = int(year_match.group(0)) if year_match else 2026

    termine = []
    monate_namen = ["Januar", "Februar", "März", "April", "Mai", "Juni",
                    "Juli", "August", "September", "Oktober", "November", "Dezember"]

    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]  # Alles auf einer Seite
            # x_tolerance auf 2, damit Tag und x nicht verschmelzen
            words = page.extract_words(x_tolerance=2, y_tolerance=3)

            # 1. Die 12 Monats-Anker finden (X-Positionen)
            anchors = []
            for w in words:
                txt = w['text']
                rev_txt = txt[::-1]
                for i, m in enumerate(monate_namen):
                    if m.lower() in txt.lower() or m.lower() in rev_txt.lower():
                        anchors.append({'nr': i + 1, 'name': m, 'x0': w['x0']})

            # Nur die 12 echten Spaltenköpfe nehmen (die am weitesten oben stehen)
            anchors = sorted(anchors, key=lambda x: x['x0'])
            unique_anchors = []
            if anchors:
                unique_anchors.append(anchors[0])
                for a in anchors[1:]:
                    if a['x0'] - unique_anchors[-1]['x0'] > 40:  # Mindestmonatsbreite
                        unique_anchors.append(a)

            # Monatssilos definieren
            silos = []
            for i in range(len(unique_anchors)):
                a = unique_anchors[i]
                x_max = unique_anchors[i + 1]['x0'] - 5 if i < len(unique_anchors) - 1 else a['x0'] + 70
                silos.append({'nr': a['nr'], 'name': a['name'], 'x_min': a['x0'] - 15, 'x_max': x_max})

            if debug: print(f"DEBUG: {len(silos)} Monats-Silos erstellt.")

            # 2. Alle Tage und x-Markierungen
            all_days = [w for w in words if w['text'].isdigit() and 1 <= int(w['text']) <= 31]
            all_marks = [w for w in words if w['text'].lower() == 'x']

            # 3. Zuordnung innerhalb der Silos
            for silo in silos:
                # Nur Wörter und x-Markierungen in DIESEM Silo betrachten
                silo_days = [d for d in all_days if silo['x_min'] <= d['x0'] <= silo['x_max']]
                silo_marks = [m for m in all_marks if silo['x_min'] <= m['x0'] <= silo['x_max']]

                for mx in silo_marks:
                    # Finde den Tag im gleichen Silo auf der gleichen Höhe (Y)
                    best_day = next((dy for dy in silo_days if abs(mx['top'] - dy['top']) < 3), None)

                    if best_day:
                        tag_nr = int(best_day['text'])
                        rel_x = mx['x0'] - best_day['x1']

                        # Nur positive Abstände (x muss rechts vom Tag stehen)
                        if 2 < rel_x < 50:
                            col_idx = get_column_index(rel_x)
                            muell_name = MAPPING[col_idx]

                            try:
                                datum = datetime.date(pdf_year, silo['nr'], tag_nr)
                                termine.append({"datum": datum, "name": muell_name})
                                if debug:
                                    print(f"DEBUG: {tag_nr:02d}.{silo['nr']:02d} | rel_x: {rel_x:4.1f} -> {muell_name}")
                            except ValueError:
                                pass

    except Exception as e:
        print(f"Schwerer Parser-Fehler: {e}")

    # Gruppieren
    final_dict = {}
    for t in termine:
        d = t['datum']
        if d not in final_dict: final_dict[d] = []
        if t['name'] not in final_dict[d]: final_dict[d].append(t['name'])

    return [{"datum": d, "namen": sorted(final_dict[d])} for d in sorted(final_dict.keys())], pdf_year


def save_to_csv(termine, script_path):
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abfall_termine.csv")
    try:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(f"# {script_path}\n")
            writer = csv.writer(f)
            writer.writerow(["Datum", "Wochentag", "Abfallarten"])
            for t in termine:
                writer.writerow([t['datum'].strftime('%Y-%m-%d'), t['datum'].strftime('%a'), " & ".join(t['namen'])])
        print(f"CSV gespeichert: {csv_path} ({len(termine)} Einträge)")
    except Exception as e:
        print(f"CSV Fehler: {e}")


def check_and_notify(force_test=False):
    script_path = "config/maps/plugins/wannweil/de-DE/check_trash.py"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_files = [f for f in os.listdir(script_dir) if f.endswith('.pdf') and 'Abfall' in f]

    if not pdf_files: return
    pdf_path = os.path.join(script_dir, pdf_files[0])

    termine_data, pdf_year = parse_wannweil_silo_logic(pdf_path, debug=force_test)

    if termine_data:
        save_to_csv(termine_data, script_path)
    else:
        print("Keine Termine gefunden.")
        return

    heute = datetime.date.today()
    morgen = heute + datetime.timedelta(days=1)
    print(f"System-Check: Heute ist {heute.strftime('%d.%m.%Y')}.")

    for t in termine_data:
        if t['datum'] == morgen:
            inhalt = " & ".join(t['namen'])
            os.system(f'notify-send "MÜLL-ALARM" "Morgen: {inhalt}" --urgency=critical')
            espeak(f"Morgen wird der {inhalt} abgeholt", LANG_CODE)

    if force_test:
        zukunft = [t for t in termine_data if t['datum'] >= heute]
        if zukunft:
            n = zukunft[0]
            n1 = zukunft[1]
            msg = f"Nächste Abholung: {n['datum'].strftime('%d.%m.%Y')} ({' & '.join(n['namen'])}) "
            msg += f"Übernnächste Abholung: {n1['datum'].strftime('%d.%m.%Y')} ({' & '.join(n1['namen'])})"
            print(msg)
            espeak(msg, LANG_CODE)
            os.system(f'notify-send "MÜLL-VORSCHAU" "{msg}"')


if __name__ == "__main__":
    check_and_notify(force_test="test" in sys.argv)

