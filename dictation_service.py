# File: dictation_service.py
import os
import sys, subprocess



# Python path to ensure reliable imports on all platforms
# This solves potential issues when running from a batch script on Windows


# ==============================================================================
# --- PREREQUISITE 1: VIRTUAL ENVIRONMENT CHECK ---
# The script MUST run inside its virtual environment to find dependencies.
# The 'VIRTUAL_ENV' variable is a standard indicator for an active venv.

if 'VIRTUAL_ENV' not in os.environ:
    print(
        "\nFATAL: Python virtual environment not activated!",
        file=sys.stderr
    )
    print(
        "       Please activate it first. On Linux/macOS, run:",
        file=sys.stderr
    )
    print("       source .venv/bin/activate", file=sys.stderr)
    print(
        "       Then, you can run the script: python dictation_service.py",
        file=sys.stderr
    )

    print("       Or (recommended) run:", file=sys.stderr)
    print(
        "       scripts/restart_venv_and_run-server.sh or run scripts/activate-venv_and_run-server.sh",
        file=sys.stderr
    )
    sys.exit(1)



# ==============================================================================






import sys, os, atexit, requests, logging, platform, importlib
from pathlib import Path

# --- Local Imports (grouped for clarity) ---
from config.settings import (LANGUAGETOOL_RELATIVE_PATH,
                            USE_EXTERNAL_LANGUAGETOOL, EXTERNAL_LANGUAGETOOL_URL, LANGUAGETOOL_PORT,
                            DEV_MODE,
                            ENABLE_AUTO_LANGUAGE_DETECTION,
                            AUTO_ENTER_AFTER_DICTATION
                            )


