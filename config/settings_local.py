# config/settings_local.py

# My personal settings for SL5 Aura
# This file is ignored by Git.

SERVICE_START_OPTION = 1
# Option 1: Start the service only on when there is an internet connection.

NOTIFICATION_LEVEL = 1

soundMute = 1  # 1 is really recommandet. to know when your recording is endet.
soundUnMute = 1

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
# DEV_MODE = True
DEV_MODE = False

# may yo want to overwrite the PRELOAD_MODELS settings from settings.py here
# PRELOAD_MODELS = ["vosk-model-de-0.21"]

# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]

PRELOAD_MODELS = ["vosk-model-de-0.21"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]


CRITICAL_THRESHOLD_MB = 1024 * 2
# CRITICAL_THRESHOLD_MB = 28000 # (also 28 GB)


# --- Custom Client-Side Plugins ---
# Enable or disable specific client-side behaviors (plugins).
# The logic is handled by client scripts (e.g., type_watcher.sh, AutoKey).
# These settings tell the backend service what to expect or how to format output.


PLUGINS_ENABLED = {
    "git": True,
    "wannweil": True,
    "game-dealers_choice": False,
    "0ad": False,
    "ethiktagung": True,
    "volkshochschule_tue": False,
    "CCC_tue": True,
    "vsp_rt": True,
    "ki-maker-space": True,
    "numbers_to_digits": True,
    # "digits_to_numbers": False, deprecated
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
# TODO implement for windows

