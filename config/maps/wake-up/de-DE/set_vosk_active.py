# config/maps/wake-up/de-DE/set_vosk_active.py:1
import os
import platform
from pathlib import Path

from scripts.py.func.audio_manager import speak_inclusive_fallback

def execute(match_data):
    """
    Inverted Logic: If the flag exists, the Aura is SUSPENDED.
    Default behavior remains 'active' without core source changes.
    """
    if platform.system() == "Windows":
        TMP_DIR = Path("C:/tmp")
    else:
        TMP_DIR = Path("/tmp")

    print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL cmd_tag')


    # Ensure directory exists for flag file
    if not TMP_DIR.exists():
        TMP_DIR.mkdir(parents=True, exist_ok=True)

    flag_path = TMP_DIR / "sl5_aura" / "aura_vosk_suspended.flag"
    cmd_tag = match_data.get('text_after_replacement', '').lower()

    if cmd_tag == "voss_stop":
        # Create flag to stop processing (Mute)
        flag_path.touch()
        speak_inclusive_fallback("Ich schlafe jetzt", 'de-DE')
        return "Suspended🗣"

    elif cmd_tag == "voss_start":
        # Remove flag to resume processing (Unmute)
        if flag_path.exists():
            os.remove(flag_path)
            speak_inclusive_fallback("Ich höre zu", 'de-DE')
        return "on🗣" # STT Active. Mute flag removed

    status = "Suspended" if flag_path.exists() else "Active"
    return f"Vosk Status: {status}"
#
#on🗣einenbin klappt das einschlafen

