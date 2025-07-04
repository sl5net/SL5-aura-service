import subprocess
import time
from pathlib import Path
import os

# SCRIPT_DIR = Path(__file__).resolve().parent

import tomllib # In Python 3.11+ Standard
CONFIG_PATH = Path.home() / ".config/sl5-stt/config.toml"
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)
PROJECT_DIR = Path(config["paths"]["project_root"])


readmeBuckup = """
xdotool key --clearmodifiers ctrl+Left ctrl+shift+Right && sleep 0.1 && xdotool key --clearmodifiers ctrl+c && sleep 0.1 && {scriptDir}/.venv/bin/python {scriptDir}/vosk-tts/bin/python ~/projects/py/STT/get_suggestions.py
command = 'xdotool click 2 && sleep 0.1 && xdotool key --clearmodifiers "ctrl+c" && sleep 0.1 && {scriptDir}/vosk-tts/bin/python ~/projects/py/STT/get_suggestions.py'
system . exec_command (command)
Mond
"""

keyboard.send_keys('<ctrl>+<left>')
keyboard.send_keys('<ctrl>+<shift>+<right>')
keyboard.send_keys('<ctrl>+c')
time.sleep(0.2)
keyboard.send_keys('<right>')

home_dir = Path.home()

command = f"{PROJECT_DIR}/.venv/bin/python {PROJECT_DIR}/get_suggestions.py"
# clipboard.fill_clipboard(command)
# {SCRIPT_DIR}/.venv/bin/python {SCRIPT_DIR}/get_suggestions.py
# maus     Has Huns UAS Hulas Huts /home/seeh/.config/autokey/data/stt/autokey-scripts/.venv/bin/python /home/seeh/.config/autokey/data/stt/autokey-scripts/get_suggestions.py
system.exec_command (command)

# Haus ( aus | hass | hatz | hausse | ass )






