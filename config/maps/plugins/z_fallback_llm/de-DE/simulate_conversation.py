import sys
import os
import subprocess
import time
#import re

# Sicherstellen, dass wir ask_ollama finden
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import ask_ollama
except ImportError:
    print("❌ FEHLER: Konnte 'ask_ollama.py' nicht importieren.")
    sys.exit(1)

# --- KONFIGURATION ---
ROUNDS = 5  # Wie oft sollen sie hin und her reden?

# --- MOCK OBJEKT (Damit Aura denkt, es kommt vom Mikrofon) ---
class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        return ("Computer", self.text)
    def group(self, index):
        if index == 2: return self.text
        return "Computer"

# --- BOT A: DER USER (Ollama 1) ---
def generate_user_question(last_aura_response, round_num):
    """
    Dieser Bot simuliert den User. Er reagiert auf Auras Antwort.
    """
    print(f"\n🤔 User-Bot überlegt (Runde {round_num})...")

    system_prompt = (
        "Du bist ein neugieriger, kritischer User, der einen neuen Open-Source Sprachassistenten testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, knackige Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Computer, '.\n"
        "3. Sei kreativ! Frag nach Details, Installation, Witzen oder technischen Grenzen.\n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )
    system_prompt = (
        "Du bist ein User, Ergotherapeut mit Schwehrbehinderten, der sehr selten Computer benutz und das neue Open-Source assistant framework testet.\n"
        "Du hast keine Ahnung, wie er funktioniert.\n"
        "REGELN:\n"
        "1. Stelle EINE kurze, Frage basierend auf der letzten Antwort.\n"
        "2. Beginne den Satz IMMER mit 'Computer, '.\n"
        "3. Sei kreativ! \n"
        "4. Schreib nur den Satz, keine Anführungszeichen.\n"
    )

    # Kontext geben: Was hat Aura gerade gesagt?
    context_prompt = f"{system_prompt}\n\nLETZTE ANTWORT DES ASSISTENTEN:\n\"{last_aura_response}\"\n\nDEINE NÄCHSTE FRAGE:"

    cmd = ["ollama", "run", "llama3.2"]
    result = subprocess.run(cmd, input=context_prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        return None

    # Bereinigen (Manchmal ist Llama geschwätzig)
    question = result.stdout.strip().replace('"', '')

    # Sicherstellen, dass "Computer" am Anfang steht (falls Llama es vergisst)
    if not question.lower().startswith("computer"):
        question = "Computer, " + question

    return question

# --- BOT B: AURA (Ollama 2 + Python Logic) ---
def ask_aura(question):
    """
    Ruft das echte Aura-Plugin auf.
    """
    print(f"🎤 INPUT: '{question}'")

    match_data = {'regex_match_obj': MockMatchObj(question)}

    start = time.time()
    # Hier passiert die Magie (Cache, Readme-Suche, etc.)
    response = ask_ollama.execute(match_data)
    duration = time.time() - start

    print(f"🔮 AURA ({duration:.2f}s): {response}")
    return response

# --- MAIN LOOP ---
def main():
    print("🎬 Starte Simulation: User-Bot vs. Aura")
    print("=======================================")

    # Start-Szenario
    last_response = "Hallo! Ich bin Aura, dein offline Sprachassistent. Ich habe Zugriff auf meine eigene Dokumentation."
    print(f"🔮 AURA (Start): {last_response}")

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
        print("-" * 60)

    print("\n✅ Simulation beendet.")
    print("Tipp: Die generierten Antworten sind jetzt im Cache und stehen sofort zur Verfügung!")

if __name__ == "__main__":
    main()
