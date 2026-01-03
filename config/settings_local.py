# config.settings_local.py
from scripts.py.func.determine_current_user import determine_current_user

# My personal settings for SL5 Aura
# This file should may ignored by you by Git. But is not here for demonstration.

SERVICE_START_OPTION = 0
# Option 1: Start the service only on when there is an internet connection.

current_user,_ = determine_current_user()
print(f'hi, hallo, welcome: {current_user}')

NOTIFICATION_LEVEL = 0 # 0=Silent, 1=Essential, 2=Verbose

soundMute = 1  # 1 is really recommended. to know when your recording is ended.
soundUnMute = 1
soundProgramLoaded = 1


# best disable before run self-tester(DEV_MODE = True) rules like: match all to nothing. like: .+ -> or .* -> ''

# Set to True to disable certain production checks for local development,
# e.g., the wrapper script enforcement.
# DEV_MODE = True
DEV_MODE = False
DEV_MODE_memory = False
DEV_MODE_all_processing = False

# needs NO restart:
PRE_RECORDING_TIMEOUT = 6
SPEECH_PAUSE_TIMEOUT = 2

# may yo want to overwrite the PRELOAD_MODELS settings from settings.py here
PRELOAD_MODELS = ["vosk-model-de-0.21"]

#test (original:'test', 🗣SL5。de╱Aura).
if current_user == 'seeh' or current_user == 'SL5.de' :

    # needs NO restart:
    PRE_RECORDING_TIMEOUT = 2
    SPEECH_PAUSE_TIMEOUT = 1



    PLUGIN_HELPER_TTS_ENABLED = False


    signatur=''

    #
    if 1:
        signatur=''
        signatur1=f''
        signatur_pt_br=f''
        signatur_en=f''
        signatur_ar=f''
        signatur_ja=f''


    DEV_MODE = 1
    DEV_MODE_all_processing = 0
    PRELOAD_MODELS = ["vosk-model-de-0.21"]
    PRELOAD_MODELS = ["vosk-model-de-0.21", "vosk-model-en-us-0.22"]
    # PRELOAD_MODELS = ["vosk-model-small-de-0.15"]
    # PRELOAD_MODELS = ["vosk-model-en-us-0.22"]
    # needs NO restart:


    AUDIO_INPUT_DEVICE = 'SYSTEM_DEFAULT'


    if 1:
        AUDIO_INPUT_DEVICE = 'SYSTEM_DEFAULT'
        # INITIAL_WAIT_TIMEOUT = initial_silence_timeout
        # SPEECH_PAUSE_TIMEOUT = 2.0 # Standardwert
        SPEECH_PAUSE_TIMEOUT = 1
        # Standardwert
    else:
        AUDIO_INPUT_DEVICE = 'MIC_AND_DESKTOP'
        PRE_RECORDING_TIMEOUT = 6
        SPEECH_PAUSE_TIMEOUT = 4


#


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
    "wannweil": True,
    "game": False,
    "game.dealers_choice": True,
    "game.0ad": False,
    "ethiktagung": False,
    "volkshochschule_tue": True,
    "CCC_tue": True,
    "vsp_rt": True,
    "ki-maker-space": True,
    "numbers_to_digits": True,
    "digits_to_numbers": False,
    "web-radio-funk": True,
    "it-begriffe": True,
    "it-begriffe.php.codeigniter": True,


}
#  geht status eins zwei doch

# needs restart. implemented in the python part:
ADD_TO_SENCTENCE = "."
# set ADD_TO_SENCTENCE = "" when you dont want it.



# needs NO restart. implemented in the sh part. TODO implemt for windows:
# use . for all windos. Other examples:
# AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "."
AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = "(ExampleAplicationThatNotExist|Pi, your personal AI)"
# TODO implement for windows

