# config/maps/plugins/wannweil/de-DE/check_trash.py

# ./.venv/bin/python3 config/maps/plugins/wannweil/de-DE/check_trash.py
#  ./.venv/bin/python3 config/maps/plugins/wannweil/de-DE/check_trash.py
# or use:
#     ~/pr/py/STT    master *1 !2 ?1  python.sh ./config/maps/plugins/wannweil/de-DE/check_trash.py &


import sys
import os
import unicodedata
import pdfplumber
import datetime  # Nur das Modul importieren
import re
import subprocess
import csv
import smtplib
import hashlib

from email.message import EmailMessage
from dotenv import load_dotenv



# --- E-MAIL KONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465


# Ermittle den Ordner, in dem dieses Skript liegt
script_dir = os.path.dirname(os.path.abspath(__file__))
# Suche die .env Datei genau in diesem Ordner
env_path = os.path.join(script_dir, '.env')

# Lade die Datei, falls sie existiert
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    print(f"Hinweis: Keine .env Datei in {script_dir} gefunden.")

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

RECEIVER_EMAIL = "sl5softwarelab@gmail.com" # Wo die Mail hin soll

def sanitize_to_ascii(s: str, maxlen: int = None) -> str:
    """
    - Unicode normalisieren (NFKD), diakritische Zeichen trennen
    - Non-ASCII entfernen (oder ersetzen)
    - Steuerzeichen außer \t,\n,\r entfernen
    - Optional kürzen
    """
    if s is None:
        return ''
    # 1) Normalize (separate accents)
    s = unicodedata.normalize('NFKD', s)
    # 2) Remove combining marks (keeps base ascii letters)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    # 3) Replace common unicode dashes/quotes with ascii equivalents
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u00A0': ' '
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    # 4) Remove NULs and other non-printable controls (allow tab, lf, cr)
    s = s.replace('\x00', '')
    s = re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', s)
    # 5) Collapse whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    # 6) Optional truncate
    if maxlen and len(s) > maxlen:
        s = s[:maxlen-3].rstrip() + '...'
    return s

def send_mail_notification(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)
        print("E-Mail erfolgreich gesendet.")
    except Exception as e:
        print(f"E-Mail Fehler: {e}")















# --- KONFIGURATION ---
LANG_CODE = "de-DE"
MAPPING = {
    0: 'Gelber Sack 🟡',
    1: 'Papiertonne 📄',
    2: 'Restmüll 🗑️',
    3: 'Biotonne 🍎',
    4: 'Problemstoffe ⚠️'
}

# Liste für deutsche Wochentage (0 = Montag, 6 = Sonntag)
WOCHENTAGE_DE = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]


def espeak(text_to_speak, language_code):
    # return True


    short_lang = language_code.split('-')[0]
    command = ['espeak', '-v', short_lang, text_to_speak]
    try:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Espeak Fehler: {e}")


def get_column_index(rel_x):
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
            page = pdf.pages[0]
            words = page.extract_words(x_tolerance=2, y_tolerance=3)

            anchors = []
            for w in words:
                txt = w['text']
                rev_txt = txt[::-1]
                for i, m in enumerate(monate_namen):
                    if m.lower() in txt.lower() or m.lower() in rev_txt.lower():
                        anchors.append({'nr': i + 1, 'name': m, 'x0': w['x0']})

            anchors = sorted(anchors, key=lambda x: x['x0'])
            unique_anchors = []
            if anchors:
                unique_anchors.append(anchors[0])
                for a in anchors[1:]:
                    if a['x0'] - unique_anchors[-1]['x0'] > 40:
                        unique_anchors.append(a)

            silos = []
            for i in range(len(unique_anchors)):
                a = unique_anchors[i]
                x_max = unique_anchors[i + 1]['x0'] - 5 if i < len(unique_anchors) - 1 else a['x0'] + 70
                silos.append({'nr': a['nr'], 'name': a['name'], 'x_min': a['x0'] - 15, 'x_max': x_max})

            all_days = [w for w in words if w['text'].isdigit() and 1 <= int(w['text']) <= 31]
            all_marks = [w for w in words if w['text'].lower() == 'x']

            for silo in silos:
                silo_days = [d for d in all_days if silo['x_min'] <= d['x0'] <= silo['x_max']]
                silo_marks = [m for m in all_marks if silo['x_min'] <= m['x0'] <= silo['x_max']]

                for mx in silo_marks:
                    best_day = next((dy for dy in silo_days if abs(mx['top'] - dy['top']) < 3), None)

                    if best_day:
                        tag_nr = int(best_day['text'])
                        rel_x = mx['x0'] - best_day['x1']

                        if 2 < rel_x < 50:
                            col_idx = get_column_index(rel_x)
                            muell_name = MAPPING[col_idx]

                            if col_idx == 0:

                                tag_nr = muell_name = ''# 'Gelber Sack 🟡' FIX ... becouse i personally dont need the Ifor for the 'Gelber Sack 🟡' 13.2.'26 11:18 Fri
                                #   0: 'Gelber Sack 🟡',
                                continue


                            try:
                                datum = datetime.date(pdf_year, silo['nr'], tag_nr)
                                # Die fehlerhaften tag_name Zeilen wurden hier entfernt
                                termine.append({"datum": datum, "name": muell_name})
                                # if debug:
                                #     print(f"DEBUG: {tag_nr:02d}.{silo['nr']:02d} | rel_x: {rel_x:4.1f} -> {muell_name}")
                            except ValueError:
                                pass
    except Exception as e:
        print(f"Schwerer Parser-Fehler: {e}")

    final_dict = {}
    for t in termine:
        d = t['datum']
        if d not in final_dict: final_dict[d] = []
        if t['name'] not in final_dict[d]: final_dict[d].append(t['name'])

    return [{"datum": d, "namen": sorted(final_dict[d])} for d in sorted(final_dict.keys())], pdf_year


