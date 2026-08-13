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

# config/maps/wake-up/de-DE/set_vosk_active.py:1

import os
import platform
from pathlib import Path


def execute(match_data):
    from scripts.py.func.audio_manager import speak_inclusive_fallback

    """
    Inverted Logic: If the flag exists, the Aura is SUSPENDED.
    Default behavior remains 'active' without core source changes.
    """
    if platform.system() == "Windows":
        TMP_DIR = Path("C:/tmp")
    else:
        TMP_DIR = Path("/tmp")

    print('LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL cmd_tag')


    # Assurez-vous que le répertoire existe pour le fichier d'indicateur

    if not TMP_DIR.exists():
        TMP_DIR.mkdir(parents=True, exist_ok=True)

    flag_path = TMP_DIR / "sl5_aura" / "aura_vosk_suspended.flag"
    cmd_tag = match_data.get('text_after_replacement', '').lower()

    if cmd_tag == "voss_stop":
        # Créer un indicateur pour arrêter le traitement (Muet)

        flag_path.touch()
        speak_inclusive_fallback("Ich schlafe jetzt", 'de-DE')
        return "Suspended🗣"

    elif cmd_tag == "voss_start":
        # Supprimer l'indicateur pour reprendre le traitement (Réactiver le son)

        if flag_path.exists():
            os.remove(flag_path)
            speak_inclusive_fallback("Ich höre zu", 'de-DE')
        return "on🗣" # STT Active. Mute flag removed

    status = "Suspended" if flag_path.exists() else "Active"
    return f"Vosk Status: {status}"
#
# on🗣parfois je peux m'endormir


