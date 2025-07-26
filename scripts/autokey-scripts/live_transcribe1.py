# File: scripts/autokey-scripts/sl5_stt_trigger.py
# This script's only job is to ensure the dictation service is running and then trigger it.
# The backend now handles language switching internally, so no restart is needed.

import os
import sys
import subprocess
import time
from pathlib import Path
import tomllib

# --- Configuration and Paths ---
try:
    CONFIG_PATH = Path.home() / ".config/sl5-stt/config.toml"
    with open(CONFIG_PATH, "rb") as f:
        config = tomllib.load(f)
    PROJECT_DIR = Path(config["paths"]["project_root"])
except (FileNotFoundError, KeyError) as e:
    subprocess.run(["notify-send", "-u", "critical", "SL5 STT Config Error", f"Could not load config: {e}"])
    sys.exit(1)

SERVICE_PY_NAME = "dictation_service.py"

TRIGGER_path = "/tmp/sl5_record.trigger"
TRIGGER_FILE = Path(TRIGGER_path)

HEARTBEAT_FILE = Path(f"/tmp/dictation_service.heartbeat")
# INCREASED TIMEOUT: Give the service more time to start
HEARTBEAT_MAX_AGE_SECONDS = 30 # Increased from 15

# --- Helper Function ---
def is_service_healthy(heartbeat_path, max_age):
    if not heartbeat_path.is_file():
        return False
    try:
        age = time.time() - int(heartbeat_path.read_text().strip())
        return age < max_age
    except (IOError, ValueError):
        return False

# --- Main Logic ---
# 1. Check if the service is already running and healthy.
# This is now the normal, fast path.
if not is_service_healthy(HEARTBEAT_FILE, HEARTBEAT_MAX_AGE_SECONDS):
    
    # 2. If not healthy, check if the process exists but is stalled.
    is_running = subprocess.run(['pgrep', '-f', SERVICE_PY_NAME]).returncode == 0
    if is_running:
        subprocess.run(["notify-send", "SL5 STT Warning", "Heartbeat stale. Killing old process."])
        subprocess.run(['pkill', '-f', SERVICE_PY_NAME])
        time.sleep(0.5)

    # 3. Start the service and wait for it to become ready.
    subprocess.run(["notify-send", "SL5 STT", "Service not running. Starting..."])
    start_script = PROJECT_DIR / "scripts/activate-venv_and_run-server.sh"
    subprocess.Popen([str(start_script)], shell=False)

    ready = False
    # Wait up to 30 seconds for the service to write its first heartbeat
    for _ in range(HEARTBEAT_MAX_AGE_SECONDS): 
        if is_service_healthy(HEARTBEAT_FILE, 5): # Check against a small window
            subprocess.run(["notify-send", "SL5 STT", "Service is now ready!"])
            ready = True
            break
        time.sleep(1)

    if not ready:
        subprocess.run(["notify-send", "-u", "critical", "SL5 STT Error", "Service failed to start. Check logs."])
        sys.exit(1)

# 4. If we are here, the service is running. Trigger it.
# TRIGGER_FILE.touch(exist_ok=True) # <= thats not stabel  12.7.'25 00:42 Sat
subprocess.run(["touch", TRIGGER_path, "Triggered"]) # <= thats works more tabel much better 12.7.'25 00:42 Sat
# 
# Optional: a quiet confirmation that the trigger was sent
# TestOkay das funktioniert
# subprocess.run(["notify-send", "-t", "1000", "SL5 STT", "Triggered..."])
