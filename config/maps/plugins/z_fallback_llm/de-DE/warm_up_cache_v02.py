# warm_up_cache_v03.py
# Version: 0.3
# Status: Aura-Safe (Crasht nicht beim Laden durch den Service)

import sys
import os
import re
import subprocess
import time
from pathlib import Path

# --- AURA SAFETY CHECK ---
# Wir definieren ask_ollama global als None.
# Wenn der Import fehlschlägt (weil Aura es lädt), crashen wir NICHT sofort.
ask_ollama = None

try:
    # Versuchen, das Modul zu laden (für manuelle Ausführung)
    # Wir fügen den aktuellen Ordner zum Pfad hinzu, damit Importe klappen
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import ask_ollama
except ImportError:
    # Wenn das fehlschlägt, machen wir gar nichts.
    # Aura wird diese Datei laden, sehen dass nichts passiert, und weitermachen.
    pass


# --- HELPER: README FINDEN ---
def get_readme_content_standalone():
    """Sucht die README.md eigenständig."""
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


# --- LLM FRAGEN GENERATOR ---
def generate_questions_via_llm(readme_text):
    print("🧠 Aura liest die README, um Fragen zu generieren...")

    prompt = (
        "Du bist ein QA-Engineer. Analysiere die folgende Dokumentation.\n"
        "Erstelle eine Liste mit den 5 häufigsten Fragen, die ein Nutzer dazu stellen würde.\n"
        "Format: Nur die Fragen, eine pro Zeile. Keine Nummerierung. Deutsch.\n"
        "Beispiele: 'Wie installiere ich das?', 'Welche Features gibt es?'\n\n"
        f"DOKUMENTATION:\n{readme_text}\n"
    )

    cmd = ["ollama", "run", "llama3.2"]

    # Nutzung von STDIN (Pipe) für Stabilität
    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        print(f"❌ Fehler bei Ollama: {result.stderr}")
        return []

    raw_lines = result.stdout.strip().split('\n')
    questions = []
    for line in raw_lines:
        clean_line = re.sub(r'^[\d\-\.\s]+', '', line).strip()
        if clean_line and "?" in clean_line:
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
    # Sicherheitscheck: Wenn ask_ollama fehlt, können wir nicht simulieren
    if ask_ollama is None:
        print(f"⚠️  Überspringe '{question}' (ask_ollama Modul nicht geladen)")
        return

    print(f"🤖 Simuliere Frage: '{question}'")

    match_data = {
        'regex_match_obj': MockMatchObj(question)
    }

    start = time.time()
    try:
        response = ask_ollama.execute(match_data)
        duration = time.time() - start
        preview = response.replace('\n', ' ')[:80] if response else "Keine Antwort"
        print(f"    ⏱️  Dauer: {duration:.2f}s")
        print(f"    💬 Antwort: {preview}...")
    except Exception as e:
        print(f"    ❌ Fehler bei der Ausführung: {e}")
    print("-" * 40)


def main():
    # --- WICHTIG: Erst hier prüfen wir den Import hart ---
    if ask_ollama is None:
        print("\n❌ FATAL ERROR: Konnte 'ask_ollama.py' nicht importieren.")
        print("   Bitte stelle sicher, dass 'ask_ollama.py' im selben Ordner liegt.")
        print("   Dieser Fehler ist normal, wenn Aura das Skript automatisch lädt,")
        print("   aber nicht, wenn du es manuell startest.\n")
        sys.exit(1)

    print("🔥 Starting Cache Warmer v0.3 for SL5 Aura...")
    print("=============================================")

    try:
        os.system("rm -rf __pycache__")
    except Exception:
        pass

    readme = get_readme_content_standalone()
    if not readme:
        print("❌ Abbruch: Keine Doku gefunden.")
        return

    questions = generate_questions_via_llm(readme)
    if not questions:
        print("❌ Abbruch: LLM hat keine Fragen generiert.")
        return

    print(f"✅ Habe {len(questions)} Fragen generiert.")
    print("=" * 60)

    for q in questions:
        simulate_aura_request(q)

    print("=" * 60)
    print("🎉 Cache Warming abgeschlossen! Datenbank ist gefüllt.")


if __name__ == "__main__":
    main()
