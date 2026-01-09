# File: aura_engine.py
import objgraph
from datetime import datetime, timedelta

import os
import sys, subprocess

import signal


import psutil
import time, re


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
        "       Then, you can run the script: python aura_engine.py",
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



# aura_engine.py:59
from scripts.py.func.config.dynamic_settings import settings

# if settings.DEV_MODE :
#   ohhh. 16.12.'25 19:43 Tue i have forgot diesaber the log server. omg
#   from tools.simple_log_server import readme



from scripts.py.func.checks.check_settings_syntax import verify_plugin_notation
verify_plugin_notation(settings.PLUGINS_ENABLED)



if settings.ENABLE_AUTO_LANGUAGE_DETECTION:
    # Check if the package is installed without actually importing it
    if importlib.util.find_spec("fasttext") is None:
        logging.warning("FastText is not installed but is enabled in config.")
        logging.info("At    ting to install 'fasttext-wheel' automatically...")
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

    project_root = PROJECT_ROOT
    sys.path.append(str(project_root))

from config import settings







# We add the 'scripts' directory to the path to import our custom validator.

# sys.path.append(os.path.join(SCRIPT_DIR, 'scripts'))


from scripts.py.func.checks.validate_punctuation_map_keys import validate_punctuation_map_keys

from scripts.py.func.checks.check_installer_sizes import check_installer_sizes

from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2





# from  scripts.py.func.checks.self_tester import run_core_logic_self_test





# File: STT/aura_engine.py
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
HEARTBEAT_FILE = TMP_DIR / "aura_engine.heartbeat"
PIDFILE = TMP_DIR / "aura_engine.pid"
LOG_FILE = PROJECT_ROOT / "log" / "aura_engine.log"

LOCK_DIR = TMP_DIR / "sl5_aura" / "aura_lock"





PROJECT_ROOT = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = PROJECT_ROOT / settings.LANGUAGETOOL_RELATIVE_PATH


suspicious_events = []
if platform.system() == "Windows":
    TMP_DIR = Path("C:/tmp")
    NOTIFY_SEND_PATH = None
else:
    TMP_DIR = Path("/tmp")
OUTPUT_FILE = TMP_DIR / "tts_output.txt"

HEARTBEAT_FILE = TMP_DIR / "aura_engine.heartbeat"
PIDFILE = TMP_DIR / "aura_engine.pid"
LOG_FILE = Path("log/aura_engine.log")

SCRIPT_DIR = Path(__file__).resolve().parent
LANGUAGETOOL_JAR_PATH = f"{SCRIPT_DIR}/LanguageTool-6.6/languagetool-server.jar"

languagetool_process = None


logging.raiseExceptions = True

class WindowsEmojiFilter1(logging.Filter):
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
            '📢️': '[MIC]',
            '💾': '[SAVE]',
            '📋': '[EMPTY]',
            '🔳': '[NOTHING]',
            "👀": '[EYES]',
            '🚀': '[ROCKET]',
            '🔁':'REPLACE',
            '📚':'BOOK',
            '⌚': '[(-)]',  # clock
            '🗺️':'MAP',
            '🍒':'cherries'
        }

        # Fancy text symbols˗ˏˋ꒰ 🍒 ꒱ˏˋ°•*⁀ ༊*·˚⋆·˚ ༘ *・ ・ೃ⁀ ⇢ ˗ˏˋ*ೃ༄︶︶༉‧₊˚.♡ ༉‧₊˚ੈ ‧₊˚☄. *. ⋆: ̗̀ ...


    def filter(self, record):
        # Only perform replacement if running on Windows
        #if os.name == 'nt':
        if platform.system() == "Windows":
            for emoji, text in self.replacements.items():
                record.msg = record.msg.replace(emoji, text)
        return True

