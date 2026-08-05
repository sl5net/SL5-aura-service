# config/maps/plugins/game/0ad/0ad_actions.py
import logging
import os
import subprocess
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
    subprocess.run(['dotool'], input=command, text=True, check=True)
    # helpful tips: dotool --list-keys | grep -iE "period|dot|full"

def press_plus_multiple_times(count):
    # helpful tips: dotool --list-keys | grep -iE "period|dot|full"
    command_list = []
    for i in range(count):
        # Verwenden Sie 'rightbrace' für das deutsche Layout ohne Shift-Modifier
        command_list.append("key rightbrace")

    # Verbindet alle Befehle mit Zeilenumbrüchen zu einem einzigen String
    chained_commands = "\n".join(command_list)
    _dotool(chained_commands)

def press_plus_multiple_times_slow(count):
    # helpful tips: dotool --list-keys | grep -iE "period|dot|full"
    for _ in range(count):
        # echo "key plus" | dotool
        # dotool: WARNING: impossible key for layout: plus

        # echo "key kpplus" | dotool

        # _dotool('key kpplus') # ++++
        _dotool('key rightbrace')


def execute(match_data):
    # helpful tips: dotool --list-keys | grep -iE "period|dot|full"
    import sys
    log(f'0ad_actions.py:19 execute called: {match_data}\n')

    from scripts.py.func.audio_manager import speak_inclusive_fallback

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    text_after_replacement = match_data['text_after_replacement']
    log(f'0ad_actions.py:27 -> text_after_replacement: {text_after_replacement}')

    def _idle_select(do_speak= False):
        _dotool('keydown leftalt\nkey backslash\nkeyup leftalt')  # works 30.7.'26 15:05 Thu
        if do_speak:
            speak_inclusive_fallback("idle worker selected", "en-US")

    def _schedule_idle_select(delay=8, do_speak= False):
        import threading

        def _auto_select():
            # helpful tips: dotool --list-keys | grep -iE "period|dot|full"
            # _dotool('key alt+numbersign')
            # _dotool('key alt+.')
            # _dotool('keydown leftalt\n.\nkeyup leftalt')
            # _dotool('key leftalt period')
            # _dotool('keydown leftalt\nkey period\nkeyup leftalt')



            # _dotool('keydown leftalt\nkey rightbrace\nkeyup leftalt') macht ganz oder markiert alle??

            # _dotool('keydown leftalt\nkey dot\nkeyup leftalt') # works 30.7.'26 14:26 Thu
            # _dotool('keydown leftalt\nkey backslash\nkeyup leftalt') # works 30.7.'26 15:05 Thu
            _idle_select(do_speak)



            # subprocess.run(['xdotool', 'key', '--clearmodifiers', 'Alt+period'], check=False)

        timer = threading.Timer(delay, _auto_select)
        timer.daemon = True
        timer.start()
    if False:
        print('')
    elif 'h' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("haus wurde gesprochen", "en-US")
        _schedule_idle_select()
    elif 's' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("store-haus", "en-US")
        _schedule_idle_select()
    elif 'f' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("field", "en-US")
        _schedule_idle_select()
    elif 'b' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("barrack", "en-US")
        _schedule_idle_select()
    elif 'm' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("markt", "en-US")
        _schedule_idle_select()
    elif 'n' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("forge", "en-US")
        _schedule_idle_select()
    elif 't' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("sentry_tower", "en-US")
        _schedule_idle_select()
    elif 'tt' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("defense_tower", "en-US")
        _schedule_idle_select()
    elif 'ttt' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("temple", "en-US")
        _schedule_idle_select()
    elif 'a' == text_after_replacement:
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        speak_inclusive_fallback("arsenal", "en-US")
        _schedule_idle_select()
    elif 'ff' == text_after_replacement:
        _idle_select()
        _dotool('key f\nkey f')
        speak_inclusive_fallback("farm", "en-US")
        _schedule_idle_select()
    elif 'fff' == text_after_replacement:
        _idle_select()
        _dotool('key f\nkey f\nkey f')
        speak_inclusive_fallback("fortress", "en-US")
        _schedule_idle_select()
    elif text_after_replacement == 'dd':
        _idle_select()
        _dotool('key d\nkey d\nkey')
        _schedule_idle_select()

    elif text_after_replacement in ['aa', 'aaa', 'aaaa', 'aaaaa']:
        cmd = ' '.join(['a\nkey'] * len(text_after_replacement))
        _idle_select()
        _dotool(f'key {cmd}')
        _schedule_idle_select()

    elif text_after_replacement in ['select iddle', 'select_idle']:
        _idle_select()

    elif text_after_replacement.startswith('select_'):
        select_map = {
            'select_infantry': ('i', 'infantry'),
            'select_pikemen': ('p', 'pikemen'),
            'select_cavalry': ('c', 'cavalry'),
            'select_archers': ('a', 'archers'),
            'select_swordsmen': ('s', 'swordsmen'),
            'select_elephants': ('e', 'elephants'),
            'select_catapults': ('k', 'catapults'),
            'select_healers': ('h', 'healers'),
            'select_women': ('w', 'woman'),
        }
        item = select_map.get(text_after_replacement)
        if item:
            key_letter, spoken_label = item
            _dotool(f'keydown leftalt\nkey {key_letter}\nkeyup leftalt')
            speak_inclusive_fallback(f"select {spoken_label}", "en-US")








    elif 'wood' in text_after_replacement:
        _idle_select()
        press_plus_multiple_times(1)
        speak_inclusive_fallback("wood", "en-US")
        _schedule_idle_select()

    elif 'fruit' in text_after_replacement:
        _idle_select()
        press_plus_multiple_times(2)
        speak_inclusive_fallback("fruit", "en-US")
        _schedule_idle_select()

    elif 'meat' in text_after_replacement:
        _idle_select()
        press_plus_multiple_times(3)
        speak_inclusive_fallback("meat", "en-US")
        _schedule_idle_select()

    elif 'stone' in text_after_replacement:
        _idle_select()
        press_plus_multiple_times(4)
        speak_inclusive_fallback("stone", "en-US")
        _schedule_idle_select()

    elif 'metal' in text_after_replacement:
        _idle_select()
        press_plus_multiple_times(5)
        speak_inclusive_fallback("metal", "en-US")
        _schedule_idle_select()

    elif len(text_after_replacement) == 1 and text_after_replacement.isalpha():
        _idle_select()
        _dotool(f'key {text_after_replacement}')
        _schedule_idle_select()

    elif text_after_replacement.startswith('kp'):
        direction_map = {
            'kp8': 'kp8', 'north': 'kp8', 'norden': 'kp8',
            'kp2': 'kp2', 'south': 'kp2', 'sueden': 'kp2',
            'kp6': 'kp6', 'east': 'kp6', 'osten': 'kp6',
            'kp4': 'kp4', 'west': 'kp4', 'westen': 'kp4',
            'kp9': 'kp9', 'northeast': 'kp9', 'nordosten': 'kp9',
            'kp7': 'kp7', 'northwest': 'kp7', 'nordwesten': 'kp7',
            'kp3': 'kp3', 'southeast': 'kp3', 'suedosten': 'kp3',
            'kp1': 'kp1', 'southwest': 'kp1', 'suedwesten': 'kp1',
        }
        _schedule_idle_select()
        for token, kp_key in direction_map.items():
            if token in text_after_replacement.lower():
                _dotool(f'key {kp_key}')
                break
        speak_inclusive_fallback(text_after_replacement, "en-US")

    elif text_after_replacement.startswith('camera_'):
        camera_map = {
            'camera_up': 'alt+Up',
            'camera_down': 'alt+Down',
            'camera_left': 'alt+Left',
            'camera_right': 'alt+Right',
        }
        key_cmd = camera_map.get(text_after_replacement)
        if key_cmd:
            _dotool(f'key {key_cmd}')
            speak_inclusive_fallback("camera", "en-US")



    elif 'ctrl+alt' in text_after_replacement:

        _dotool('keydown leftctrl\nkeydown leftalt\nkeyup leftalt\nkeyup leftctrl')
        speak_inclusive_fallback("select all", "en-US")

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
