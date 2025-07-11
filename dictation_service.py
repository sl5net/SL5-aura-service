# File: ~/projects/py/STT/dictation_service.py
import vosk, sys, time
import sounddevice as sd
import queue, json, pyperclip, subprocess
from pathlib import Path
import argparse
import os, atexit, requests, logging
import platform, threading

from scripts.py.func import cleanup

from scripts.py.func.main import main

from pathlib import Path
from config.settings import (LANGUAGETOOL_RELATIVE_PATH,
                            USE_EXTERNAL_LANGUAGETOOL, EXTERNAL_LANGUAGETOOL_URL, LANGUAGETOOL_PORT,
                            CRITICAL_THRESHOLD_MB)

PROJECT_ROOT = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = PROJECT_ROOT / LANGUAGETOOL_RELATIVE_PATH


suspicious_events = []
if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
    NOTIFY_SEND_PATH = None
else:
    TMP_DIR = Path("/tmp")
OUTPUT_FILE = TMP_DIR / "tts_output.txt"
TRIGGER_FILE = TMP_DIR / "vosk_trigger"

HEARTBEAT_FILE = TMP_DIR / "dictation_service.heartbeat"
PIDFILE = TMP_DIR / "dictation_service.pid"
LOG_FILE = Path("vosk_dictation.log")

SCRIPT_DIR = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"

languagetool_process = None



# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    handlers=[
        logging.FileHandler(f'{SCRIPT_DIR}/vosk_dictation.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()
# --- Wrapper Script Check ---
if os.environ.get("DICTATION_SERVICE_STARTED_CORRECTLY") != "true":
    logger.fatal("FATAL: This script must be started using the 'activate-venv_and_run-server.sh' wrapper.")
    sys.exit(1)

from scripts.py.func.notify import notify
from scripts.py.func.cleanup import cleanup
from scripts.py.func.start_languagetool_server import start_languagetool_server
from scripts.py.func.stop_languagetool_server import stop_languagetool_server 
from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
from scripts.py.func.check_memory_critical import check_memory_critical
from scripts.py.func.normalize_punctuation import normalize_punctuation
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model

files_to_clean = [HEARTBEAT_FILE, PIDFILE, TRIGGER_FILE]
atexit.register(cleanup, logger, files_to_clean)

with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

# --- Argument Parsing und Model-Setup ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21"
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
parser.add_argument('--test-text', help="Bypass microphone and use this text for testing.")
args = parser.parse_args()
VOSK_MODEL_FILE = SCRIPT_DIR / "config/model_name.txt"
vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT
MODEL_PATH = SCRIPT_DIR / "models" / MODEL_NAME

import scripts.py.func.guess_lt_language_from_model

LT_LANGUAGE = guess_lt_language_from_model(MODEL_NAME)


# --- Model Loading und Server-Start ---
logger.info("--- Vosk dictation_service starting ---")
TRIGGER_FILE.unlink(missing_ok=True)




active_lt_url = None

if USE_EXTERNAL_LANGUAGETOOL:
    logger.warning(f"USING EXTERNAL LT SERVER: {EXTERNAL_LANGUAGETOOL_URL}. AT YOUR OWN RISK.")
    active_lt_url = EXTERNAL_LANGUAGETOOL_URL
    # PING-TEST:
    try:
        requests.get(f"{active_lt_url}/v2/languages", timeout=3)
        logger.info("External LanguageTool server is responsive.")
    except requests.exceptions.RequestException:
        logger.fatal("External LanguageTool server did not respond. Is it running?")
        sys.exit(1)
else:
    PROJECT_ROOT = Path(__file__).resolve().parent
    jar_path_absolute = PROJECT_ROOT / LANGUAGETOOL_RELATIVE_PATH
    internal_lt_url = f"http://localhost:{LANGUAGETOOL_PORT}"

    languagetool_process = start_languagetool_server(logger, jar_path_absolute, internal_lt_url)
    if not languagetool_process: sys.exit(1)
    atexit.register(stop_languagetool_server, logger, languagetool_process)
    active_lt_url = f"http://localhost:{LANGUAGETOOL_PORT}/v2/check"





if not start_languagetool_server:
    notify("Vosk Startup Error", "LanguageTool Server failed to start.", "critical")
    sys.exit(1)
if not MODEL_PATH.exists():
    notify("Vosk Startup Error", f"Model not found: {MODEL_PATH}", "critical")
    sys.exit(1)
try:
    model = vosk.Model(str(MODEL_PATH))
    logger.info(f"{MODEL_NAME} loaded. Waiting for trigger.")
    notify("Vosk Ready", f"{MODEL_NAME} loaded.", icon="media-record")
except Exception as e:
    notify("Vosk Error", f"Could not load model {MODEL_NAME}: {e}", "critical")
    sys.exit(1)
# --- Kernlogik für die Verarbeitung (läuft im Thread) ---
recording_time = 0
if __name__ == "__main__":


    config = {
        "TMP_DIR": TMP_DIR,
        "HEARTBEAT_FILE": HEARTBEAT_FILE,
        "PIDFILE": PIDFILE,
        "TRIGGER_FILE": TRIGGER_FILE,
        "LT_LANGUAGE": LT_LANGUAGE,
        "CRITICAL_THRESHOLD_MB": CRITICAL_THRESHOLD_MB   
    }
    main(logger, LT_LANGUAGE, model, config, suspicious_events, TMP_DIR, recording_time,active_lt_url)
#

