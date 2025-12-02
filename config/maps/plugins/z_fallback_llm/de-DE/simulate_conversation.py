import sys
import os
import subprocess, psutil
import time, datetime

from pygments.lexer import include

#import re
#import sys
#from pathlib import Path
#import subprocess

from . import utils



from . health_checks import check_db_statistics_and_exit_if_invalid, check_db_statistics_and_exit_if_invalid


# --- KONFIGURATION ---
ROUNDS = 900  # Wie oft sollen sie hin und her reden?

# https://ollama.com/download


# Sicherstellen, dass wir ask_ollama finden
# try:
#     sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#     import ask_ollama
# except ImportError:
#     print("❌ FEHLER: Konnte 'ask_ollama.py' nicht importieren.")
#     sys.exit(1)



# simulate_conversation.py
from . import ask_ollama


# --- MOCK OBJEKT (Damit Aura denkt, es kommt vom Mikrofon) ---
class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        # return ("Computer", self.text)
        return ("Aura", self.text)
    def group(self, index):
        if index == 2: return self.text
        # return "Computer"
        return "Aura"

# --- BOT A: DER USER (Ollama 1) ---
def generate_user_question(last_aura_response, round_num):
    """
    Dieser Bot simuliert den User. Er reagiert auf Auras Antwort.
    """
    # print(f"\n🤔 User-Bot überlegt (Runde {round_num})...")

    system_prompt_Ergotherapeut = ( # noqa: F841
        "Du bist ein User, Ergotherapeut mit Schwehrbehinderten, der sehr selten Computer benutz und das neue Open-Source assistant framework testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! \n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    system_prompt_kritischer = ( # noqa: F841
        "Du bist ein neugieriger, kritischer User, der einen neuen Open-Source Sprachassistenten testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, knackige Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! Frag nach Details, Installation, Witzen oder technischen Grenzen.\n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    system_prompt_LinuxAdministrator1 = ( # noqa: F841
        "Du bist ein Linux-User, der Aura, den Offline Voice Assistant STT to Commands or Text, Pluggable System testet.\n"
        "REGELN:\n"
        "Aura ist Headless / CLI. Keine GUI. Keine Maus für alle OS (z.B. Linux, Windows, Mac).\n"
        "Alle REGELN müssen sich in config/maps/ befinden.\n"
        "1. Stelle EINE kurze, knackige Frage.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! Schreib nur den Satz, keine Anführungszeichen.\n"
    )
    system_prompt_LinuxMusikerin = ( # noqa: F841
        "Du bist ein kritische, kreative Jornalist, die Aura, den Offline Voice Assistant STT to Commands or Text, Pluggable System testet.\n"
        "Dich interessieren Beispiel oder einfache Regeln:\n"
        "Aura ist Headless / CLI. Keine GUI. Keine Maus für alle OS (z.B. Linux, Windows, Mac).\n"
        "Alle REGELN müssen sich in config/maps/ befinden.\n"
        "1. Stelle EINE kurze, knackige Frage.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    system_prompt_LinuxAdministrator = ( # noqa: F841
        "Du bist ein strenger Linux-Admin, der den Voice-Assistant 'SL5 Aura' konfiguriert.\n"
        "Dein Ziel: Prüfen, ob der Bot die Dateipfade und Regex-Syntax kennt.\n"
        "Kontext: Aura ist headless, nutzt '/tmp/sl5_record.trigger' und Configs in 'config/maps/'.\n\n"

        "REGELN FÜR DICH:\n"
        "1. Stelle Fragen zur Konfiguration, zu Dateipfaden oder Regex-Regeln.\n"
        "2. Frage NICHT nach allgemeinem Linux-Wissen (wie 'Was ist systemd').\n"
        "3. Beginne IMMER mit 'Aura, '.\n"
        "4. Sei kurz und fordernd.\n\n"

        "BEISPIEL-FRAGEN (Variiere diese):\n"
        "- Aura, wo muss ich meine neuen Regeln speichern?\n"
        "- Aura, erstelle eine Regel, die auf 'Computer herunterfahren' reagiert.\n"
        "- Aura, wie lautet der Befehl, um die Aufnahme manuell auszulösen?\n"
        "- Aura, schreibe einen Regex, der 'Licht an' oder 'Licht aus' erkennt.\n"
        "- Aura, welche Datei muss ich anlegen, damit du zuhörst?"
    )


    system_prompt = system_prompt_LinuxMusikerin

    # Kontext geben: Was hat Aura gerade gesagt?
    context_prompt = f"{system_prompt}\n\nLETZTE ANTWORT DES ASSISTENTEN:\n\"{last_aura_response}\"\n\nDEINE NÄCHSTE FRAGE:"

    # cmd = ["ollama", "run", "llama3.2"]
    cmd = ["ollama", "run", "llama3.2"]
    result = subprocess.run(cmd, input=context_prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        return None

    # Bereinigen (Manchmal ist Llama geschwätzig)
    question = result.stdout.strip().replace('"', '')

    question = question.replace('trigger-Ordner','trigger ')


    # /tmp/sl5_record.trigger-Ordner

    question = question.replace('JSON','Python')
    question = question.replace('YAML','Python')
    question = question.replace('json','Python')
    question = question.replace('.Python','.py')
    question = question.replace('Aurah ','Aura ')
    question = question.replace('Aurawhen','Aura ')
    question = question.replace('config/maps/Ordner','config/maps Ordner')

    question = question.replace('Format `.config`','Format `.py`')
    question = question.replace('.config',' config/ ')
    speak_espeak(question)

    # Sicherstellen, dass "Computer" am Anfang steht (falls Llama es vergisst)
    if not question.lower().startswith("aura"):
        question = "Aura, " + question

    return question



def speak_espeak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)

    #     h = os.environ.get("HOME", "/tmp")  # $HOME Variable
    #     f = "/tmp/sl5_aura/simulate_conversation.txt"
    #     process = subprocess.run(['python', speak_file_path, f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")

