# config/settings_local.py
import os
import pwd

# My personal settings for SL5 Aura
# This file is ignored by Git.

SERVICE_START_OPTION = 1
# Option 1: Start the service only on when there is an internet connection.

# Get username
current_user = pwd.getpwuid(os.getuid())[0]

NOTIFICATION_LEVEL = 0 # 0=Silent, 1=Essential, 2=Verbose

soundMute = 1  # 1 is really recomanded. to know when your recording is endet.
soundUnMute = 1
soundProgramLoaded = 1

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
# DEV_MODE = True
DEV_MODE = False
DEV_MODE_memory = False

# may yo want to overwrite the PRELOAD_MODELS settings from settings.py here
PRELOAD_MODELS = ["vosk-model-de-0.21"]

if current_user == 'seeh':
    DEV_MODE = True
    # DEV_MODE = False
    PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]



# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"] # e.g. ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]

# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]

# PRELOAD_MODELS = ["vosk-model-en-us-0.22"]
# PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]


CRITICAL_THRESHOLD_MB = 1024 * 2
# CRITICAL_THRESHOLD_MB = 28000 # (also 28 GB)


# --- Custom Client-Side Plugins ---
# Enable or disable specific client-side behaviors (plugins).
# The logic is handled by client scripts (e.g., type_watcher_keep_alive.sh, AutoKey).
# These settings tell the backend service what to expect or how to format output.

#git status git status git status

USE_ESPEAK_FALLBACK = True

PLUGINS_ENABLED = {
    "empty_all": False,
    "git": True,
    # "wannweil": True,
    "game": False,
    "game/dealers_choice": True,
    "game/0ad": False,
    "ethiktagung": False,
    "volkshochschule_tue": True,
    "CCC_tue": True,
    "vsp_rt": True,
    "ki-maker-space": True,
    "numbers_to_digits": True, # hundert|einhundert --> 100
    "digits_to_numbers": False,
    "web-radio-funk": True,
    "it-begriffe": False,
    "it-begriffe/php/codeigniter": True,
}
#  geht status eins zwei doch

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

