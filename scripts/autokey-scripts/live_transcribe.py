import subprocess
import time
from pathlib import Path
import os

# source /pfad/zum/venv/bin/activate

home_dir = Path.home()
project_dir = home_dir / "projects" / "py" / "STT"

# --- Dateipfade für den Zustand ---
VOSK_MODEL_FILE = project_dir / "config/model_name.txt"
VOSK_LASTUSED_FILE = project_dir / "config/model_name_lastused.txt"

# --- Hilfsfunktionen ---
def read_from_file(filepath, default_value=None):
    """
    Liest Inhalt aus einer Datei; gibt default_value zurück, wenn nicht vorhanden.
    """
    path = Path(filepath)
    if not path.exists():
        return default_value
    try:
        return path.read_text().strip()
    except Exception as e:
        system.exec_command(f"notify-send 'FEHLER' 'Konnte nicht aus {filepath} lesen: {e}'")
        return default_value

def write_to_file(filepath, content):
    """Schreibt den Inhalt sicher in eine Datei."""
    try:
        Path(filepath).write_text(str(content))
    except Exception as e:
        system.exec_command(f"notify-send 'FEHLER' 'Konnte nicht in {filepath} schreiben: {e}'")

# --- Ihre bestehende Logik, aber mit Dateizugriffen ---

# Andere Pfade und Variablen
service_name = "dictation_service.py"
trigger_file = Path("/tmp/vosk_trigger")
python_executable = project_dir / ".venv" / "bin" / "python"
service_script_path = project_dir / service_name

# Werte aus Dateien lesen statt aus dem store
# Wir geben einen Standardwert für vosk_model an, falls die Datei beim allerersten Start nicht existiert
vosk_model = read_from_file(VOSK_MODEL_FILE, default_value="vosk-model-de-0.21")
vosk_model_lastused = read_from_file(VOSK_LASTUSED_FILE)

# system.exec_command(f"notify-send 'Check' 'Soll: {vosk_model} | War: {vosk_model_lastused}' -t 4000")

if vosk_model != vosk_model_lastused:
    system.exec_command("notify-send 'INFO' 'Sprachmodell wird gewechselt...'")

    commandKill = f"/usr/bin/pkill -f {service_name} &"
    try:
        # This is the original command that sometimes fails
        system.exec_command(commandKill)
    except subprocess.CalledProcessError as e:
        # Check if the error is specifically the one we are looking for
        # (command was empty string and exit status was 1)
        if e.cmd == '' and e.returncode == 1:
            # If it is, run the specified server script instead.
            # Get the absolute path to the script in the home directory.
            server_script = os.path.expanduser('~/projects/py/STT/scripts/activate-venv_and_run-server.sh')

            # Execute the script
            system.exec_command(server_script)
        else:
            # If it's a different CalledProcessError, re-raise it
            # so you don't hide other potential problems.
            raise e


    # Kurze Pause, damit der pkill-Befehl wirken kann (dies ist immer noch eine gute Praxis)
    time.sleep(0.5)

    # Den neuen Zustand in die "lastused"-Datei schreiben
    write_to_file(VOSK_LASTUSED_FILE, vosk_model)

# --- Hauptlogik (bleibt unverändert) ---
check_command = ['pgrep', '-f', service_name]
result = subprocess.run(check_command, capture_output=True)

if result.returncode != 0:
    system.exec_command(f"notify-send 'start ' ' {vosk_model}...' -t 3000")

    # wehen teh script is already running. Then  the script gibes an Error. that we dont want see
    try:
        start_command = f"{project_dir}/scripts/activate-venv_and_run-server.sh"
        # start_command = f"{python_executable} {service_script_path} --vosk_model {vosk_model} &"
        system.exec_command(start_command)
    finally:
        time.sleep(5)

# system.exec_command(f"notify-send 'model:' '{vosk_model}'")
#tests certainly isn't oh great that's great

system.exec_command(f'touch {trigger_file}')

# how are you what to nameno everything looks like expected
#

# sometimes all
# blablab
