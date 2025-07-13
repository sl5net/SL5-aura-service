# File: STT/dictation_service.py
import sys, time, os, atexit, requests, logging, platform
from pathlib import Path

# --- Local Imports (grouped for clarity) ---
from config.settings import (LANGUAGETOOL_RELATIVE_PATH,
                            USE_EXTERNAL_LANGUAGETOOL, EXTERNAL_LANGUAGETOOL_URL, LANGUAGETOOL_PORT,
                            CRITICAL_THRESHOLD_MB, PRELOAD_MODELS)
from scripts.py.func.main import main
from scripts.py.func.notify import notify
from scripts.py.func.cleanup import cleanup
from scripts.py.func.start_languagetool_server import start_languagetool_server
from scripts.py.func.stop_languagetool_server import stop_languagetool_server
from scripts.py.func.check_memory_critical import check_memory_critical
# We need vosk here for the model loading
import vosk


# --- Constants and Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR # In this structure, SCRIPT_DIR is PROJECT_ROOT

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
else:
    TMP_DIR = Path("/tmp")

TRIGGER_FILE = TMP_DIR / "vosk_trigger"
HEARTBEAT_FILE = TMP_DIR / "dictation_service.heartbeat"
PIDFILE = TMP_DIR / "dictation_service.pid"
LOG_FILE = PROJECT_ROOT / "log/dictation_service.log"






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
LOG_FILE = Path("log/dictation_service.log")

SCRIPT_DIR = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"

languagetool_process = None



# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    handlers=[
        logging.FileHandler(f'{SCRIPT_DIR}/log/dictation_service.log', mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()
# --- Wrapper Script Check ---
"""
if os.environ.get("DICTATION_SERVICE_STARTED_CORRECTLY") != "true":
    logger.fatal("FATAL: This script must be started using the 'activate-venv_and_run-server.sh' wrapper.")
    sys.exit(1)
"""

from scripts.py.func.notify import notify
from scripts.py.func.cleanup import cleanup
from scripts.py.func.start_languagetool_server import start_languagetool_server
from scripts.py.func.stop_languagetool_server import stop_languagetool_server
from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
from scripts.py.func.check_memory_critical import check_memory_critical
from scripts.py.func.stop_languagetool_server import stop_languagetool_server
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model

files_to_clean = [HEARTBEAT_FILE, PIDFILE, TRIGGER_FILE]
atexit.register(lambda: cleanup(logger, files_to_clean))
atexit.register(lambda: stop_languagetool_server(logger, languagetool_process))

with open(PIDFILE, 'w') as f:
    f.write(str(os.getpid()))

# --- Argument Parsing und Model-Setup ---
MODEL_NAME_DEFAULT = "vosk-model-de-0.21" # fallback

SCRIPT_DIR = Path(__file__).resolve().parent

""""
parser = argparse.ArgumentParser(description="A real-time dictation service using Vosk.")
parser.add_argument('--vosk_model', help=f"Name of the Vosk model folder. Defaults to '{MODEL_NAME_DEFAULT}'.")
parser.add_argument('--test-text', help="Bypass microphone and use this text for testing.")
args = parser.parse_args()
VOSK_MODEL_FILE = SCRIPT_DIR / "config/model_name.txt"
vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
MODEL_NAME = args.vosk_model or vosk_model_from_file or MODEL_NAME_DEFAULT

"""





TRIGGER_FILE.unlink(missing_ok=True)

# MODEL_PATH = SCRIPT_DIR / "models" / MODEL_NAME

import scripts.py.func.guess_lt_language_from_model

# LT_LANGUAGE = guess_lt_language_from_model(MODEL_NAME)




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

    logger.info(f"start_languagetool_server(logger, {jar_path_absolute}, {internal_lt_url})")
    languagetool_process = start_languagetool_server(logger, jar_path_absolute, internal_lt_url)
    if not languagetool_process: sys.exit(1)
    atexit.register(lambda: stop_languagetool_server(logger, languagetool_process))

    active_lt_url = f"http://localhost:{LANGUAGETOOL_PORT}/v2/check"





if not start_languagetool_server:
    notify("Vosk Startup Error", "LanguageTool Server failed to start.", "critical")
    sys.exit(1)

# --- mainlogic is in Thread ---



# --- Preload multiple models ---
loaded_models = {}

is_critical, avail_mb = check_memory_critical(CRITICAL_THRESHOLD_MB)
if is_critical:
    logger.critical(f"memory < --{CRITICAL_THRESHOLD_MB}-- ({avail_mb:.0f}MB available). Shutting down.")
    notify("Vosk: Critical Error", "Low memory detected. Service shutting down.", "critical")
    sys.exit(1)

else:
    # --- Model Pre-loading ---
    logger.info("--- Starting model pre-loading phase ---")
    loaded_models = {}

    is_critical, avail_mb = check_memory_critical(CRITICAL_THRESHOLD_MB)

    if is_critical:
        logger.critical(f"memory < --{CRITICAL_THRESHOLD_MB}-- ({avail_mb:.0f}MB available). ")
        logger.warning("Critical memory situation detected. Skipping model preloading.")
        notify("Vosk: Critical Error", "Low memory detected. Service shutting down.", "critical")
    else:
        logger.info(f"Attempting to preload models from settings: {PRELOAD_MODELS}")
        for model_name in PRELOAD_MODELS:
            model_path = SCRIPT_DIR / "models" / model_name
            if not model_path.exists():
                logger.warning(f"Model '{model_name}' not found at '{model_path}', skipping.")
                continue
            try:
                lang_key = model_name.split('-')[2]
                logger.info(f"Loading model '{model_name}' for language key '{lang_key}'...")
                model = vosk.Model(str(model_path))
                loaded_models[lang_key] = model
                logger.info(f"Successfully loaded '{model_name}'.")
            except Exception as e:
                logger.error(f"Could not load model '{model_name}': {e}", exc_info=True)


if not loaded_models:
    notify("Vosk Startup Error", "No models could be loaded. Check logs.", "critical")
    logger.fatal("FATAL: No models were loaded. Exiting.")
    sys.exit(1)

logger.info(f"Models loaded: {list(loaded_models.keys())}. Waiting for trigger.")
# notify("Vosk Ready", f"Models loaded: {', '.join(loaded_models.keys())}", icon="media-record")
notify("SL5 Dictation Ready", f"Models loaded: {', '.join(loaded_models.keys())}", icon="dialog-information")




# --- main-logic is in Thread ---

recording_time = 0
if __name__ == "__main__":
    config = {
        "TMP_DIR": TMP_DIR,
        "HEARTBEAT_FILE": HEARTBEAT_FILE,
        "PIDFILE": PIDFILE,
        "TRIGGER_FILE": TRIGGER_FILE,
        # REMOVED: LT_LANGUAGE is now determined dynamically inside main
        "CRITICAL_THRESHOLD_MB": CRITICAL_THRESHOLD_MB,
        "PROJECT_ROOT": PROJECT_ROOT
    }
    # MODIFIED: Pass the dictionary of loaded models to main
    main(logger, loaded_models, config, suspicious_events, TMP_DIR, recording_time, active_lt_url)