class WindowsEmojiFilter(logging.Filter):
    """
    A logging filter that replaces emojis with text placeholders on Windows.
    This prevents UnicodeEncodeError on older console environments.
    """

    def __init__(self):
        super().__init__()
        self.replacements = {
            '🚀': '[▲]',  # Rakete als Pfeil
            '🔁': '[⟳]',  # Loop als Kreispfeil
            '📚': '[▉]',  # Buch als gefülltes Rechteck
            '❌': '[■]',  # noqa: F601 Fehler als ausgefülltes Quadrat
            '⚠️': '[!]',  # Warnung
            '✅': '[✓]',  # OK, Haken
            '👍': '[OK]',
            '👎': '[NO]',
            '🎊': '[*]',  # Konfetti
            '❌': '[x]',  # noqa: F601 Fehler, ausgefülltes Quadrat
            '🎬': '[>]',  # Start, Play
            '⏹️': '[■]',  # Stop, Quadrat
            '🏁': '[>]',  # Start
            '🎤': '[◉]',  # Mikrofon
            '🎙️': '[▣]',  # Studio-Mikrofon, gefüllter Kreis
            '📢️': '[≡]',  # Lautsprecher (Klangwellen)
            '💾': '[¥]',  # Diskette/Save, ausgefülltes Quadrat mit Rand
            '📋': '[‗]',  # Zwischenablage, Unterstrich/Leiste
            '🔳': '[□]',  # Nichts, leeres Quadrat
            "👀": '[o_o]',  # Augen
            '🚀': '[▲]',  # Rakete, Pfeil hoch
            '🔁': '[⟳]',  # Wiederholen, Kreispfeil
            '📚': '[▉]',  # Buch, gefülltes Rechteck
            '⌚': '[(-)]',  # clock
            '🗺️':'▀▄▀'
        # ▣▣■
                 #                 '🚀': '[>>>]',
        }

    def filter(self, record):
        # Only perform replacement if running on Windows
        #if os.name == 'nt':
        if platform.system() == "Windows":
            for emoji, text in self.replacements.items():
                record.msg = record.msg.replace(emoji, text)
        return True



# aura_engine.py:268

logger = logging.getLogger()



# class PrintToConsoleAndFile(object):
#     def __init__(self, logger):
#         self.logger = logger
#         self.terminal = sys.__stdout__ # Das echte Terminal sichern
#
#     def write(self, buf):
#         # 1. Sofort auf die Konsole schreiben (Garantie!)
#         self.terminal.write(buf)
#         self.terminal.flush()
#
#         # 2. Danach ins Logfile senden
#         if buf.strip():
#             try:
#                 # Hier nutzen wir den Logger nur fürs File
#                 # (Falls der ConsoleHandler noch aktiv ist, könnte es doppelt kommen,
#                 # aber besser doppelt als gar nicht)
#                 self.logger.info(buf.rstrip())
#             except:
#                 pass
#
#     def flush(self):
#         self.terminal.flush()




class SafeStreamToLogger(object):
    def __init__(self, logger, original_stream, file_handler):
        self.logger = logger
        self.terminal = original_stream
        self.file_handler_ref = file_handler               # <--- HIER speichern
        self.is_logging = False # <--- DER SCHUTZSCHALTER
        self.log_pattern = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3}\s-\s[A-Z]+\s+-\s')

    def write(self, buf):
        # 1. Immer sofort auf die Konsole schreiben (für dich sichtbar)
        self.terminal.write(buf)
        # self.terminal.flush() <-- BESSER SO (Spart CPU/Zeit)

        # 2. Wenn wir gerade NICHT loggen, dann ins File senden
        # if not self.is_logging and buf.strip():
        if buf and not buf.isspace() and not self.is_logging:
            self.is_logging = True # Schalter an
            try:
                # Prüfen: Hat der Text schon einen Zeitstempel?
                match = self.log_pattern.match(buf)

                if match:
                    # JA: Wir schneiden den Zeitstempel vorne weg!
                    # match.end() ist die Stelle, wo der echte Text anfängt.
                    clean_msg = buf[match.end():].rstrip()
                else:
                    # NEIN: Wir nehmen den Text so wie er ist (z.B. von print)
                    clean_msg = buf.rstrip()

                # Nur schreiben, wenn noch Text übrig ist
                if clean_msg:
                    record = logging.LogRecord(
                        name="PRINT", level=logging.INFO, pathname="print", lineno=0,
                        msg=clean_msg, args=(), exc_info=None
                    )
                    self.file_handler_ref.handle(record)

            except Exception:
                pass
            finally:
                self.is_logging = False

    def flush(self):
        # self.terminal.flush() # entfernen spart viel Zeit. Erfüllt die Pflicht
        pass

