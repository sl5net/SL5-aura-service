# file: config/settings.py
# Central configuration for the application

# --- Notification Settings ---
# Default for new users is the most verbose level.
NOTIFICATION_LEVEL = 2 # 0=Silent, 1=Essential, 2=Verbose

# Try to import user-specific overrides
try:
    from .settings_local import *
    print("Loaded local config overrides.")
except ImportError:
    pass # No local config found, using defaults.

# --- Language Model Preloading ---
# A list of Vosk model folder names to preload at startup if memory allows.
PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]
# PRELOAD_MODELS = ["vosk-model-de-0.21"]

# --- LanguageTool Server ---
# Set to True to use an existing LT server. AT YOUR OWN RISK!
# The application will not start its own server and will not stop the external one.
USE_EXTERNAL_LANGUAGETOOL = False # Default: False

# URL for the external server if the option above is True.
EXTERNAL_LANGUAGETOOL_URL = "http://localhost:8081"

# Settings for our internal server (if used)
LANGUAGETOOL_PORT = 8082

# Recording & Transcription
SUSPICIOUS_TIME_WINDOW = 90
SUSPICIOUS_THRESHOLD = 3

SILENCE_TIMEOUT = 0.4
PRE_RECORDING_TIMEOUT = 12

SAMPLE_RATE = 16000

# System
CRITICAL_THRESHOLD_MB = 1024

# LanguageTool Server Configuration
LANGUAGETOOL_BASE_URL = f"http://localhost:{LANGUAGETOOL_PORT}"
LANGUAGETOOL_CHECK_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
LANGUAGETOOL_RELATIVE_PATH = "LanguageTool-6.6/languagetool-server.jar"

NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"


