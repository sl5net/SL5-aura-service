# file: scripts/py/func/process_text_in_background.py
from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW
from .normalize_punctuation import normalize_punctuation

from .correct_text import correct_text
import re, time
from .notify import notify

def process_text_in_background(logger,
                               LT_LANGUAGE,
                               raw_text,
                               TMP_DIR,
                               recording_time,
                               active_lt_url):
    try:


        logger.info(f"THREAD: Starting processing for: '{raw_text}'")
        processed_text = normalize_punctuation(raw_text)
        processed_text = correct_text(logger, active_lt_url, LT_LANGUAGE, processed_text)
        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
        recording_time = time.time()
        timestamp = int(time.time() * 1000)
        unique_output_file = TMP_DIR / f"tts_output_{timestamp}.txt"
        unique_output_file.write_text(processed_text)
        logger.info(f"THREAD: Successfully wrote to {unique_output_file}")
        notify("Transcribed", duration=1000)
    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
    finally:
        logger.info(f"--- Background processing for '{raw_text[:20]}...' finished. ---")

    return suspicious_events
