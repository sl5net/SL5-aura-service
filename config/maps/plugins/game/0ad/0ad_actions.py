# config/maps/plugins/game/0ad/0ad_actions.py
import logging
import os
from pathlib import Path

_tmp_dir = Path("C:/tmp") if os.name == "nt" else Path("/tmp")
PROJECT_ROOT = Path((_tmp_dir / "sl5_aura" / "sl5net_aura_project_root").read_text().strip())

log_dir = PROJECT_ROOT / "log"
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.INFO)
_logger.propagate = False  # don't bubble up to the root logger / aura_engine.log
if not _logger.handlers:
    _handler = logging.FileHandler(str(log_dir / f"{__name__}.log"))
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s,%(msecs)03d - %(threadName)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    ))
    _logger.addHandler(_handler)


def log(msg: str) -> None:
    _logger.info(msg)


def _dotool(command):
    import subprocess
    subprocess.run(['dotool'], input=command, text=True, check=True)


def press_plus_multiple_times(count):

    command_list = []
    for i in range(count):
        # Verwenden Sie 'rightbrace' für das deutsche Layout ohne Shift-Modifier
        command_list.append("key rightbrace")

    # Verbindet alle Befehle mit Zeilenumbrüchen zu einem einzigen String
    chained_commands = "\n".join(command_list)
    _dotool(chained_commands)

def press_plus_multiple_times_slow(count):

    for _ in range(count):
        # echo "key plus" | dotool
        # dotool: WARNING: impossible key for layout: plus

        # echo "key kpplus" | dotool

        # _dotool('key kpplus') # ++++
        _dotool('key rightbrace')

def execute(match_data):
    import sys
    log(f'0ad_actions.py:19 execute called: {match_data}\n')

    from scripts.py.func.audio_manager import speak_inclusive_fallback

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    text_after_replacement = match_data['text_after_replacement']
    log(f'0ad_actions.py:27 -> text_after_replacement: {text_after_replacement}')

    if 'wood' in text_after_replacement:
        press_plus_multiple_times(1)
        speak_inclusive_fallback("wood", "en-US")

    if 'fruit' in text_after_replacement:
        press_plus_multiple_times(2)
    if 'meat' in text_after_replacement:
        press_plus_multiple_times(3)
    elif 'stone' in text_after_replacement:
        press_plus_multiple_times(4)
    elif 'metal' in text_after_replacement:
        press_plus_multiple_times(5)
    elif 'ctrl+alt' in text_after_replacement:
        speak_inclusive_fallback("DEBUG test lets go", "en-US")

        _dotool('keydown leftctrl\nkeydown leftalt\nkeyup leftalt\nkeyup leftctrl')
        # _dotool('key ctrl+alt')
        # _dotool('key ctrl:down alt:down alt:up ctrl:up') # dotool dont know this syntax: dotool --list-keys | grep -iE "^(ctrl|alt|leftctrl|leftalt)"
        # _dotool('key leftctrl:down\nkey leftalt:down\nkey leftalt:up\nkey leftctrl:up')
        # _dotool('keydown leftctrl leftalt\nkeyup leftctrl leftalt')
        # _dotool('key leftctrl leftalt')
        # subprocess.run(['xdotool', 'key', 'Control_L+Alt_L'], check=False)
        #
        # subprocess.run(['xdotool', 'keyup', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'], check=False)
        # subprocess.run(['xdotool', 'key', '--clearmodifiers', 'Control_L+Alt_L'], check=False)
        #

        # if 'ctrl+alt' in text_after_replacement or 'alles markieren' in text_after_replacement:
        #     import subprocess
        #     subprocess.run(['xdotool', 'search', '--name', '0 A.D.', 'key', '--clearmodifiers', 'Control_L+Alt_L'],
        #                    check=False)

        # if 'ctrl+alt' in text_after_replacement or 'alles markieren' in text_after_replacement:
        #     import time
        #     import subprocess
        #
        #     time.sleep(0.03)
        #
        #     subprocess.run(['xdotool', 'keyup', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R'], check=False)
        #     time.sleep(0.03)
        #     subprocess.run(['xdotool', 'keydown', 'Control_L'], check=False)
        #     time.sleep(0.03)
        #     subprocess.run(['xdotool', 'keydown', 'Alt_L'], check=False)
        #     time.sleep(0.05)
        #     subprocess.run(['xdotool', 'keyup', 'Alt_L'], check=False)
        #     time.sleep(0.05)
        #     subprocess.run(['xdotool', 'keyup', 'Control_L'], check=False)

    from scripts.py.func.global_state import SilentException
    raise SilentException()
