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

# config/maps/plugins/z_fallback_llm/de-DE/stress_test_cache.py

import sys
import os
import time
# à partir du chemin d'importation pathlib


# Forcer l'importation

try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # stress_test_cache.py

    from . import ask_ollama
except ImportError:
    print("❌ 'stress_test_cache.py:11: ask_ollama.py' nicht gefunden 1.12.'25 16:32 Mon.")
    sys.exit(1)

# Objet simulé

class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        return ("Computer", self.text)
    def group(self, index):
        if index == 2: return self.text
        return "Computer"

def main():
    print("🔨 Starte Cache Stress-Test (Papageien-Modus)…")
    print("------------------------------------------------")

    # Ces questions désactivent l'historique -> Hachage identique garanti !

    questions = [
        "Computer, was steht in der Readme?",
        "Computer, wie installiere ich das Projekt?",
        "Computer, welche Features gibt es?"
    ]

    # Nous posons chaque question 5 fois

    REPEAT_COUNT = 5

    for q in questions:
        print(f"\n📢 Teste Frage: '{q}'")

        for i in range(1, REPEAT_COUNT + 1):
            print(f"   Lauf {i}/{REPEAT_COUNT}…", end="", flush=True)

            match_data = {'regex_match_obj': MockMatchObj(q)}

            start = time.time()
            # L'exécution est appelée ici

            # Exécution 1 : manque de cache (lent)

            # Exécution 2-5 : accès au cache (rapide)

            ask_ollama.execute(match_data)
            duration = time.time() - start

            if duration < 1.0:
                print(f" ⚡ HIT ({duration:.2f}s)")
            else:
                print(f" 🐢 MISS/GENERATE ({duration:.2f}s)")

    print("\n================================================")
    print("✅ Test beendet. Prüfe jetzt die DB 'usage_count'!")

if __name__ == "__main__":
    main()