def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        # subprocess.run(['espeak', '-v', 'de', text], check=True)

        h = os.environ.get("HOME", "/tmp")  # $HOME Variable

        speak_file_path = f"{h}/projects/py/TTS/speak_file.py"

        f_path = "/tmp/sl5_aura/simulate_conversation.txt"
        # --- FIX: stdout explizit stummschalten ---
        subprocess.run(
            ['python', speak_file_path, f_path],
            stdout=subprocess.DEVNULL,  # <--- WICHTIG: Das hier fehlte/war falsch positioniert
            stderr=subprocess.DEVNULL,  # Auch Fehler unterdrücken
            check=False                 # Verhindert Absturz, falls Exit-Code != 0
        )


    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")


# --- BOT B: AURA (Ollama 2 + Python Logic) ---
def ask_aura(question):
    """
    Ruft das echte Aura-Plugin auf.
    """
    # print(f"🎤 INPUT: '{question}'")

    match_data = {'regex_match_obj': MockMatchObj(question)}

    start = time.time()
    # Hier passiert die Magie (Cache, Readme-Suche, etc.)
    response = ask_ollama.execute(match_data)
    duration = time.time() - start


    print(f"🤔: '{question}'")


    print(f"\n")

    print(f"🗣 SL5 AURA ({duration:.2f}s): {response}… 🗣 SL5.de╱Aura")

    f = "/tmp/sl5_aura/simulate_conversation.txt"
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w") as file:
        file.write(response)




    speak(response)

    # sys.exit(1)

    return response

# --- MAIN LOOP ---
def main():
    print("🎬 Starte Simulation: User-Bot vs. Aura")
    print("=======================================")

    # Start-Szenario
    last_response = ("Hallo! Ich bin '🗣 SL5 Aura', dein offline, privacy-first, voice assistant framework. "
                     "Ich habe Zugriff auf meine eigene Dokumentation.")
    print(f"🗣 SL5 AURA (Start): {last_response}")
    print(f"\n")

    script_start_time = time.time()

    for i in range(1, ROUNDS + 1):

        if psutil.virtual_memory().percent > 80:
            # restart your script is a very common and effective fallback workaround for managing excessive memory usage
            print(' memory().percent > 80% -> exit. protected excessive memory usage')
            sys.exit(1)



        print("\n")

        # 1. User generiert Frage

        question = "Aura. Was ist SL5 Aura?"
        if True:
            question = generate_user_question(last_response, i)
        if not question:
            print("❌ User-Bot ist abgestürzt.")
            break

        # 2. Aura antwortet
        response = ask_aura(question)


        # -------------------------------------------------------------
        # BERECHNUNGEN FÜR DIE AUSGABE (am Ende jeder Runde)
        # -------------------------------------------------------------

        # 1. Bisherige Laufzeit (verstrichen)
        elapsed_time_secs = time.time() - script_start_time

        # 2. Durchschnittliche Zeit pro Runde (Vermeidung von Division durch Null bei i=1)
        # Wenn i > 0, berechne Durchschnitt, sonst 0
        avg_time_per_round = elapsed_time_secs / i if i > 0 else 0

        # 3. Geschätzte Gesamtzeit (für alle ROUNDS)
        estimated_total_time_secs = avg_time_per_round * ROUNDS

        # 4. Geschätzte verbleibende Zeit
        remaining_time_secs = estimated_total_time_secs - elapsed_time_secs

        # 5. Voraussichtliches Ende (Timestamp)
        estimated_end_timestamp = script_start_time + estimated_total_time_secs

        # 6. Formatierung der Endzeit in einen lesbaren String
        estimated_end_str = datetime.datetime.fromtimestamp(estimated_end_timestamp).strftime('%H:%M:%S')

        # 7. Formatierung der Zeitdauern in einen lesbaren String (Minuten, Sekunden)
        # Verwenden Sie hier die Funktion format_duration, die wir zuvor besprochen haben
        # (Ich nehme an, diese ist verfügbar, ansonsten nutzen Sie eine einfache Rundung)

        total_duration_str = utils.format_duration(estimated_total_time_secs)
        remaining_duration_str = utils.format_duration(remaining_time_secs)

        # -------------------------------------------------------------
        # AUSGABE MIT F-STRING
        # -------------------------------------------------------------


        print(f"\n\n Nr. {i} 📊  ")
        print(f"vorrausichtliches gesamt Dauer der {ROUNDS} Durchläufe {total_duration_str} \n"
              f"und vorraussichtliches Ende der {ROUNDS} Durchläufe um {estimated_end_str} \n"
              f"und noch verbleibndee Zeit: {remaining_duration_str} \n")


        # Speichern für nächste Runde
        last_response = response

        # Kurze Pause
        time.sleep(0.03)
        print("_" * 40)
        print("\n")


    print("\n✅ Simulation beendet.")
    print("Tipp: Die generierten Antworten sind jetzt im Cache und stehen sofort zur Verfügung!")

if __name__ == "__main__":
    # 🚨

    # https://stackoverflow.com/a/69511430/2891692
    # psutil.virtual_memory().percent



    check_db_statistics_and_exit_if_invalid()

    main()


