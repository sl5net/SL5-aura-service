# config/maps/plugins/game/0ad/0ad_actions.py
import time


def _dotool(command):
    import subprocess
    subprocess.run(['dotool'], input=command, text=True, check=True)


def press_plus_multiple_times(count):
    from scripts.py.func.audio_manager import speak_inclusive_fallback

    command_list = []
    for i in range(count):
        # Verwenden Sie 'rightbrace' für das deutsche Layout ohne Shift-Modifier
        command_list.append("key rightbrace")

    # Verbindet alle Befehle mit Zeilenumbrüchen zu einem einzigen String
    chained_commands = "\n".join(command_list)
    _dotool(chained_commands)

    time.sleep(2)
    speak_inclusive_fallback(f"count is {count}", "en-US")


def press_plus_multiple_times_slow(count):
    from scripts.py.func.audio_manager import speak_inclusive_fallback

    for _ in range(count):
        # echo "key plus" | dotool
        # dotool: WARNING: impossible key for layout: plus

        # echo "key kpplus" | dotool

        # _dotool('key kpplus') # ++++
        _dotool('key rightbrace')

        # time.sleep(0.01)

    time.sleep(2)
    speak_inclusive_fallback(f"count is {count}", "en-US")


def execute(match_data):
    import sys
    import platform
    from pathlib import Path
    try:
        print('0ad_actions.py:19')
        print('0ad_actions.py:19')
        print('0ad_actions.py:19')
        print('0ad_actions.py:19')
        print('0ad_actions.py:19')

        from scripts.py.func.audio_manager import speak_inclusive_fallback
        speak_inclusive_fallback("wait 0ad", "en-US")

        TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
        PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
        PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))

        if str(PROJECT_ROOT) not in sys.path:
            sys.path.insert(0, str(PROJECT_ROOT))

        text_after_replacement = match_data['text_after_replacement']
        print(f'0ad_actions.py:27 -> text_after_replacement: {text_after_replacement}')


        if 'wood' in text_after_replacement:
            press_plus_multiple_times(1)
        if 'fruit' in text_after_replacement:
            press_plus_multiple_times(2)
        if 'meat' in text_after_replacement:
            press_plus_multiple_times(3)
        elif 'stone' in text_after_replacement:
            press_plus_multiple_times(4)
        elif 'metal' in text_after_replacement:
            press_plus_multiple_times(5)

        text_after_replacement = ''
        # time.sleep(0.1)
        raise Exception('no text after replacement')
    finally:
        # optional: cleanup
        pass
