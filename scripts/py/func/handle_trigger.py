# scripts/py/func/handle_trigger.py
import threading
import time
import vosk

import config.settings_local
from config.settings import PRE_RECORDING_TIMEOUT, SPEECH_PAUSE_TIMEOUT, SAMPLE_RATE

from .model_manager import MODELS_LOCK

# In scripts/py/func/handle_trigger.py
dictation_session_active = threading.Event()
active_transcription_thread = None

from scripts.py.func.process_text_in_background import process_text_in_background
from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model
from scripts.py.func.audio_manager import unmute_microphone


def finalize_recording_session(logger):
    """A dedicated function to clean up after a recording session."""
    global active_transcription_thread

    logger.info("Finalizing recording session: All new audio intake has stopped.")

    # Set the global thread variable to None to indicate no active session.
    active_transcription_thread = None




def handle_trigger(
        logger,
        loaded_models,
        suspicious_events,
        project_root,
        TMP_DIR,
        recording_time,
        active_lt_url
):
    global active_transcription_thread

    # --- ACTION 1: STOP an ongoing session ---
    if dictation_session_active.is_set():
        logger.info("⏹️ Manual stop trigger detected. Signaling session to end.")


        # We just send the signal and exit immediately.
        # We DO NOT wait here for the thread to finish. This prevents
        # blocking and queuing of subsequent trigger events.
        dictation_session_active.clear()

        return


    # --- ACTION 2: START a new session ---

    unmute_microphone()

    logger.info("🎬 Trigger received. Starting new dictation session.")
    dictation_session_active.set()

    # --- Select a model safely ---
    selected_model = None
    found_key = None
    with MODELS_LOCK:
        if not loaded_models:
            logger.error("Trigger ignored: No models have been loaded yet.")
            dictation_session_active.clear()
            return

        try:
            target_model_name = (project_root / "config/model_name.txt").read_text().strip()
            logger.info("----> Target model name: %s", target_model_name)

            if not target_model_name: raise FileNotFoundError

            # Find the requested model among loaded ones
            for key, model_dict in loaded_models.items():
                if f"-{key}-" in target_model_name:
                    selected_model = model_dict
                    found_key = key
                    break

            if not selected_model:
                logger.warning(f"Model for '{target_model_name}' not ready. Using first available.")
                found_key = list(loaded_models.keys())[0]
                selected_model = loaded_models[found_key]

        except FileNotFoundError:
            logger.warning("No target model file found. Using first available.")
            found_key = list(loaded_models.keys())[0]
            selected_model = loaded_models[found_key]

    # --- Define the session logic inside a nested function ---
    def session_thread_target():
        try:
            # In session_thread_target()
            model_object = selected_model
            lt_language = guess_lt_language_from_model(logger, found_key)


            recognizer = vosk.KaldiRecognizer(model_object, SAMPLE_RATE)
            logger.info(f"Using model for lang '{lt_language}'.")

            silence_timeout = PRE_RECORDING_TIMEOUT if not suspicious_events else SPEECH_PAUSE_TIMEOUT

            text_chunk_iterator = transcribe_audio_with_feedback(
                logger, recognizer, lt_language, silence_timeout, dictation_session_active, config.settings_local.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
            )

            for text_chunk in text_chunk_iterator:
                if text_chunk.strip():
                    logger.info(f"Processing chunk: '{text_chunk[:30]}...'")
                    thread = threading.Thread(target=process_text_in_background,
                                              args=(logger, lt_language, text_chunk, TMP_DIR,
                                                    time.time(), active_lt_url))
                    thread.start()

                if not dictation_session_active.is_set():
                    logger.info("Stop signal received. Gracefully exiting recording loop.")
                    break

        finally:
            logger.info("Session thread is finishing. Ensuring state is cleared.")
            finalize_recording_session(logger)
            dictation_session_active.clear()


    # --- Start the session in a new thread ---
    active_transcription_thread = threading.Thread(target=session_thread_target)
    active_transcription_thread.start()