def save_to_csv(termine, script_path, pdf_path):
    print(f"csv NOT SAVED becouse i dont need save it alowas. save it in Januar is enought then it usually works for the year. 13.2.'26 11:13 Fri")
    print(f"csv NOT SAVED becouse i dont need save it alowas. save it in Januar is enought then it usually works for the year. 13.2.'26 11:13 Fri")
    print(f"csv NOT SAVED becouse i dont need save it alowas. save it in Januar is enought then it usually works for the year. 13.2.'26 11:13 Fri")
    print(f"csv NOT SAVED becouse i dont need save it alowas. save it in Januar is enought then it usually works for the year. 13.2.'26 11:13 Fri")


    return True







    # print(f"{pdf_path} -----------------------------------------")
    # csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "abfall_termine.csv")
    csv_path = f"{pdf_path}.csv"

    try:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write(f"# {script_path}\n")
            writer = csv.writer(f)
            writer.writerow(["Datum", "Wochentag", "Abfallarten"])
            for t in termine:
                # Hier holen wir den deutschen Namen über den Index (datum.weekday())
                wochentag_de = WOCHENTAGE_DE[t['datum'].weekday()]
                writer.writerow([t['datum'].strftime('%Y-%m-%d'), wochentag_de, " & ".join(t['namen'])])
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
        save_to_csv(termine_data, script_path, pdf_path)
    else:
        print("Keine Termine gefunden.")
        return

    heute = datetime.date.today()
    morgen = heute + datetime.timedelta(days=1)


    # Debug Info für Terminal
    # if force_test:
    #     print(f"System-Check: Heute ist {heute.strftime('%d.%m.%Y')}.")

    check_csv_alerts()

    for t in termine_data:
        if t['datum'] == morgen:
            inhalt = " & ".join(t['namen'])
            os.system(f'notify-send "MÜLL-ALARM" "Morgen: {inhalt}" --urgency=critical')
            espeak(f"Morgen wird der {inhalt} abgeholt", LANG_CODE)


    # sys.exit(0)


    if force_test:
        zukunft = [t for t in termine_data if t['datum'] >= heute]
        if zukunft:
            n = zukunft[0]
            tag_name = WOCHENTAGE_DE[n['datum'].weekday()]
            # msg = f"Nächste Abholung: {n['datum'].strftime('%d.%m.%Y')} ({' & '.join(n['namen'])})"
            # datum_formatiert = n['datum'].strftime('%-d.%-m.%Y ')
            d = n['datum']
            datum_formatiert = n['datum'].strftime(f"{d.day}.{d.month}.{d.year}") # Für Windows und Linux geeignet
            datum_formatiert_espeak = n['datum'].strftime(f"{d.day}.{d.month}.") # Für Windows und Linux geeignet
            msg = f"{tag_name}, {datum_formatiert} ({' & '.join(n['namen'])}) | Nächste Abholung | MÜLL-VORSCHAU |"
            msg_espeak = f"{tag_name}, {datum_formatiert_espeak} ({' & '.join(n['namen'])}) | {tag_name}, ({' & '.join(n['namen'])}) "
            msg_espeak_ohne_emojis = re.sub(r'[^\w\s.,!-]', '', msg_espeak).strip()


            print(msg)
            os.system(f'notify-send "MÜLL-VORSCHAU" "{msg}"')

            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            # VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
            espeak(msg_espeak_ohne_emojis, LANG_CODE)

            # send_mail_notification(msg, msg)

