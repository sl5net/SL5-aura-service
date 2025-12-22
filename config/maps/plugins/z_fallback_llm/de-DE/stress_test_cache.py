# config/maps/plugins/z_fallback_llm/de-DE/stress_test_cache.py
import sys
import os
import time
#from pathlib import Path

# Import erzwingen
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # stress_test_cache.py
    from . import ask_ollama
except ImportError:
    print("❌ 'stress_test_cache.py:11: ask_ollama.py' nicht gefunden 1.12.'25 16:32 Mon.")
    sys.exit(1)

# Mock Objekt
class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        return ("Computer", self.text)
    def group(self, index):
        if index == 2: return self.text
        return "Computer"

def main():
    print("🔨 Starte Cache Stress-Test (Papageien-Modus)...")
    print("------------------------------------------------")

    # Diese Fragen deaktivieren die History -> Identischer Hash garantiert!
    questions = [
        "Computer, was steht in der Readme?",
        "Computer, wie installiere ich das Projekt?",
        "Computer, welche Features gibt es?"
    ]

    # Wir stellen jede Frage 5 mal
    REPEAT_COUNT = 5

    for q in questions:
        print(f"\n📢 Teste Frage: '{q}'")

        for i in range(1, REPEAT_COUNT + 1):
            print(f"   Lauf {i}/{REPEAT_COUNT}...", end="", flush=True)

            match_data = {'regex_match_obj': MockMatchObj(q)}

            start = time.time()
            # Hier wird execute aufgerufen
            # Lauf 1: Cache Miss (Langsam)
            # Lauf 2-5: Cache Hit (Schnell)
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
