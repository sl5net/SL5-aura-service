intertingDontDeleteIt = """
pkill -f dictation_service.py
pgrep -f dictation_service.py
"""
import time

from pathlib import Path

import tomllib # In Python 3.11+ Standard
CONFIG_PATH = Path.home() / ".config/sl5-stt/config.toml"
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)
PROJECT_DIR = Path(config["paths"]["project_root"])


# --- Hilfsfunktion zum Schreiben in eine Datei ---
def write_to_file(filepath, content):
    """Schreibt den Inhalt sicher in eine Datei."""
    try:
        Path(filepath).write_text(str(content))
    except Exception as e:
        system.exec_command(f"notify-send 'FEHLER' 'Konnte nicht in {filepath} schreiben: {e}'")

# --- Hauptlogik ---

home_dir = Path.home()
# PROJECT_DIR = home_dir / "projects" / "py" / "STT"
VOSK_MODEL_FILE = PROJECT_DIR / "config/model_name.txt"

# new_model = "vosk-model-small-en-us-0.15"
new_model = "vosk-model-de-0.21"

# Den neuen Wert in die Datei schreiben
#
write_to_file(VOSK_MODEL_FILE, new_model)

# system.exec_command(f"notify-send 'Modell: ' '{new_model}'")
system.exec_command(f"notify-send 'Modell: ' '{new_model}' -t 2000")

# Das live_transcribe Skript aufrufen. Eine Verzögerung ist nicht mehr nötig.
engine.run_script("live_transcribe")

# testWouldn't be GaetaUnd wie geht's
