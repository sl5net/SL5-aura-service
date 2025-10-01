# config/settings_local.py

# My personal settings for SL5 Aura
# This file is ignored by Git.

SERVICE_START_OPTION = 1
# Option 1: Start the service only on when there is an internet connection.

NOTIFICATION_LEVEL = 1

soundMute = 1
soundUnMute = 0

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
DEV_MODE = True
# DEV_MODE = False

# may yo want overwrite the PRELOAD_MODELS settings from settings.py here
# PRELOAD_MODELS = ["vosk-model-de-0.21"]
PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]


# --- Custom Correction Settings ---
# Import the default dictionary from the main settings file.
try:
    from .settings import CORRECTIONS_ENABLED
except ImportError:
    CORRECTIONS_ENABLED = {} # Fallback in case the import fails

# Update the dictionary with my personal preferences.
CORRECTIONS_ENABLED.update({
})


CRITICAL_THRESHOLD_MB = 1024 * 2
# CRITICAL_THRESHOLD_MB = 28000 # (also 28 GB)


# --- Custom Client-Side Plugins ---
# Enable or disable specific client-side behaviors (plugins).
# The logic is handled by client scripts (e.g., type_watcher.sh, AutoKey).
# These settings tell the backend service what to expect or how to format output.

#
PLUGINS_ENABLED = {
    "git": True,
    "wannweil": True,
    "game-dealers_choice": False,             # For Andy's poker game
    "0ad": True,             # For 0ad game
    "ethiktagung": True,
    "volkshochschule_tue": True,
    "CCC_tue": True

}

# needs restart. implemented in the python part:
ADD_TO_SENCTENCE = "."
# set ADD_TO_SENCTENCE = "" when you dont want it.


# needs NO restart:
PRE_RECORDING_TIMEOUT = 8
SPEECH_PAUSE_TIMEOUT = 2

# needs NO restart. implemented in the sh part. TODO implemt for windows:
# use . for all windos. Other examples:
# AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "."
AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "(ExampleAplicationThatNotExist|Pi, your personal AI)"
# TODO implemt for windows

