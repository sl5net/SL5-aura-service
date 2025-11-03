# In Ihrer CONFIG_DIR / 'translate_german_to_portuguese.py'

import sys
from pathlib import Path
import subprocess

# Pfad zur Statusdatei
STATE_FILE = Path(__file__).parent / 'translation_state.txt'

# --- KONFIGURATION für das externe Übersetzungstool ---
# Python-Interpreter für das neue Skript
PYTHON_EXECUTABLE = Path.home() / 'projects' / 'py' / 'STT' / '.venv' / 'bin' / 'python3'
# WICHTIG: Pfad zum NEUEN, sauberen Skript
TRANSLATE_SCRIPT = Path.home() / 'projects' / 'py' / 'STT' / 'tools' / 'simple_translate.py' # ANPASSEN, falls der Pfad anders ist

def execute(match_data):
    """
    Prüft den Übersetzungsmodus. Wenn aktiv, wird der Text mit dem sauberen
    simple_translate.py Skript übersetzt und das Ergebnis zurückgegeben.
    """
    # 1. Prüfen, ob der Übersetzungsmodus aktiv ist
    original_text = match_data.get('original_text')

    #

    if not STATE_FILE.exists() or STATE_FILE.read_text().strip().lower() != 'on':
        return original_text  # Modus aus, nichts tun

    try:
        if not original_text:
            return None # Kein Text zum Übersetzen

        print(f"INFO: [Translator Plugin] Übersetze: '{original_text}'")

        # 2. Das NEUE, saubere Übersetzungsskript aufrufen
        command = [
            str(PYTHON_EXECUTABLE),
            str(TRANSLATE_SCRIPT),
            original_text,
            'pt-BR' # Ziel: Brasilianisches Portugiesisch
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True, # Löst einen Fehler aus, wenn simple_translate.py mit sys.exit(1) endet
            encoding='utf-8'
        )


        #

        translated_text = result.stdout.strip()

        # 3. Das reine Ergebnis zurückgeben, damit der Service es sprechen kann
        return f"{translated_text} (original: {original_text} ) "

    except subprocess.CalledProcessError as e:
        # Das simple_translate.py Skript hat einen Fehler gemeldet.
        # Die Fehlermeldung steht in e.stderr.
        print(f"ERROR: [Translator Plugin] Fehler vom Übersetzungsskript: {e.stderr.strip()}", file=sys.stderr)
        return "Bei der Übersetzung ist ein Fehler aufgetreten."
    except Exception as e:
        print(f"ERROR: [Translator Plugin] Unerwarteter Fehler: {e}", file=sys.stderr)
        return "Bei der Übersetzung ist ein unerwarteter Fehler aufgetreten."
