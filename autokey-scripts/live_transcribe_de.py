intertingDontDeleteIt = """
pkill -f dictation_service.py
pgrep -f dictation_service.py
"""
import time
from pathlib import Path
# --- Hilfsfunktion zum Schreiben in eine Datei ---
def write_to_file(filepath, content):
    """Schreibt den Inhalt sicher in eine Datei."""
    try:
        Path(filepath).write_text(str(content))
    except Exception as e:
        system.exec_command(f"notify-send 'FEHLER' 'Konnte nicht in {filepath} schreiben: {e}'")

# --- Hauptlogik ---
VOSK_MODEL_FILE = "/tmp/vosk_model"
# new_model = "vosk-model-small-en-us-0.15"
new_model = "vosk-model-de-0.21"

# Den neuen Wert in die Datei schreiben
write_to_file(VOSK_MODEL_FILE, new_model)

system.exec_command(f"notify-send 'Modell gesetzt' 'Neues Modell ist {new_model}'")

# Das live_transcribe Skript aufrufen. Eine Verzögerung ist nicht mehr nötig.
engine.run_script("live_transcribe")
# no everything looks like expectednun funktioniert alles wie erwartetgute nacht