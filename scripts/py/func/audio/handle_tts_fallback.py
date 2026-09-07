# scripts/py/func/audio/handle_tts_fallback.py:1
import platform

# scripts/py/func/audio/handle_tts_fallback.py:11
from pathlib import Path

from scripts.py.func.config.dynamic_settings import settings

from .piper_speak_via_server import piper_speak_via_server

TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")


def handle_tts_fallback(processed_text, LT_LANGUAGE, logger):
    if not settings.PLUGIN_HELPER_TTS_ENABLED:
        logger.info("no PLUGIN_HELPER_TTS_ENABLED > skipping audio-speak …")
        return False  # Silent mode

    # Wait if self-test is running
    self_test_running = TMP_DIR / "sl5_aura" / "core_logic_self_test_FILE_is_running"

    if self_test_running.exists():
        logger.info("Maintenance: Self-test is running, skipping audio-speak …")
        return False

    # 1. Try Piper Server (if not ESPEAK primary)
    if str(getattr(settings, "USE_AS_PRIMARY_SPEAK", "")).upper() != "ESPEAK":
        if piper_speak_via_server(processed_text):
            return True
        logger.warning("Primary TTS failed. Trying Wyoming fallback")
        from .wyoming_speak import wyoming_speak

        if wyoming_speak(processed_text, logger=logger):
            logger.info("Wyoming TTS synthesis started successfully")
            return True
        logger.warning("Wyoming TTS failed or unreachable. Trying espeak fallback")
    # 2. Fallback Espeak
    if settings.USE_ESPEAK_FALLBACK:
        logger.info("Triggering espeak fallback")
        from ..audio_manager import speak_inclusive_fallback

        speak_inclusive_fallback(processed_text, LT_LANGUAGE)
        return True

    return False
