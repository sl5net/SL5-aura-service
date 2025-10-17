# file: config/settings.py
# Central configuration for the application
# please see also: settings_local.py_Example.txt
import os

SERVICE_START_OPTION = 0
# Option 1: Start the service only on when there is an internet connection.

# Get username
current_user = os.environ.get('USERNAME', 'default')

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
DEV_MODE = False

soundMute = 1  # 1 is really recommandet. to know when your recording is ended.
soundUnMute = 1
soundProgramLoaded = 1

ENABLE_AUTO_LANGUAGE_DETECTION = False # Deprecated . Better set it to False

# --- Notification Settings ---
# Default for new users is the most verbose level.
NOTIFICATION_LEVEL = 0 # 0=Silent, 1=Essential, 2=Verbose

# --- Language Model Preloading ---
# A list of Vosk model folder names to preload at startup if memory allows.
# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]
PRELOAD_MODELS = ["vosk-model-de-0.21"]

if current_user == 'SL5.de':
    PRELOAD_MODELS = ["vosk-model-de-0.21"]


# --- LanguageTool Server ---
# Set to True to use an existing LT server. AT YOUR OWN RISK!
# The application will not start its own server and will not stop the external one.
USE_EXTERNAL_LANGUAGETOOL = False # Default: False

# URL for the external server if the option above is True.
EXTERNAL_LANGUAGETOOL_URL = "http://localhost:8081"

# Settings for our internal server (if used)
LANGUAGETOOL_PORT = 8082

# --- Text Correction Settings ---
# This dictionary controls which categories of LanguageTool rules are enabled.
# The application will use these settings to enable/disable rule categories
# when checking text. Set a category to False to ignore its suggestions.
#
# You can override these in your config/settings_local.py file.
CORRECTIONS_ENABLED = {
    # Core Corrections
    "spelling": True,          # Basic spell checking (e.g., "Rechtschreibung")
    "punctuation": True,       # Missing/incorrect commas, periods, etc.
    "grammar": True,           # Grammatical errors (e.g., subject-verb agreement)
    "casing": True,            # Incorrect capitalization (e.g., "berlin" -> "Berlin")
    "style": True,             # Stylistic suggestions (e.g., wordiness, passive voice)
    "colloquialisms": True,    # Flags informal or colloquial language

    # Specialized Dictionaries/Rules
    # These are disabled by default as they may not be relevant for all users.
    # Set to True in settings_local.py to enable them.
    "medical": False,          # Rules related to medical terminology
    "law_rules": False,        # Rules related to legal terminology

    "git": False,        # git Basic commands

    # Add other custom categories here as needed.
    # "academic_writing": False,
}


default_mode_is_all = True
#  1 zwei drei vier 5
#

PLUGINS_ENABLED = {}

# needs restart. implemented in the python part:
ADD_TO_SENCTENCE = "."
# set ADD_TO_SENCTENCE = "" when you dont want it.


# Recording & Transcription
SUSPICIOUS_TIME_WINDOW = 90
SUSPICIOUS_THRESHOLD = 3

# INITIAL_WAIT_TIMEOUT = initial_silence_timeout
# SPEECH_PAUSE_TIMEOUT = 2.0 # Standardwert

PRE_RECORDING_TIMEOUT = 12
SPEECH_PAUSE_TIMEOUT = 0.6


SAMPLE_RATE = 16000

# System
CRITICAL_THRESHOLD_MB = 1024 * 2

# LanguageTool Server Configuration
LANGUAGETOOL_BASE_URL = f"http://localhost:{LANGUAGETOOL_PORT}"
LANGUAGETOOL_CHECK_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
LANGUAGETOOL_RELATIVE_PATH = "LanguageTool-6.6/languagetool-server.jar"

NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"

TRIGGER_FILE_PATH = "/tmp/sl5_record.trigger"

# Auto-detected Java path
JAVA_EXECUTABLE_PATH = r"/usr/bin/java"

# needs NO restart. implemented in the sh part. TODO implemt for windows:
# use . for all Windows. Other examples:
# AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "."
AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "(ExampleAplicationThatNotExist|Pi, your personal AI)"
# TODO implement for windows
