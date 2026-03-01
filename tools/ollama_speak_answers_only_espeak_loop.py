#!/usr/bin/env python3
import subprocess
import sys
import re

# Konfiguration
MODEL = "llama3.2"
VOICE = "de-de" # this is man
VOICE = "de+f2" # f3 means femail „de+f1“ und „de+f2“
# i mean f1,f2 better then f3
# maybe i prefer f2

SPEED = "150"

def speak(text):
    """Sendet Text an espeak."""
    if not text.strip():
        return
    # Wir starten espeak als Unterprozess
    subprocess.run(["espeak", "-v", VOICE, "-s", SPEED, text], stderr=subprocess.DEVNULL)

def main():
    print(f"--- Ollama Sprach-Chat aktiv ({MODEL}) ---")
    print("Tippe 'exit' zum Beenden.")

    # Wir verwalten den Kontext manuell, damit Ollama sich an das Gespräch erinnert
    context = []

    while True:
        try:
            # 1. Benutzereingabe (Deine Frage)
            user_input = input("\nDu: ")

            if user_input.lower() in ['exit', 'quit', 'beenden']:
                break

            # 2. Ollama aufrufen
            # Wir nutzen 'ollama run', aber ohne interaktives Terminal,
            # damit kein Echo entsteht.
            process = subprocess.Popen(
                ["ollama", "run", MODEL, user_input],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            print("Ollama: ", end="", flush=True)

            full_response = ""
            sentence_buffer = ""

            # 3. Antwort von Ollama streamen
            for line in process.stdout:
                # Text im Terminal anzeigen
                print(line, end="", flush=True)
                full_response += line
                sentence_buffer += line

                # Sobald ein Satz zu Ende ist (Punkt, Ausrufezeichen, Fragezeichen)
                if any(punct in line for punct in ['.', '!', '?']):
                    # Den fertigen Satz vorlesen
                    speak(sentence_buffer.strip())
                    sentence_buffer = ""

            # Den Rest vorlesen, falls kein Satzzeichen am Ende war
            if sentence_buffer.strip():
                speak(sentence_buffer.strip())

            process.wait()

        except KeyboardInterrupt:
            print("\nBeendet.")
            break

if __name__ == "__main__":
    main()