# wannweil/de-DE/_alerts/
def check_csv_alerts():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "_alerts/alerts.csv")
    if not os.path.exists(csv_file):
        print(f"CSV Fehler: {csv_file}.")
        return

    print(f"check_trash.py:256")

    # now = datetime.datetime.now()
    # now = datetime.now()

    yad_row = 0

    with (open(csv_file, 'r', encoding='utf-8') as f):
        reader = csv.DictReader(f)
        for row in reader:
            print(row)

            try:
                # Nutze hier datetime.datetime.strptime

                now = datetime.datetime.now()


                # 1. Daten auslesen & Wildcards prüfen
                # ---------------------------------------------------------
                start_str = row.get('Start', '').strip()
                end_str = row.get('End', '').strip()
                modes = row.get('Modes', '').strip()
                msg = row.get('Message', '').replace('"', '\\"')  # Anführungszeichen escapen

                # Definition: Was gilt als "leeres" Datum? (Wildcard)
                wildcards = ['', '_', '-']
                is_start_always = start_str in wildcards
                is_end_forever = end_str in wildcards

                if not is_start_always:
                    start = datetime.datetime.strptime(row['Start'].strip(), "%Y-%m-%d %H:%M")

                if not is_end_forever:
                    end = datetime.datetime.strptime(row['End'].strip(), "%Y-%m-%d %H:%M")

                tolerance = datetime.timedelta(hours=5)
                print('check_trash.py:274')
                if (is_start_always and is_end_forever ) or (is_start_always and now <= end + tolerance) or (start - tolerance <= now and is_end_forever) or (start - tolerance <= now <= end + tolerance) :
                    print(' innerhalb des tolerierten Zeitfensters')


                    # if start <= now <= end:
                    # msg = f"{row['Start'].strip()} {row['Message'].strip()}"

                    # msg = msg.replace('"', '\\"')

                    if 'P' in modes:
                        if '📍' in modes or '📌' in modes :
                            if '📍' in modes:
                                msg_yad_save = sanitize_to_ascii(msg)
                                yad_row += 1
                                yad_y_offset = 150
                                yad_y_pos = yad_row * yad_y_offset
                                timeout = 60*15
                                cmd = f'yad --text="{msg_yad_save}" --geometry=300x100+2000+{int(yad_y_pos-yad_y_offset/2)} --no-buttons --undecorated --sticky --on-top --timeout={timeout} &'
                                os.system(cmd)
                                #     geom = f'{width}x{height}+{geom_x}+{y}'
                                # Set dialog timeout in seconds.

                            if '📌' in modes:
                                # critical stays for ever
                                # os.system(f'notify-send "AURA ALERT" "{msg}" --urgency=critical')
                                hash_object = hashlib.md5(msg.encode())
                                notif_id = int(hash_object.hexdigest(), 16) % 1000000
                                os.system(f'notify-send "{msg} |{modes}" -r {notif_id} --urgency=critical -t 0')

                        else:
                            # os.system(f'notify-send "{msg} |{modes}" --urgency=critical -t 5000')
                            os.system(f'notify-send "{msg} |{modes}" --urgency=normal')

                    if 'V' in modes:
                        # Hier säubern wir nur die Sprachausgabe (Emojis weg)

                        msg = f"{row['Message'].strip()}"

                        clean_voice = re.sub(r'[^\w\s.,!-]', '', msg)
                        espeak(clean_voice, LANG_CODE)
                    if 'M' in modes:
                        send_mail_notification(f"Alert: {msg}", msg)  # Mail darf Emojis behalten
            except Exception as e:
                m = f"Fehler beim Parsen einer Alert-Zeile: {e}"
                print(m)
                espeak(m, LANG_CODE)





if __name__ == "__main__":
    if 0:
        check_and_notify(force_test="test" in sys.argv)
    else:
        print("nix 16.2.'26 Mon")
        print("nix 16.2.'26 Mon")
        print("nix 16.2.'26 Mon")
        print("nix 16.2.'26 Mon")
        print("nix 16.2.'26 Mon")
