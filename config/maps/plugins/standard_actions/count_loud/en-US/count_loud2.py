# ==============================================================================
# 🌐 AUTOMATICALLY GENERATED / MACHINE-TRANSLATED MAP
# ==============================================================================
# ℹ️  Source Language: German (de-DE)
# ⚙️  Note: Speech recognition regexes (VOSK) and Koan instructions in this
#     file were machine-translated. Spoken patterns may require refinement
#     or tuning for natural speech in the target language.
#
# 🤝  CONTRIBUTIONS WELCOME!
#     We would love your help improving this map! If you test or refine these
#     regex patterns, please open a Pull Request with your improvements.
# ==============================================================================

# config/maps/plugins/standard_actions/count_loud/de-DE/count_loud.py

# import sys

from pathlib import Path
import subprocess

RULES_FILE_PATH = Path(__file__).parent / 'FUZZY_MAP_pre.py'
def speak(text):
    """Gibt Text über ein TTS-System aus. Passen Sie den Befehl ggf. an."""
    try:
        subprocess.run(['espeak', '-v', 'de', text], check=True)
    except Exception as e:
        print(f"STDOUT (TTS-Fallback): {text} , {e}")

# standard_actions/count_loud/de-DE/count_loud.py:14

def on_file_load():
    # This must be defined to show up in the attributes list

    from scripts.py.func.audio_manager import speak_inclusive_fallback

    speak_inclusive_fallback("started 1", 'de-DE')

def on_plugin_load():
    from scripts.py.func.audio_manager import speak_inclusive_fallback

    speak_inclusive_fallback("einmal nur 20", 'de-DE')

# Jeff


# def on_reload():

# speak("System reloaded 1")

#
# #Try it out

#
# def on_folder_change(current_dir=None):

# speak("Hello Sun 4") #desTestTestTestTestjkhlTestsdfsdf

#
# def execute(match_data):

#
# speak("Hello mountain")

#
# def __main__():

# speak("Hello tree")

#
#
#
# if __name__ == '__main__':

# __Main__()


# TestTestTest

