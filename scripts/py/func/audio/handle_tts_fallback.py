
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from scripts.py.func.config.dynamic_settings import DynamicSettings
settings = DynamicSettings()
from ..audio_manager import speak_inclusive_fallback

# scripts/py/func/audio/handle_tts_fallback.py:11
def handle_tts_fallback(processed_text: str, LT_LANGUAGE: str, logger):
    home_dir = Path.home()
    speak_piper_file_path = home_dir / "projects" / "py" / "TTS" / "speak_file.py"
    primary_tts_successful = False

    # Warnung bei redundanter Konfiguration
    if settings.USE_AS_PRIMARY_SPEAK == "ESPEAK" and settings.USE_ESPEAK_FALLBACK:
        logger.warning("USE_AS_PRIMARY_SPEAK=ESPEAK + USE_ESPEAK_FALLBACK=True ist redundant.")

    # Primären TTS versuchen (nur wenn nicht ESPEAK primary)
    if settings.USE_AS_PRIMARY_SPEAK != "ESPEAK" and speak_piper_file_path.exists():
        tmp_file = None
        try:
            # speak_file.py erwartet Dateipfad, keinen Text direkt
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(processed_text)
                tmp_file = tmp.name
            result = subprocess.run(
                [sys.executable, str(speak_piper_file_path), tmp_file],
                timeout=15
            )
            primary_tts_successful = (result.returncode == 0)
        except Exception as e:
            logger.warning(f"Primary TTS failed: {e}")
        finally:
            if tmp_file and os.path.exists(tmp_file):
                os.unlink(tmp_file)

    use_fallback = (
        settings.USE_AS_PRIMARY_SPEAK == "ESPEAK"
        or
        (not primary_tts_successful and settings.USE_ESPEAK_FALLBACK and processed_text)
    )

    if use_fallback:
        if settings.USE_AS_PRIMARY_SPEAK != "ESPEAK":
            logger.warning("primary TTS failed. try Espeak-Fallback...")
        speak_inclusive_fallback(processed_text, LT_LANGUAGE)