# file: config/settings.py
# Central configuration for the application

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
SILENCE_TIMEOUT = 5

SILENCE_TIMEOUT2 = 0.4

# System
CRITICAL_THRESHOLD_MB = 1024

# LanguageTool Server Configuration
LANGUAGETOOL_BASE_URL = f"http://localhost:{LANGUAGETOOL_PORT}"
LANGUAGETOOL_CHECK_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
LANGUAGETOOL_RELATIVE_PATH = "LanguageTool-6.6/languagetool-server.jar"

NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"


