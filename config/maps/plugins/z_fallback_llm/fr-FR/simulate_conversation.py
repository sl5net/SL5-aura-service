# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/z_fallback_llm/de-DE/simulate_conversation.py

from scripts.py.func.get_project_root import get_aura_project_root
import datetime
import logging
import os
import sys
import time
import psutil
import subprocess

from pathlib import Path

# Votre logique SL5NET_AURA_PROJECT_ROOT

tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
SL5NET_AURA_PROJECT_ROOT = get_aura_project_root()

# Ajouter le chemin vers le répertoire actuel du plugin pour les importations absolues

PLUGIN_DIR = str(SL5NET_AURA_PROJECT_ROOT / "config" / "maps" / "plugins" / "z_fallback_llm" / "de-DE")
if PLUGIN_DIR not in sys.path:
    sys.path.insert(0, PLUGIN_DIR)

# Désormais, les importations absolues fonctionnent sans le point (.)

import utils
import health_checks
import ask_ollama

# --- CONFIGURATION ---

ROUNDS = 900  # Wie oft sollen sie hin und her reden?

# utils.log_debug(f"🚀 début 04/12/25 16h45 jeu")

# utils.log_debug(f"🚀 début 04/12/25 17h12 jeu")



# sys.exit(1)



# https://ollama.com/download



# S'assurer que nous trouvons Ask_ollama

# try:

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# importer Ask_ollama

# sauf ImportError :

# print("❌ ERREUR : Impossible d'importer 'ask_ollama.py'.")

# sys.exit(1)




# simuler_conversation.py


log = logging.getLogger("simulate_conversation")
GITHUB_BASE = "https://github.com/sl5net/SL5-aura-service/blob/master"

def get_github_url(file_path):
    """Erstellt den passenden GitHub-Link aus dem lokalen Pfad."""
    rel_path = ""
    if "STT/" in str(file_path):
        rel_path = str(file_path).split("STT/")[1]
    elif "SL5-aura-service/" in str(file_path):
        rel_path = str(file_path).split("SL5-aura-service/")[1]
    if rel_path:
        url = f"{GITHUB_BASE}/{rel_path}"
        log.debug(f"get_github_url: {file_path} -> {url}")
        return url
    log.warning(f"get_github_url: kein STT/ oder SL5-aura-service/ in Pfad: {file_path}")
    return None


# --- OBJET MOCK (Pour qu'Aura pense que ça vient du micro) ---

class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        # return("Ordinateur", self.text)

        return ("Aura", self.text)
    def group(self, index):
        if index == 2: return self.text
        # renvoyer "ordinateur"

        return "Aura"

# --- BOT A : L'UTILISATEUR (Ollama 1) ---

def generate_user_question(last_aura_response, round_num):
    """
    Dieser Bot simuliert den User. Er reagiert auf Auras Antwort.
    """
    # print(f"\n🤔 Le robot utilisateur considère (round {round_num})…")


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
        "Kontext: Aura ist headless, nutzt '/tmp/sl5_record.trigger' et Configurations dans 'config/maps/'.\n\n"

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

    # Donner le contexte : qu'est-ce qu'Aura vient de dire ?

    context_prompt = f"{system_prompt}\n\nLETZTE ANTWORT DES ASSISTENTEN:\n\"{last_aura_response}\"\n\nDEINE NÄCHSTE FRAGE:"

    # cmd = ["ollama", "run", "llama3.2"]

    cmd = ["ollama", "run", "llama3.2"]
    result = subprocess.run(cmd, input=context_prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        return None

    # Nettoyer (parfois le lama est bavard)

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

    # Assurez-vous que "Ordinateur" est au début (au cas où Llama oublierait)

    if not question.lower().startswith("aura"):
        question = "Aura, " + question

    return question



def speak_espeak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)

    # h = os.environ.get("HOME", "/tmp") # Variable $HOME

    # f = "/tmp/sl5_aura/simulate_conversation.txt"

    # process = subprocess.run(['python', speak_file_path, f], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")

def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        # subprocess.run(['espeak', '-v', 'de', text], check=True)


        h = os.environ.get("HOME", "/tmp")  # $HOME Variable

        speak_file_path = f"{h}/projects/py/TTS/speak_file.py"

        f_path = "/tmp/sl5_aura/simulate_conversation.txt"
        # --- CORRECTIF : couper explicitement la sortie standard ---

        subprocess.run(
            ['python', speak_file_path, f_path],
            stdout=subprocess.DEVNULL,  # <--- WICHTIG: Das hier fehlte/war falsch positioniert
            stderr=subprocess.DEVNULL,  # Auch Fehler unterdrücken
            check=False                 # Verhindert Absturz, falls Exit-Code != 0
        )


    except Exception:
        print(f"STDOUT (TTS-Fallback): {text}")


