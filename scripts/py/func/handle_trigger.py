# File: scripts/py/func/handle_trigger.py
import platform, subprocess, threading, time
import sys
from pathlib import Path

from config.settings import SILENCE_TIMEOUT, SAMPLE_RATE, SUSPICIOUS_TIME_WINDOW, SUSPICIOUS_THRESHOLD
from .transcribe_audio_with_feedback import transcribe_audio_with_feedback
from .process_text_in_background import process_text_in_background
from .check_memory_critical import check_memory_critical
from .guess_lt_language_from_model import guess_lt_language_from_model
from .notify import notify

import vosk

def handle_trigger(
    logger,
    loaded_models,
    active_threads,
    suspicious_events,
    project_root,
    TMP_DIR,
    recording_time,
    active_lt_url
):
    logger.info(f"TRIGGER DETECTED! Active threads: {len(active_threads)}")
    model_name_file = project_root / "config/model_name.txt"
    last_used_file = project_root / "config/model_name_lastused.txt"

    try:
        target_model_name = model_name_file.read_text().strip()
        if not target_model_name: raise FileNotFoundError("model_name.txt is empty")
        last_used_file.write_text(target_model_name)
    except FileNotFoundError as e:
        logger.warning(f"Could not read target model ('{e}'). Using first available as fallback.")
        first_key = list(loaded_models.keys())[0]
        selected_model = loaded_models[first_key]
        target_model_name = f"fallback-model-{first_key}"
    else:
        # --- ROBUSTNESS-fallback: search language-key ---
        selected_model = None
        found_key = None
        for key in loaded_models.keys():
            # search "-de-" or "-en-"
            if f"-{key}-" in target_model_name:
                selected_model = loaded_models[key]
                found_key = key
                logger.info(f"Language key '{key}' found in '{target_model_name}'. Selecting model.")
                break # kay is found

        # Fallback
        if not selected_model:
            logger.error(f"No matching pre-loaded model found for '{target_model_name}'. Falling back.")
            first_key = list(loaded_models.keys())[0]
            selected_model = loaded_models[first_key]
            target_model_name = f"fallback-model-{first_key}"
        # --- end extra robustness  ---

    lt_language = guess_lt_language_from_model(target_model_name)
    logger.info(f"Using model for lang '{lt_language}'.")

    recognizer = vosk.KaldiRecognizer(selected_model, SAMPLE_RATE)
    raw_text = transcribe_audio_with_feedback(logger, recognizer, lt_language, SILENCE_TIMEOUT, SAMPLE_RATE)

    # 2. proof "strange" Events
    if not raw_text.strip() or len(raw_text.split()) < 1:
        suspicious_events.append(time.time())
    now = time.time()
    suspicious_events = [t for t in suspicious_events if now - t < SUSPICIOUS_TIME_WINDOW]

    if len(suspicious_events) >= SUSPICIOUS_THRESHOLD:
        message = f"record is often ({SUSPICIOUS_THRESHOLD}) very short. Want set SILENCE_TIMEOUT to 0.8 or 1.0 ?"
        notify(
            f"Tip: record often (({SUSPICIOUS_THRESHOLD})) to short?",
            message,
            "normal"
        )
        suspicious_events = []



    if raw_text.strip():
        thread = threading.Thread(target=process_text_in_background,
                                    args=(logger, lt_language, raw_text, TMP_DIR,
                                        recording_time, active_lt_url ))
        thread.start()
        active_threads.append(thread)

