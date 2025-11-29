# warm_up_cache_v04.py
# Version: 0.4
# Status: Aura-Safe & Kreativer Modus (keine langweiligen Fragen mehr)
# https://ollama.com/download

import sys
import os
import re
import subprocess
import time
from pathlib import Path

# --- AURA SAFETY CHECK ---
ask_ollama = None
try:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import ask_ollama
except ImportError:
    pass

# --- HELPER: README FINDEN ---
def get_readme_content_standalone():
    try:
        current_path = Path(__file__).resolve()
        for _ in range(6):
            current_path = current_path.parent
            readme_path = current_path / "README.md"
            if readme_path.exists():
                print(f"📄 README gefunden: {readme_path}")
                content = readme_path.read_text(encoding='utf-8').strip()
                return content[:6000]
        print("❌ WARNUNG: Keine README.md gefunden.")
        return None
    except Exception as e:
        print(f"❌ Fehler beim Lesen der README: {e}")
        return None

# --- LLM FRAGEN GENERATOR (Kreativ-Modus) ---
def generate_questions_via_llm(readme_text):
    print("🧠 Aura liest die README und denkt sich Fragen aus...")

    # ÄNDERUNG: Der Prompt ist jetzt viel fordernder
    prompt = (
        "Du bist ein kritischer Software-Entwickler, der dieses Projekt evaluieren will.\n"
        "Lies die folgende Dokumentation und formuliere 5 spezifische, technische Fragen dazu.\n"
        "REGELN:\n"
        "1. Frag nach konkreten Features aus dem Text (z.B. Offline-Modus, Plugins, RAM).\n"
        "2. Keine langweiligen Fragen wie 'Wie geht das?'.\n"
        "3. Format: Nur die Fragen, eine pro Zeile. Deutsch.\n"
        "4. Sei abwechslungsreich!\n\n"
        f"DOKUMENTATION:\n{readme_text}\n"
    )

    cmd = ["ollama", "run", "llama3.2"]

    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        print(f"❌ Fehler bei Ollama: {result.stderr}")
        return []

    raw_lines = result.stdout.strip().split('\n')
    questions = []
    for line in raw_lines:
        # Bereinigung (Zahlen, Bulletpoints weg)
        clean_line = re.sub(r'^[\d\-\.\s\*\>]+', '', line).strip()
        # Nur Zeilen nehmen, die wie Fragen aussehen
        if clean_line and "?" in clean_line and len(clean_line) > 10:
            questions.append(clean_line)

    return questions

# --- MOCK OBJEKTE ---
class MockMatchObj:
    def __init__(self, text):
        self.text = text
    def groups(self):
        return ("Computer", self.text)
    def group(self, index):
        if index == 2: return self.text
        return "Computer"

def simulate_aura_request(question):
    if ask_ollama is None: return

    print(f"🤖 Lerne Antwort für: '{question}'")

    match_data = {
        'regex_match_obj': MockMatchObj(question)
    }

    start = time.time()
    try:
        # Hier wird der Cache befüllt!
        response = ask_ollama.execute(match_data)
        duration = time.time() - start
        preview = response.replace('\n', ' ')[:80] if response else "Keine Antwort"
        print(f"    ⏱️  Dauer: {duration:.2f}s")
        print(f"    💬 Antwort: {preview}...")
    except Exception as e:
        print(f"    ❌ Fehler: {e}")
    print("-" * 40)

def main():
    if ask_ollama is None:
        print("\n❌ FATAL: 'ask_ollama.py' nicht gefunden.")
        sys.exit(1)

    print("🔥 Starting Cache Warmer v0.4 (Creative Mode)")
    print("=============================================")

    try:
        os.system("rm -rf __pycache__")
    except Exception: pass

    readme = get_readme_content_standalone()
    if not readme: return

    # 1. Fragen generieren lassen
    questions = generate_questions_via_llm(readme)

    if not questions:
        print("❌ Ollama war stumm. Versuch es nochmal.")
        return

    # 2. Fragen anzeigen (Beweis für dich!)
    print("\n✨ Ollama hat sich folgende Fragen ausgedacht:")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q}")
    print("\n" + "=" * 60)

    # 3. Cache füllen
    for q in questions:
        simulate_aura_request(q)

    print("=" * 60)
    print("🎉 Training beendet.")

if __name__ == "__main__":
    main()