# --- BOT B : AURA (Ollama 2 + Python Logic) ---

def ask_aura(question):
    """
    Ruft das echte Aura-Plugin auf.
    """
    # print(f"🎤 INPUT : '{question}'")


    match_data = {'regex_match_obj': MockMatchObj(question)}

    start = time.time()
    # C'est là que la magie opère (cache, recherche readme, etc.)

    response = ask_ollama.execute(match_data)
    duration = time.time() - start


    print(f"🤔: '{question}'")


    print("\n")

    print(f"🗣 SL5 AURA ({duration:.2f}s): {response}… 🗣 SL5.de╱Aura")

    f = "/tmp/sl5_aura/simulate_conversation.txt"
    os.makedirs(os.path.dirname(f), exist_ok=True)
    with open(f, "w") as file:
        file.write(response)




    speak(response)

    # sys.exit(1)


    return response

# --- BOUCLE PRINCIPALE ---

def main():
    print("🎬 Starte Simulation: User-Bot vs. Aura")
    print("=======================================")

    # Scénario de départ

    last_response = ("Hallo! Ich bin '🗣 SL5 Aura', dein offline, privacy-first, voice assistant framework. "
                     "Ich habe Zugriff auf meine eigene Dokumentation.")
    print(f"🗣 SL5 AURA (Start): {last_response}")
    print("\n")

    script_start_time = time.time()

    for i in range(1, ROUNDS + 1):

        if psutil.virtual_memory().percent >90:
            # redémarrer votre script est une solution de secours très courante et efficace pour gérer une utilisation excessive de la mémoire

            print(' memory().percent > 90% -> exit. protected excessive memory usage')
            sys.exit(1)



        print("\n")

        # 1. L'utilisateur génère une question


        question = "Aura. Was ist SL5 Aura?"
        if True:
            question = generate_user_question(last_response, i)
        if not question:
            print("❌ User-Bot ist abgestürzt.")
            break

        # 2. Aura répond

        response = ask_aura(question)


        # -------------------------------------------------------------

        # CALCULS DE SORTIE (à la fin de chaque tour)

        # -------------------------------------------------------------


        # 1. Mandat précédent (écoulé)

        elapsed_time_secs = time.time() - script_start_time

        # 2. Temps moyen par tour (en évitant la division par zéro lorsque i=1)

        # Si i > 0, calculez la moyenne, sinon 0

        avg_time_per_round = elapsed_time_secs / i if i > 0 else 0

        # 3. Temps total estimé (pour tous les TOURS)

        estimated_total_time_secs = avg_time_per_round * ROUNDS

        # 4. Temps restant estimé

        remaining_time_secs = estimated_total_time_secs - elapsed_time_secs

        # 5. Fin estimée (horodatage)

        estimated_end_timestamp = script_start_time + estimated_total_time_secs

        # 6. Formatage de l'heure de fin dans une chaîne lisible

        estimated_end_str = datetime.datetime.fromtimestamp(estimated_end_timestamp).strftime('%H:%M:%S')

        # 7. Formatage des durées dans une chaîne lisible (minutes, secondes)

        # Utilisez ici la fonction format_duration dont nous avons discuté plus tôt

        # (Je suppose que cela est disponible, sinon utilisez un simple arrondi)


        total_duration_str = utils.format_duration(estimated_total_time_secs)
        remaining_duration_str = utils.format_duration(remaining_time_secs)

        # -------------------------------------------------------------

        # PROBLEME AVEC F-STRING

        # -------------------------------------------------------------



        print(f"\n\n Nr. {i} 📊  ")
        print(f"vorrausichtliches gesamt Dauer der {ROUNDS} Durchläufe {total_duration_str} \n"
              f"und vorraussichtliches Ende der {ROUNDS} Durchläufe um {estimated_end_str} \n"
              f"und noch verbleibndee Zeit: {remaining_duration_str} \n")


        # Enregistrer pour le prochain tour

        last_response = response

        # Courte pause

        time.sleep(0.03)
        print("_" * 40)
        print("\n")


    print("\n✅ Simulation beendet.")
    print("Tipp: Die generierten Antworten sind jetzt im Cache und stehen sofort zur Verfügung!")

if __name__ == "__main__":
    # 🚨


    # https://stackoverflow.com/a/69511430/2891692

    # psutil.virtual_memory().percent




    health_checks.check_db_statistics_and_exit_if_invalid()

    main()


