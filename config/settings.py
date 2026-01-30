
# config/settings.py
# Central configuration for the application
# please see also: settings_local.py_Example.txt
from scripts.py.func.determine_current_user import determine_current_user

SERVICE_START_OPTION = 0
# Option 1: Start the service only on when there is an internet connection.

current_user,_ = determine_current_user()
print(f'hi, hallo, welcome: {current_user}')
current_user = user_name = USER_NAME = str(current_user) # fallbacks
# logger.info("Current user successfully determined in a cross-platform manner.") # Add logger import if needed

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
DEV_MODE = False
DEV_MODE_all_processing = False

soundMute = 1  # 1 is really recommended. to know when your recording is ended.
soundUnMute = 1
soundProgramLoaded = 1

ENABLE_AUTO_LANGUAGE_DETECTION = False # Deprecated . Better set it to False

# --- Notification Settings ---
# Default for new users is the most verbose level.
NOTIFICATION_LEVEL = 0 # 0=Silent, 1=Essential, 2=Verbose


SIGNATURE_COOLDOWN = 50 # 600

# 🗣️🌐 (symbols and icons are probably cut out later by )
# sometimes e.g.in twitch: gelöscht: Nightbot: @seeh74 -> Sorry, you can't post links without permission!
#🗣ടㄴ⠄de╱Aura SL5.de/Aura
signatur=' #FreedomLadder #FreeSoftware #FSF #SL5Aura SL5.de/Aura'

# signatur='🗣SL5net ⟫ Aura'
# signatur='🗣[ SL5net Aura ]'
# signatur='🗣SL5net Aura'
# signatur='🗣ടㄴ5⠄de╱Aura'
# signatur='🗣Sㄴ5⠄de╱Aura' # this l is unvisable in gemini
#signatur='🗣SL5⠄de╱Aura'
# signatur='🗣SL5⠠de╱Aura' # i like this 11.11.'25 09:58 Tue
#now (original:'jetzt', ).
#signatur=',🗣SL5。de╱Aura' # i like this 11.11.'25 09:58 Tue
signatur=''
signatur='🗣SL5net ⟫ Aura'
signatur1=f'{signatur}' # (Powered by

LANGUAGE_PREFIXES = {
    "pt-br": "Tradução de Voz",
    "en": "Voice Translation",
    "ar": "تحدثت الترجمة",
    "ja": "話し言葉の翻訳",
    "de": "Sprachübersetzung",
    "DEFAULT": "" # Fallback
}




# Format: { "Regex-Pattern": ( "Signatur-Text", Cooldown_in_Sekunden ) }
SIGNATURE_MAPPING = {
    r"0 a\.d\.": ("SL5net >> Aura", 14400),        # 4 Stunden für Spiele
    r"Matrix|Discord": ("🗣SL5net ⟫ Aura", 3600),   # 1 Stunde für Chat
    r"Outlook|Mail": ("-- Sent via Aura --", 86400), # 1 Tag für E-Mails
    "Konsole|kate": ("", 86400),
    r".*": ("🗣[ SL5net Aura ]", 1800)             # 30 Min Fallback
}


# --- Language Model Preloading ---
# A list of Vosk model folder names to preload at startup if memory allows.
# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]
PRELOAD_MODELS = ["vosk-model-de-0.21"]



if current_user == 'SL5.de':
    PRELOAD_MODELS = ["vosk-model-de-0.21"]

# config/settings.py
PLUGIN_HELPER_TTS_ENABLED = True
# USE_AS_PRIMARY_SPEAK = "piper"
USE_AS_PRIMARY_SPEAK = "ESPEAK"
USE_ESPEAK_FALLBACK = True

#testtest


ESPEAK_FALLBACK_AMPLITUDE = 50

# --- LanguageTool Server ---
# Set to True to use an existing LT server. AT YOUR OWN RISK!
# The application will not start its own server and will not stop the external one.
USE_EXTERNAL_LANGUAGETOOL = False # Default: False

# URL for the external server if the option above is True.
# EXTERNAL_LANGUAGETOOL_URL = "http://127.0.0.1:8081"

