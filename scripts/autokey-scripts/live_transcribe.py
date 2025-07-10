import os
import subprocess
import time
from pathlib import Path

import tomllib # In Python 3.11+ Standard
CONFIG_PATH = Path.home() / ".config/sl5-stt/config.toml"
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)
PROJECT_DIR = Path(config["paths"]["project_root"])

SERVICE_NAME = "dictation_service"
HEARTBEAT_FILE = f"/tmp/{SERVICE_NAME}.heartbeat"
HEARTBEAT_INTERVAL_SECONDS = 10 # Should be less than MAX_STALE_SECONDS

# source /pfad/zum/venv/bin/activate

home_dir = Path.home()
# PROJECT_DIR = home_dir / "projects" / "py" / "STT"

# --- Dateipfade für den Zustand ---
VOSK_MODEL_FILE = PROJECT_DIR / "config/model_name.txt"
VOSK_LASTUSED_FILE = PROJECT_DIR / "config/model_name_lastused.txt"

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

def isHearHealty(HEARTBEAT_FILE, MAX_STALE_SECONDS):
    if os.path.isfile(HEARTBEAT_FILE):
        try:
            with open(HEARTBEAT_FILE, 'r') as f:
                last_update_str = f.read().strip()
                last_update = int(float(last_update_str))
            
            current_time = int(time.time())
            age = current_time - last_update

            if age < MAX_STALE_SECONDS:
                print("Service appears to be running and healthy.")
                return True
                sys.exit(0)
            else:
                print("Service heartbeat is stale. Attempting to restart.")
                return False
                # The logic to restart the service would go here.
                
        except (IOError, ValueError):
            print("Heartbeat file is present but unreadable or corrupt.")
            return False
            # Treat as if the service is not running correctly.
    else:
        print("Service is not running.")
        return False




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
python_executable = PROJECT_DIR / ".venv" / "bin" / "python"
service_script_path = PROJECT_DIR / service_name

# Werte aus Dateien lesen statt aus dem storeHockey Test Test Test
# Wir geben einen Standardwert für vosk_model an, falls die Datei beim allerersten Start nicht existiert
vosk_model = read_from_file(VOSK_MODEL_FILE, default_value="vosk-model-de-0.21")
vosk_model_lastused = read_from_file(VOSK_LASTUSED_FILE)

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
            server_script = os.path.expanduser(f"{PROJECT_DIR}/scripts/activate-venv_and_run-server.sh")

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
    for _ in range(5):
        try:
            system.exec_command(f"notify-send 'start ' ' {vosk_model}...' -t 5000")
            start_command = f"{PROJECT_DIR}/scripts/activate-venv_and_run-server.sh"

            proc = subprocess.Popen([start_command])
            subprocess.run(["notify-send", "STT Server Started", f"Running with PID: {proc.pid}"])

            time.sleep(5)
            check_command = ['pgrep', '-f', service_name]
            result = subprocess.run(check_command, capture_output=True)

            if result.returncode == 0:
                system.exec_command(f"notify-send 'STT runs' '{vosk_model}'")
            else:
                system.exec_command(f"notify-send 'Error' 'STT not runs'")
                error(1)
                
            for _ in range(15):
                if isHearHealty(HEARTBEAT_FILE, HEARTBEAT_INTERVAL_SECONDS):
                    break
                time.sleep(1)
                                
            break  # break out of the loop if no exception occurs
            
        except Exception as e:
            print(f"Exception: {e}")
            system.exec_command(f"notify-send 'Exception' '{e}'")
            time.sleep(4)
            # continue to the next iteration if an exception occurs

system.exec_command(f'touch {trigger_file}')
# 