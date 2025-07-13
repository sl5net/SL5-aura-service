# file: scripts/py/func/process_text_in_background.py
from config.settings import SUSPICIOUS_THRESHOLD, SUSPICIOUS_TIME_WINDOW
from .normalize_punctuation import normalize_punctuation

from config.languagetool_server.FUZZY_MAP import FUZZY_MAP

from .correct_text import correct_text
import re, time
from thefuzz import fuzz
from .notify import notify

def process_text_in_background(logger,
                               LT_LANGUAGE,
                               raw_text,
                               TMP_DIR,
                               recording_time,
                               active_lt_url):
    try:


        logger.info(f"THREAD: Starting processing for: '{raw_text}'")

        # In der Funktion, wo die Aufnahme stoppt
        notify("Processing...", f"THREAD: Starting processing for: '{raw_text}'", "low", replace_tag="transcription_status")

        processed_text = normalize_punctuation(raw_text)

        if "git" not in processed_text and "push" not in processed_text:
            processed_text = correct_text(logger, active_lt_url, LT_LANGUAGE, processed_text)

        #processed_text = correct_text(logger, active_lt_url, LT_LANGUAGE, processed_text)

#git statusgit pushGeht Pool

        # Step 2: Slower, fuzzy replacements on the result
        # --- KORRIGIERTE FUZZY-MATCHING-LOGIK ---

        # Wir vergleichen den gesamten Satz, nicht mehr Wort für Wort.
        # Wir suchen den besten Treffer in der gesamten FUZZY_MAP.

        logger.info(f"DEBUG: Starting fuzzy match for: '{processed_text}'")

        best_score = 0
        best_replacement = None

        for replacement, match_phrase, threshold in FUZZY_MAP:
            score = fuzz.token_set_ratio(processed_text.lower(), match_phrase.lower())

            if score >= threshold and score > best_score:
                best_score = score
                best_replacement = replacement

        if best_replacement:
            logger.info(f"Fuzzy match found: Replacing '{processed_text}' with '{best_replacement}' (Score: {best_score})")
            processed_text = best_replacement
        else:
            logger.info(f"No fuzzy match found for '{processed_text}'")

        # --- ENDE DER KORRIGIERTEN LOGIK ---








        if re.match(r"^\w", processed_text) and time.time() - recording_time < 20:
            processed_text = ' ' + processed_text
        recording_time = time.time()
        timestamp = int(time.time() * 1000)
        unique_output_file = TMP_DIR / f"tts_output_{timestamp}.txt"
        unique_output_file.write_text(processed_text)
        logger.info(f"THREAD: Successfully wrote to {unique_output_file}")

        # notify("Transcribed", duration=700, urgency="low")

        notify("Transcribed", "", "low", duration=1000, replace_tag="transcription_status")


    except Exception as e:
        logger.error(f"FATAL: Error in processing thread: {e}", exc_info=True)
        notify(f"FATAL: Error in processing thread", duration=4000, urgency="low")
    finally:
        logger.info(f" Background processing for '{raw_text[:20]}...' finished. ")
        notify(f" Background processing for '{raw_text[:20]}...' finished. ", duration=700, urgency="low")