# config/settings.py
# Settings for our internal server (if used)


# --- Text Correction Settings ---
# This dictionary controls which categories of LanguageTool rules are enabled.
# The application will use these settings to enable/disable rule categories
# when checking text. Set a category to False to ignore its suggestions.

# if true call iteratively all rules
default_mode_is_all = True
#  1 zwei drei vier 5
#

LT_SKIP_RATIO_THRESHOLD = 20
"""
Explanation of the Ratio Logic:
ratio = original_text_length / made_a_change: Calculates how many characters (on average) correspond to one change.

if ratio < lt_skip_ratio_threshold: If the ratio is low (less than the safe threshold), we skip LanguageTool.
"""

show_PLUGINS_ENABLED = True

PLUGINS_ENABLED = {
    "standard_actions/wikipedia_local": False,
    "standard_actions/count_loud": False,
    "game": False,
    "empty_all": False,
}
# count_loud▉

# needs restart. implemented in the python part:
ADD_TO_SENCTENCE = "."
# set ADD_TO_SENCTENCE = "" when you dont want it.


# Recording & Transcription
SUSPICIOUS_TIME_WINDOW = 90
SUSPICIOUS_THRESHOLD = 3


# Default is SYSTEM_DEFAULT, can be set to an integer (device index)
# or a string

# Select the audio input source for the STT engine:
# ------------------------------------------------
# None:
# Standard mode. Uses the system's default input device (e.g., your headset).
#
# 'UNIFIED_AUDIO_INPUT':
# Advanced Linux-only mode. Captures both the microphone AND the desktop
# audio (extern use of Aura, system, Radio, TV … sounds) simultaneously.
# It creates a virtual "Unified_Sink" and manages routing automatically
# via 'pactl' (PulseAudio/PipeWire).
# Note: 🐧 On Linux, this will temporarily bridge your audio sources.

PRE_RECORDING_TIMEOUT = 12
# SPEECH_PAUSE_TIMEOUT = 0.6


AUDIO_INPUT_DEVICE = 'SYSTEM_DEFAULT'
# INITIAL_WAIT_TIMEOUT = initial_silence_timeout
# SPEECH_PAUSE_TIMEOUT = 2.0 # Standardwert
SPEECH_PAUSE_TIMEOUT = 1
# Standardwert

# AUDIO_INPUT_DEVICE = ' MIC_AND_DESKTOP'
# PRE_RECORDING_TIMEOUT = 12
# SPEECH_PAUSE_TIMEOUT = 5

# SPEECH_PAUSE_TIMEOUT
# Hebel, um Aura spürbar zu beschleunigen:
# Reaktionszeit (Der wichtigste Hebel): Reduziere den SPEECH_PAUSE_TIMEOUT in der settings_local.py (z. B. auf 0.5 oder 0.8). Aura wartet dann kürzer nach dem Ende deines Satzes, bevor sie loslegt. Das fühlt sich sofort "snappy" an.




SAMPLE_RATE = 16000

# System
CRITICAL_THRESHOLD_MB = 1024 * 2

LANGUAGETOOL_PORT = 8082

# LanguageTool Server Configuration
LANGUAGETOOL_BASE_URL = f"http://127.0.0.1:{LANGUAGETOOL_PORT}"
LANGUAGETOOL_CHECK_URL = f"{LANGUAGETOOL_BASE_URL}/v2/check"
LANGUAGETOOL_RELATIVE_PATH = "LanguageTool-6.6/languagetool-server.jar"

NOTIFY_SEND_PATH = "/usr/bin/notify-send"
XDOTOOL_PATH = "/usr/bin/xdotool"

TRIGGER_FILE_PATH = "/tmp/sl5_record.trigger"

# Auto-detected Java path
# JAVA_EXECUTABLE_PATH = r"/usr/bin/java"

# needs NO restart. implemented in the sh part. TODO implemt for windows:
# use . for all Windows. Other examples:
# AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "."
AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "(ExampleAplicationThatNotExist|Pi, your personal AI)"
# TODO implement for windows


# Auto-detected Java path
JAVA_EXECUTABLE_PATH = r"/usr/bin/java"
