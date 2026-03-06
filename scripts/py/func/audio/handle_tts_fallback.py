
from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
from .piper_speak_via_server import piper_speak_via_server
from ..audio_manager import speak_inclusive_fallback

# scripts/py/func/audio/handle_tts_fallback.py:11

def handle_tts_fallback(processed_text, LT_LANGUAGE, logger):
    # 1. Versuch via Piper Server (falls nicht ESPEAK primary)
    if settings.USE_AS_PRIMARY_SPEAK != "ESPEAK":
        if piper_speak_via_server(processed_text):
            return True
        logger.warning("Primary TTS failed. Trying Fallback...")

    # 2. Fallback zu Espeak
    if settings.USE_ESPEAK_FALLBACK:
        speak_inclusive_fallback(processed_text, LT_LANGUAGE)
        return True
    return False