if ENABLE_AUTO_LANGUAGE_DETECTION:
    # Check if the package is installed without actually importing it
    if importlib.util.find_spec("fasttext") is None:
        logging.warning("FastText is not installed but is enabled in config.")
        logging.info("Attempting to install 'fasttext-wheel' automatically...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "fasttext-wheel"])
            logging.info("FastText installed successfully. Please restart the service to activate it.")
            sys.exit()
        except subprocess.CalledProcessError:
            logging.error("Failed to install FastText. Please install it manually: pip install fasttext-wheel")
            sys.exit(1)
    else:
        logging.info("FastText for auto language detection is available.")



from scripts.py.func.main import main
#from scripts.py.func.notify import notify
#from scripts.py.func.cleanup import cleanup
#from scripts.py.func.start_languagetool_server import start_languagetool_server
#from scripts.py.func.stop_languagetool_server import stop_languagetool_server
#from scripts.py.func.check_memory_critical import check_memory_critical
# We need vosk here for the model loading
# import vosk

from scripts.py.func.create_required_folders import setup_project_structure



# --- Constants and Paths ---
SCRIPT_DIR = Path(__file__).resolve().parent


PROJECT_ROOT = SCRIPT_DIR # In this structure, SCRIPT_DIR is PROJECT_ROOT


# ==============================================================================
# --- PRE-RUN SETUP VALIDATION ---

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# We add the 'scripts' directory to the path to import our custom validator.

# sys.path.append(os.path.join(SCRIPT_DIR, 'scripts'))

from scripts.py.func.checks.setup_validator import parse_all_files, validate_setup, check_for_unused_functions, check_for_frequent_calls

from scripts.py.func.checks.validate_punctuation_map_keys import validate_punctuation_map_keys

from scripts.py.func.checks.check_installer_sizes import check_installer_sizes

# from  scripts.py.func.checks.self_tester import run_core_logic_self_test





# File: STT/dictation_service.py
# ...
# --- Wrapper Script Check ---

    #sys.exit(1)

# ==============================================================================
# ==============================================================================
# ==============================================================================




setup_project_structure(PROJECT_ROOT)

if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
else:
    TMP_DIR = Path("/tmp")

TRIGGER_FILE = TMP_DIR / "sl5_record.trigger"
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

HEARTBEAT_FILE = TMP_DIR / "dictation_service.heartbeat"
PIDFILE = TMP_DIR / "dictation_service.pid"
LOG_FILE = Path("log/dictation_service.log")

SCRIPT_DIR = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"

languagetool_process = None


class WindowsEmojiFilter(logging.Filter):
    """
    A logging filter that replaces emojis with text placeholders on Windows.
    This prevents UnicodeEncodeError on older console environments.
    """
    def __init__(self):
        # Emojy resources: .venv/lib/python3.13/site-packages/rich/_emoji_codes.py
        super().__init__()
        self.replacements = {
            '⚠️': '[WARN]',
            '✅': '[OK]',
            '👍': '[OK]',
            '👎': '[NO]',
            '🎊': 'CONFETTI',
            '❌': '[FAIL]',
            '🎬': '[START]',
            '⏹️': '[STOP]',
            '🎤': '[MIC]',
            '🎙️': '[MIC]',
            '💾': '[▀▄▀]',
            '📋': '[EMPTY]',
            '🔳': '[NOTHING]',
            "👀": '[EYES]',
            '🚀': '[ROCKET]',
         '🔁':'REPLACE'
        }

    def filter(self, record):
        # Only perform replacement if running on Windows
        #if os.name == 'nt':
        if platform.system() == "Windows":
            for emoji, text in self.replacements.items():
                record.msg = record.msg.replace(emoji, text)
        return True




# --- Logging Setup ---
# Manual configuration for maximum robustness.

# 1. Get the root logger.
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 2. Clear any pre-existing handlers to prevent duplicates.
if logger.hasHandlers():
    logger.handlers.clear()

# 3. Create a shared formatter.
log_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')

# 4. Create, configure, and add the File Handler.
file_handler = logging.FileHandler(f'{SCRIPT_DIR}/log/dictation_service.log', mode='w')
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

# 5. Create, configure, and add the Console Handler.
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

# The filter is innocent, but we leave it out for now for the cleanest possible test.


logger.handlers[0].addFilter(WindowsEmojiFilter())



# Execute the check. The script will exit here if the setup is incomplete.
validate_setup(SCRIPT_DIR, logger)

if DEV_MODE :

    check_installer_sizes()


    from scripts.py.func.checks.check_badges import check_badges


    check_badges(SCRIPT_DIR)




    validate_punctuation_map_keys(SCRIPT_DIR,logger)

    project_root = SCRIPT_DIR
    parsed_trees = parse_all_files(project_root, logger)

    check_for_unused_functions(parsed_trees, project_root , logger)
    check_for_frequent_calls(parsed_trees, logger, threshold=1)

    check_installer_sizes()


if DEV_MODE :
    try:
        # Create a copy of the current environment and set PYTHONPATH
        env = os.environ.copy()
        env['PYTHONPATH'] = '.'

        subprocess.run(
            [sys.executable, "scripts/py/func/checks/test_dictation_session_logic.py"],
            check=True,
            cwd=SCRIPT_DIR,
            env=env
        )
        logger.info(">>> Core Logic Self-Test PASSED.")
    except subprocess.CalledProcessError:
        logger.critical(">>> Core Logic Self-Test FAILED. Aborting service start.")
        sys.exit(1)



# ==============================================================================
# --- Wrapper Script Check ---
# if not DEV_MODE and os.environ.get("DICTATION_SERVICE_STARTED_CORRECTLY") != "true":
#     logger.fatal("FATAL: This script must be started using the 'activate-venv_and_run-server.sh' wrapper.")
#     sys.exit(1)
# ==============================================================================



from scripts.py.func.notify import notify
from scripts.py.func.cleanup import cleanup
from scripts.py.func.start_languagetool_server import start_languagetool_server
# from scripts.py.func.stop_languagetool_server import stop_languagetool_server
# from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
# from scripts.py.func.check_memory_critical import check_memory_critical
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

# import scripts.py.func.guess_lt_language_from_model

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

from scripts.py.func.checks.check_all_maps_syntax import check_folder_syntax

check_folder_syntax(SCRIPT_DIR / 'config' ) # should also work for useer without git ... for normal users

if DEV_MODE :
    from scripts.py.func.checks.check_example_file_is_synced import check_example_file_is_synced
    check_example_file_is_synced(SCRIPT_DIR)

    from scripts.py.func.checks.validate_punctuation_map_keys import validate_punctuation_map_keys
    from scripts.py.func.checks.integrity_checker import check_code_integrity

    from scripts.py.func.checks.self_tester import run_core_logic_self_test


    check_code_integrity(SCRIPT_DIR, logger)

    check_installer_sizes()


    ##################### run_core_logic_self_test #############################
    VOSK_MODEL_FILE = SCRIPT_DIR / "config/model_name.txt"
    vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
    #MODEL_NAME = MODEL_NAME_DEFAULT

    lang_code = guess_lt_language_from_model(logger, vosk_model_from_file)
    run_core_logic_self_test(logger, TMP_DIR, active_lt_url,lang_code)
    #sys.exit(1)


# --- main-logic is in Thread ---

# File: dictation_service.py
global AUTO_ENTER_AFTER_DICTATION_global

recording_time = 0
from config import settings # Import the whole settings module
if __name__ == "__main__":
    # 1. Load all settings from the module into a dictionary
    config = {key: getattr(settings, key) for key in dir(settings) if key.isupper()}

    # 2. Add/overwrite dynamic, script-specific values
    config.update({
        "SCRIPT_DIR": SCRIPT_DIR,
        "TMP_DIR": TMP_DIR,
        "HEARTBEAT_FILE": HEARTBEAT_FILE,
        "PIDFILE": PIDFILE,
        "TRIGGER_FILE": TRIGGER_FILE,
        "PROJECT_ROOT": PROJECT_ROOT,
        "AUTO_ENTER_AFTER_DICTATION": AUTO_ENTER_AFTER_DICTATION
    })



    # --- Plugin State Communication ---
    # File: dictation_service.py Line 417
    # Create a flag file so client scripts know if a plugin is active.
    try:
        AUTO_ENTER_AFTER_DICTATION_global = AUTO_ENTER_AFTER_DICTATION
        auto_enter_flag_path = "/tmp/sl5_auto_enter.flag"
        with open(auto_enter_flag_path, "w") as f:
            f.write(str(AUTO_ENTER_AFTER_DICTATION_global)) # Writes 1 or 0
        logger.info(f"Set auto-enter flag to: {AUTO_ENTER_AFTER_DICTATION_global}")
    except Exception as e:
        logger.error(f"Could not write auto-enter flag file: {e}")



    # Pass the complete, unified config to main()
    loaded_models = {}
    main(logger, loaded_models, config, suspicious_events, recording_time, active_lt_url)