# sys.stdout = SafeStreamToLogger(logger, sys.__stdout__)






# Aktivieren
# sys.stdout = PrintToConsoleAndFile(logger)




# sys.stdout = StreamToLogger(logger, logging.INFO) # print -> Logger
# sys.stderr = StreamToLogger(logger, logging.ERROR) # Fehler -> Logger



# 304
logger.setLevel(logging.INFO)

# Clear any pre-existing handlers to prevent duplicates.
if len(logger.handlers) > 0:
    logger.handlers.clear()

# Create a shared formatter with the custom formatTime function.
def formatTime(record, datefmt=None):
    time_str = time.strftime("%H:%M:%S")
    milliseconds = int((record.created - int(record.created)) * 1000)
    ms_str = f",{milliseconds:03d}"
    return time_str + ms_str


# 1. Wir erstellen eine Filter-Klasse
class DittoFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.last_msg = None

    def filter(self, record):
        # Den "echten" Inhalt der aktuellen Nachricht holen
        current_msg = record.getMessage()

        # Vergleich mit der gespeicherten Original-Nachricht
        if current_msg == self.last_msg:
            # Es ist eine Wiederholung -> Text für die Ausgabe ändern
            record.msg = "〃"
            record.args = ()

            # WICHTIG: Wir aktualisieren self.last_msg HIER NICHT.
            # Wir wollen, dass die nächste Zeile sich immer noch mit
            # dem Original (z.B. "Verbindung...") vergleicht und
            # nicht mit dem Gänsefüßchen ("〃").
        else:
            # Es ist eine neue Nachricht -> Speicher aktualisieren
            self.last_msg = current_msg

        return True


# Filter instanziieren
ditto_filter = DittoFilter()



log_formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
log_formatter.formatTime = formatTime

# Create, configure, and add the File Handler.



class FlushingFileHandler(logging.FileHandler):
    def emit(self, record):
        try:
            super().emit(record)
            self.flush() # Zwingt den Inhalt sofort auf die Platte
        except Exception:
            self.handleError(record)






# file_handler = logging.FileHandler(f'{SCRIPT_DIR}/log/aura_engine.log', mode='a', encoding='utf-8')
# Nutzen Sie diesen neuen Handler
file_handler = FlushingFileHandler(
    f'{SCRIPT_DIR}/log/aura_engine.log',
    mode='a',
    encoding='utf-8'
)


file_handler.setFormatter(log_formatter)

# logger.addFilter(ditto_filter)


sys.stdout = SafeStreamToLogger(logger, sys.__stdout__, file_handler)



# Create, configure, and add the Console Handler.
console_handler = logging.StreamHandler(sys.stdout)
#console_handler = logging.StreamHandler(sys.__stdout__)

console_handler.setFormatter(log_formatter)
#console_handler.addFilter(ditto_filter)




