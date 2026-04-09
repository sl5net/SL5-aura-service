
from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
from .piper_speak_via_server import piper_speak_via_server
from ..audio_manager import speak_inclusive_fallback

# scripts/py/func/audio/handle_tts_fallback.py:11

from pathlib import Path
import platform


TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")

def handle_tts_fallback(processed_text, LT_LANGUAGE, logger):

    if not settings.PLUGIN_HELPER_TTS_ENABLED:
        logger.info("no PLUGIN_HELPER_TTS_ENABLED > skipping audio-speak ...")
        return False # Silent mode

    # Wait if self-test is running
    self_test_running = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"

    if self_test_running.exists():
        logger.info("Maintenance: Self-test is running, skipping audio-speak ...")
        return False


    # 1. Try via Piper Server (if not ESPEAK primary)
    if settings.USE_AS_PRIMARY_SPEAK != "ESPEAK":
        if piper_speak_via_server(processed_text):
            return True
        logger.warning("Primary TTS failed. Trying Fallback...")

    # 2. Fallback zu Espeak
    if settings.USE_ESPEAK_FALLBACK:
        speak_inclusive_fallback(processed_text, LT_LANGUAGE)
        return True
    return False
