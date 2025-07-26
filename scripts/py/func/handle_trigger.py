# File: scripts/py/func/handle_trigger.py
import threading, time, vosk

from .guess_lt_language_from_model import guess_lt_language_from_model
from .notify import notify
from .process_text_in_background import process_text_in_background
from .transcribe_audio_with_feedback import transcribe_audio_with_feedback

from .prioritize_model import prioritize_model


from config.settings import SAMPLE_RATE, SUSPICIOUS_TIME_WINDOW, SUSPICIOUS_THRESHOLD, \
    PRE_RECORDING_TIMEOUT, SILENCE_TIMEOUT


def handle_trigger(
        logger,
        loaded_models,
        active_threads,
        suspicious_events,
        project_root,
        TMP_DIR,
        recording_time,
        active_lt_url,
        stop_event
):
    if not loaded_models:
        logger.error("Trigger ignored: No models are loaded, likely due to low memory.")
        notify("STT-error", "no models loaded (less memory). recording ignored.")
        return
    logger.info(f"TRIGGER DETECTED! Active threads: {len(active_threads)}")
    model_name_file = project_root / "config/model_name.txt"
    last_used_file = project_root / "config/model_name_lastused.txt"
    found_key = None  # Initialize found_key

    try:
        target_model_name = model_name_file.read_text().strip()
        if not target_model_name: raise FileNotFoundError("model_name.txt is empty")
        # last_used_file.write_text(target_model_name)
    except FileNotFoundError as e:
        logger.warning(f"Could not read target model ('{e}'). Using first available as fallback.")
        found_key = list(loaded_models.keys())[0]
        selected_model = loaded_models[found_key]
        target_model_name = f"fallback-model-{found_key}"
    else:
        # --- ROBUSTNESS-fallback: search language-key ---
        selected_model = None
        for key in loaded_models.keys():
            # search "-de-" or "-en-"
            if f"-{key}-" in target_model_name:
                selected_model = loaded_models[key]
                found_key = key
                logger.info(f"Language key '{key}' found in '{target_model_name}'. Selecting model.")
                break  # key is found

        # Fallback
        if not selected_model:
            logger.error(f"No matching pre-loaded model found for '{target_model_name}'. Falling back.")
            found_key = list(loaded_models.keys())[0]
            selected_model = loaded_models[found_key]
            target_model_name = f"fallback-model-{found_key}"
        # --- end extra robustness  ---

    last_used_model_name = last_used_file.read_text().strip()

    if last_used_model_name != target_model_name:
        prioritize_model(logger, loaded_models, found_key)

    last_used_file.write_text(target_model_name)

    lt_language = guess_lt_language_from_model(target_model_name)
    logger.info(f"Using model for lang '{lt_language}'.")

    recognizer = vosk.KaldiRecognizer(selected_model, SAMPLE_RATE)

    if not SILENCE_TIMEOUT:
        logger.error(f"SILENCE_TIMEOUT: '{SILENCE_TIMEOUT}' ")
    if not PRE_RECORDING_TIMEOUT:
        logger.error(f"PRE_RECORDING_TIMEOUT: '{PRE_RECORDING_TIMEOUT}' ")

    if len(suspicious_events) == 0:
        silence_timout = PRE_RECORDING_TIMEOUT
        logger.info(f"silence_timout now set to = PRE_RECORDING_TIMEOUT: '{PRE_RECORDING_TIMEOUT}' ")
    else:
        silence_timout = SILENCE_TIMEOUT

    raw_text = transcribe_audio_with_feedback(logger, recognizer, lt_language, stop_event)

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
                                        recording_time, active_lt_url))
        thread.start()
        active_threads.append(thread)