# Add the WindowsEmojiFilter to the file_handler
if True:

    logger.addFilter(ditto_filter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # logger.addHandler(console_handler)
    # logger.addFilter(WindowsEmojiFilter())
    # logger.addFilter(ditto_filter)
else:
    logger.addHandler(file_handler)

    console_handler.addFilter(WindowsEmojiFilter())
    console_handler.addFilter(ditto_filter)
    file_handler.addFilter(WindowsEmojiFilter())
    file_handler.addFilter(ditto_filter)

# file_handler.addFilter(WindowsEmojiFilter())
# file_handler.addFilter(ditto_filter)






















DISABLE_ALL_TEST_BECAUSE_WORKING_ON_ZIP_PACK_UNPACK_TEST = False
# DISABLE_ALL_TEST_BECAUSE_WORKING_ON_ZIP_PACK_UNPACK_TEST = True

readme = """
vosk-model-small-de-0.15
17:36:26,230 - INFO     - >>> Core Logic Self-Test PASSED.
17:36:36,138 - INFO     - ==    ✅ MODEL READY: 'small'.
==> 10 Seconds Sekunden

vosk-model-de-0.21
    ✅ MODEL READY: 'de'.
13:27:52,772 - INFO     - >>> Core Logic Self-Test PASSED.
13:29:09,816 - INFO     - self_tester.py:216 ✅  89tested of 98 tests (lang=de-DE)
==> ~70 Seconds Sekunden


"""


if settings.SERVICE_START_OPTION ==1:
    # Option 1: Start the service only on autostart (start parameter) and if there is an internet

    def check_internet_connection(host='https://sl5.de'):
        if os.getenv('CI'):
            logger.info("CI environment detected. Skipping microphone-dependent recording.")
            return True  # Pretend internet is available for CI

        if host.startswith(('http://', 'https://')):
            host = host.split('//')[1]
        # Use 'ping -n 1' on Windows and 'ping -c 1' on other OS
        # The '-n 1' and '-c 1' options specify the number of echo requests to send
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        try:
            # The subprocess.run function executes the ping command
            # It waits for the command to complete and returns a CompletedProcess object
            subprocess.run(
                ['ping', param, '1', host],
                check=True,  # This will raise a CalledProcessError if the command fails
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Internet connection is available. Successfully pinged {host}.")
            return True
        except subprocess.CalledProcessError:
            print(f"No internet connection. Failed to ping {host}.")
            return False
        except FileNotFoundError:
            print("The 'ping' command was not found. Please ensure it's in your system's PATH.")
            return False

    if not check_internet_connection():
        m = "Service will not start due to no internet connection."
        print(m)
        logging.info(m)
        sys.exit()


# Execute the check. The script will exit here if the setup is incomplete.

if settings.DEV_MODE :





    validate_punctuation_map_keys(SCRIPT_DIR,logger)

    project_root = SCRIPT_DIR


if settings.DEV_MODE :
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
from scripts.py.func.start_languagetool_server import start_languagetool_server, LT_ALREADY_RUNNING_SENTINEL
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

import threading

"""
31.10.'25 22:09 Fri
22:07:36,080 - INFO     - Graceful shutdown initiated. Final timeout set to 2.0s.
22:07:36,484 - WARNING  - SYSTEM-MEMORY CRITICAL! Usage: 92.00440896261489%. Exceeds threshold. Terminating entire process group 82694.BTW: ramUsageIncreadFromBegining: 1.0818119049072266 times
"""


SYSTEM_RAM_THRESHOLD_PERCENT = 92.0
SYSTEM_SWAP_THRESHOLD_PERCENT = 85.0 # this is deprecated. idk. seems not working like expected. dont use it.

RAM_ESTIMATE_PER_MODEL_GB = 4.0 # plus some other needed space for the model
GB_TO_MB_CONVERSION_FACTOR = 1024

# aura_engine.py:404























# --- SETUP FOR DEDICATED MEMORY LOGGING ---
# Define the path for the memory log file
MEMORY_LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log/memory_leak_analysis.log')

# Initialize a dedicated logger for memory events
memory_logger = logging.getLogger('MemoryAnalyzer')



# Fügen Sie dies vor der Konfiguration des memory_logger hinzu:

# aura_engine.py:708
if os.path.exists(MEMORY_LOG_PATH):
    # Get last modification time
    mtime_ts = os.path.getmtime(MEMORY_LOG_PATH)
    log_date = datetime.fromtimestamp(mtime_ts).date()
    # If the log file is not from today, delete it
    if log_date < datetime.now().date():
        # os.remove(MEMORY_LOG_PATH)
        try:
            if os.path.exists(MEMORY_LOG_PATH):
                # Truncate the file instead of removing it to avoid WinError 32
                with open(MEMORY_LOG_PATH, 'w'):
                    pass
        except PermissionError:
            logger.warning(f"Could not clear {MEMORY_LOG_PATH} - file is locked. May Ctrl+Alt+Def and delete alle Python processes")
            logger.warning('Prüfe im Task-Manager, ob noch eine alte python.exe im Hintergrund läuft, die die Logdatei blockiert.')




        memory_logger.info("Old memory log file deleted.")







# Ensure the logger hasn't already been configured by accident (common in Python)
if not memory_logger.handlers:
    memory_logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(MEMORY_LOG_PATH)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    memory_logger.addHandler(file_handler)
    # Prevent propagation to the root logger which might write to stdout/stderr
    memory_logger.propagate = False


def memory_leak_analyzer(interval_seconds=600, significant_growth_threshold=100):
    """
    Periodically logs the growth of the largest Python objects to a dedicated file
    to diagnose memory leaks. Runs indefinitely as a daemon thread.
    """
    memory_logger.info("logger.info('Memory Leak Analyzer started. Initializing object counts.')")

    process = psutil.Process(os.getpid())
    current_memory_mb = process.memory_info().rss / (1024 * 1024)

    memory_logger.info(f"System Process Memory (RSS): {current_memory_mb:.2f} MB")

    # Store initial counts of all objects to track growth accurately
    try:
        initial_counts = objgraph.most_common_types(limit=None, shortnames=False)
        initial_dict = {item[0]: item[1] for item in initial_counts}
    except Exception as e1:
        memory_logger.error(f"logger.info('Failed to get initial object counts: {e1}')")
        return  # Stop if initial check fails

    memory_logger.info(
        f"logger.info('Analysis interval set to {interval_seconds} seconds. Growth threshold: {significant_growth_threshold} objects.')")

    while True:
        try:
            time.sleep(interval_seconds)

            # 1. Get current process memory usage (as reported by OS)
            process = psutil.Process(os.getpid())
            current_memory_mb = process.memory_info().rss / (1024 * 1024)

            # 2. Get current Python object counts (top 30 to catch most issues)
            current_counts = objgraph.most_common_types(limit=30, shortnames=False)

            memory_logger.info("--- MEMORY SNAPSHOT ---")
            memory_logger.info(f"System Process Memory (RSS): {current_memory_mb:.2f} MB")

            # 3. Compare current counts to initial and log significant growth
            growth_found = False
            for type_name, count in current_counts:
                initial_count = initial_dict.get(type_name, 0)
                count_increase = count - initial_count

                # Only log objects that have grown significantly
                if count_increase > significant_growth_threshold:
                    memory_logger.info(
                        f"GROWTH DETECTED: {type_name}: Current={count} | Growth={count_increase}")
                    growth_found = True

            if not growth_found:
                memory_logger.info("logger.info('No significant object growth detected in top 30 types.')")
            memory_logger.info("---------------------")

        except Exception as e2:
            memory_logger.error(f"Analyzer loop encountered an error: {e2}")
            time.sleep(60)  # Short pause before continuing the loop


# --- INTEGRATION STEP ---
# This line must be added to your main application startup sequence (e.g., main.py or similar):

# To run it in parallel (similar to your existing watchdog):
if settings.DEV_MODE:
    threading.Thread(target=memory_leak_analyzer, daemon=True).start()



























def system_memory_watchdog(logging):

    logging.info(f"System Memory 👀 Watchdog started. Threshold: {SYSTEM_RAM_THRESHOLD_PERCENT}%")

    process = psutil.Process(os.getpid())

    num_preloaded_models = len(settings.PRELOAD_MODELS)

    #estimated_total_size_mb = file_size_bytes / (1024 * 1024)
    estimated_ram_for_models_mb = num_preloaded_models * RAM_ESTIMATE_PER_MODEL_GB * GB_TO_MB_CONVERSION_FACTOR

    # Cross-platform call - use getpgrp only on non-Windows systems
    import sys
    my_pgid = None
    if not sys.platform.startswith('win'):
        try:
            my_pgid = os.getpgrp()
            logging.info(f"System Memory 👀 Watchdog is running on Unix-like system with pgid: {my_pgid}")
        except AttributeError:
            # Fallback in case os.getpgrp is still missing for some reason
            pass




    if True:
        # 2. Get Swap Memory just for information
        swap_info = psutil.swap_memory()
        current_swap_percent = swap_info.percent

        ram_info = psutil.virtual_memory()
        current_ram_percent = ((ram_info.total - ram_info.available) / ram_info.total) * 100

        log_msg = (
            f"SYSTEM-MEMORY Usage: {current_ram_percent:.1f}% (>{SYSTEM_RAM_THRESHOLD_PERCENT}%) "
            f"current_swap_percent: {current_swap_percent:.1f}% (>{SYSTEM_SWAP_THRESHOLD_PERCENT}%). "
        )


    while True:
        # get the real RAM-usages
        # current_memory_percent = psutil.virtual_memory().percent

        # 1. Get Physical RAM
        ram_info = psutil.virtual_memory()
        current_ram_percent = ((ram_info.total - ram_info.available) / ram_info.total) * 100

        # 2. Get Swap Memory
        # swap_info = psutil.swap_memory()
        # current_swap_percent = swap_info.percent

        # current_swap_percent seems not working in my tests sadly

        # and current_swap_percent > SYSTEM_SWAP_THRESHOLD_PERCENT
        if current_ram_percent > SYSTEM_RAM_THRESHOLD_PERCENT:

            # Create a detailed log message that shows WHY the shutdown is happening
            log_msg = (
                f"SYSTEM-MEMORY CRITICAL! RAM Usage: {current_ram_percent:.1f}% (>{SYSTEM_RAM_THRESHOLD_PERCENT}%) "
                # f"AND Swap Usage: {current_swap_percent:.1f}% (>{SYSTEM_SWAP_THRESHOLD_PERCENT}%). "
            )
            logging.warning(log_msg)

            ram_occupied_by_this_specific_process_mb =  process.memory_info().rss / (1024 * 1024)
            ramUsageIncreadFromBegining = ram_occupied_by_this_specific_process_mb / estimated_ram_for_models_mb
            if ram_occupied_by_this_specific_process_mb >= 1.3 * estimated_ram_for_models_mb: # 1.2 or higher is maybe a good value
                logging.error(
                    f"memoryLECK! "
                    f"Process-RAM {estimated_ram_for_models_mb:.2f} MB now {ram_occupied_by_this_specific_process_mb:.2f} MB")

                script_name = None
                if sys.platform.startswith('win'):
                    script_name = 'restart_venv_and_run-server.ahk'
                elif sys.platform in ["linux", "darwin"]:
                    script_name = 'restart_venv_and_run-server.sh'
                else:
                    logging.warning(f"restart for '{sys.platform}' not suported.")

                if script_name:
                    restart_script_path=''
                    try:
                        restart_script_path = os.path.join(PROJECT_ROOT, 'scripts', script_name)
                        logging.info(f"restart in '{sys.platform}' using  {restart_script_path}")
                        subprocess.Popen([restart_script_path], shell=True) # shell=True ist für Windows sicherer
                        logging.info("Prozess will end, hope it helps restarting.")
                        sys.exit(0)

                    except FileNotFoundError:
                        logging.error(f"restart-Skript not found: {restart_script_path}")
                    except Exception as e:
                        logging.error(f"error when try restart: {e}")





            logging.warning(
                f"SYSTEM-MEMORY CRITICAL! Usage: {current_ram_percent}%. "
                f"ram_occupied_by_this_specific_process_mb: {ram_occupied_by_this_specific_process_mb}%. "
                f"Exceeds threshold. Terminating entire process group {my_pgid}."
                f"BTW: ramUsageIncreadFromBegining: {ramUsageIncreadFromBegining} times"


            )
            try:
                os.killpg(my_pgid, signal.SIGKILL)
            except ProcessLookupError:
                pass

        time.sleep(2)


watchdog_thread = threading.Thread(target=system_memory_watchdog, args=(logger,), daemon=True)
watchdog_thread.start()









TRIGGER_FILE.unlink(missing_ok=True)

# MODEL_PATH = SCRIPT_DIR / "models" / MODEL_NAME

# import scripts.py.func.guess_lt_language_from_model

# LT_LANGUAGE = guess_lt_language_from_model(MODEL_NAME)




active_lt_url = None

if settings.USE_EXTERNAL_LANGUAGETOOL:
    logger.warning(f"USING EXTERNAL LT SERVER: {settings.EXTERNAL_LANGUAGETOOL_URL}. AT YOUR OWN RISK.")
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # PING-TEST:
    try:
        requests.get(f"{active_lt_url}/v2/languages", timeout=3)
        logger.info("External LanguageTool server is responsive.")
    except requests.exceptions.RequestException:
        logger.fatal("External LanguageTool server did not respond. Is it running?")
        sys.exit(1)
else:
    PROJECT_ROOT = Path(__file__).resolve().parent
    jar_path_absolute = PROJECT_ROOT / settings.LANGUAGETOOL_RELATIVE_PATH
    internal_lt_url = f"http://localhost:{settings.LANGUAGETOOL_PORT}"

    logger.info(f"start_languagetool_server(.. {str(jar_path_absolute)[-30:0]}, {internal_lt_url})")

    # aura_engine.py:751
    languagetool_process = start_languagetool_server(logger, jar_path_absolute, internal_lt_url)

    # NEU/CHANGE: Register atexit ONLY if a real process was started
    if languagetool_process and languagetool_process is not LT_ALREADY_RUNNING_SENTINEL:
        atexit.register(lambda: stop_languagetool_server(logger, languagetool_process))

    # if not languagetool_process: sys.exit(1)
    # atexit.register(lambda: stop_languagetool_server(logger, languagetool_process))

    # aura_engine.py:760
    active_lt_url = f"http://localhost:{settings.LANGUAGETOOL_PORT}/v2/check"


if not languagetool_process:
    notify("Vosk Startup Error", "LanguageTool Server failed to start.", "critical")
    sys.exit(1)


if settings.DEV_MODE :

    from scripts.py.func.checks.check_all_maps_syntax import check_folder_syntax
    from scripts.py.func.log_memory_details import log_memory_details,log4DEV

    check_folder_syntax(SCRIPT_DIR / 'config' ) # should also work for useer without git ... for normal users


    run_e2e_live_reload_func_test_v2(logger, active_lt_url)

    log4DEV('Script Start', logger)


    log_memory_details("Script Start", logger)



    from scripts.py.func.checks.check_example_file_is_synced import check_example_file_is_synced
    # i call it two times because i removed the exit command when error today (2.10.'25 Thu). it's not critical but should not forget

    ##################### run_core_logic_self_test #############################
    VOSK_MODEL_FILE = SCRIPT_DIR / "config/model_name.txt"
    vosk_model_from_file = Path(VOSK_MODEL_FILE).read_text().strip() if Path(VOSK_MODEL_FILE).exists() else ""
    #MODEL_NAME = MODEL_NAME_DEFAULT

    lang_code = guess_lt_language_from_model(logger, vosk_model_from_file)

    from scripts.py.func.checks.self_tester import run_core_logic_self_test

    if not DISABLE_ALL_TEST_BECAUSE_WORKING_ON_ZIP_PACK_UNPACK_TEST:
        self_test_start_time = time.time()
        log4DEV(f"Start run_core_logic_self_test( .. {lang_code}", logger)
        run_core_logic_self_test(logger, TMP_DIR, active_lt_url,lang_code)


        self_test_end_time = time.time()
        self_test_duration = self_test_end_time - self_test_start_time
        self_test_readable_duration = timedelta(seconds=self_test_duration)
        logger.info(f"⌚ self_test_readable_duration: {self_test_readable_duration}")

        logSnippet = """
        without checks and clean all cashes before. it seems service can start in about 23 Seconds with a good german Model (s,25.11.'25 00:04 Tue)
        23:59:57,438 - INFO     - DEV_MODE: Running punctuation map key validation...
        00:00:20,233 - INFO     - ==    ✅ MODEL READY: 'de'.

        without checks it seems service can start in about 27 Seconds with a good german Model (s,24.11.'25 15:16 Mon):
        15:12:19,851 - INFO     - DEV_MODE: Running punctuation map key validation...
        15:12:46,853 - INFO     - ==    ✅ MODEL READY: 'de'.

        """


        """
        # self_test_readable_duration
        59 of 82 tests ❌ FAILed.    seconds=5, microseconds=578883

        """

        check_installer_sizes()


        from scripts.py.func.checks.check_badges import check_badges


        check_badges(SCRIPT_DIR)


        from scripts.py.func.checks.setup_validator import parse_all_files, validate_setup, check_for_unused_functions, check_for_frequent_calls

        validate_setup(SCRIPT_DIR, logger)


        PROJECT_ROOT = SCRIPT_DIR  # In this structure, SCRIPT_DIR is PROJECT_ROOT

        parsed_trees = parse_all_files(PROJECT_ROOT, logger)

    if not DISABLE_ALL_TEST_BECAUSE_WORKING_ON_ZIP_PACK_UNPACK_TEST:
        check_for_unused_functions(parsed_trees, PROJECT_ROOT , logger)
        check_for_frequent_calls(parsed_trees, logger, threshold=1)

        check_installer_sizes()


        check_example_file_is_synced(SCRIPT_DIR)

        from scripts.py.func.checks.validate_punctuation_map_keys import validate_punctuation_map_keys
        from scripts.py.func.checks.integrity_checker import check_code_integrity

        check_code_integrity(SCRIPT_DIR, logger)

        check_installer_sizes()


        # i call it two times because i removed the exit command when error today (2.10.'25 Thu). it's not critical but should not forget
        check_example_file_is_synced(SCRIPT_DIR)



# --- main-logic is in Thread ---

# File: aura_engine.py
global AUTO_ENTER_AFTER_DICTATION_global

recording_time = 0
# from config import settings # Import the whole settings module
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
        "AUTO_ENTER_AFTER_DICTATION_REGEX_APPS": settings.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS,
        "languagetool_process": active_lt_url
    })



    # --- Plugin State Communication ---
    # File: aura_engine.py Line 417
    # Create a flag file so client scripts know if a plugin is active.
    try:
        AUTO_ENTER_AFTER_DICTATION_global = settings.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
        auto_enter_flag_path = "/tmp/sl5_auto_enter.flag"
        with open(auto_enter_flag_path, "w") as f:
            f.write(str(AUTO_ENTER_AFTER_DICTATION_global)) # Writes 1 or 0
        logger.info(f"Set auto-enter flag to: {AUTO_ENTER_AFTER_DICTATION_global}")
    except Exception as e:
        logger.error(f"Could not write auto-enter flag file: {e}")



    # Pass the complete, unified config to main()
    loaded_models = {}
    main(logger, loaded_models, config, suspicious_events, recording_time, active_lt_url)


