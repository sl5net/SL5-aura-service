import sys
import os
import subprocess
import time
#import re
#import sys
#from pathlib import Path
#import subprocess

# --- KONFIGURATION ---
ROUNDS = 500  # Wie oft sollen sie hin und her reden?


# Sicherstellen, dass wir ask_ollama finden
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import ask_ollama
except ImportError:
    print("❌ FEHLER: Konnte 'ask_ollama.py' nicht importieren.")
    sys.exit(1)


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

    system_prompt = (
        "Du bist ein User, Ergotherapeut mit Schwehrbehinderten, der sehr selten Computer benutz und das neue Open-Source assistant framework testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! \n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    system_prompt = (
        "Du bist ein neugieriger, kritischer User, der einen neuen Open-Source Sprachassistenten testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, knackige Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Aura, '.\n"
        "3. Sei kreativ! Frag nach Details, Installation, Witzen oder technischen Grenzen.\n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    # Kontext geben: Was hat Aura gerade gesagt?
    context_prompt = f"{system_prompt}\n\nLETZTE ANTWORT DES ASSISTENTEN:\n\"{last_aura_response}\"\n\nDEINE NÄCHSTE FRAGE:"

    # cmd = ["ollama", "run", "llama3.2"]
    cmd = ["ollama", "run", "llama3.2"]
    result = subprocess.run(cmd, input=context_prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        return None

    # Bereinigen (Manchmal ist Llama geschwätzig)
    question = result.stdout.strip().replace('"', '')

    speak_espeak(question)
    # speak(question)

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

        f = "/tmp/sl5_aura/simulate_conversation.txt"
        subprocess.run(['python', speak_file_path, f], subprocess.DEVNULL, stderr=subprocess.DEVNULL)





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

    for i in range(1, ROUNDS + 1):
        # 1. User generiert Frage
        question = generate_user_question(last_response, i)
        if not question:
            print("❌ User-Bot ist abgestürzt.")
            break

        # 2. Aura antwortet
        response = ask_aura(question)

        # Speichern für nächste Runde
        last_response = response

        # Kurze Pause für Lesbarkeit
        time.sleep(1)
        print("_" * 40)

    print("\n✅ Simulation beendet.")
    print("Tipp: Die generierten Antworten sind jetzt im Cache und stehen sofort zur Verfügung!")

if __name__ == "__main__":
    main()
