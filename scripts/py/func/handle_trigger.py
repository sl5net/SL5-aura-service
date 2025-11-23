# scripts/py/func/handle_trigger.py


# flake8: noqa: F821, F401, F811, F403
# F821: Undefined name (Accepting Closure access to handle_trigger arguments)

import threading
import time
import vosk

from config.dynamic_settings import settings
from config.settings import PRE_RECORDING_TIMEOUT, SPEECH_PAUSE_TIMEOUT, SAMPLE_RATE

from .model_manager import MODELS_LOCK

# In scripts/py/func/handle_trigger.py
dictation_session_active = threading.Event()
active_transcription_thread = None

from scripts.py.func.process_text_in_background import process_text_in_background
from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
from scripts.py.func.guess_lt_language_from_model import guess_lt_language_from_model
from scripts.py.func.audio_manager import unmute_microphone, mute_microphone
from scripts.py.func.microphone_status_too_log import log_microphone_status

from .global_state import SEQUENCE_LOCK, SESSION_LAST_PROCESSED
# Global sequence counter for the current session (must be synchronized)

global text_detected

# File: scripts/py/func/handle_trigger.py

# ... existing imports

# Global sequence counter for the current session (must be synchronized)
global session_chunk_counter
session_chunk_counter = 0



# --- Define the session logic inside a nested function ---
def session_thread_target():
    global session_chunk_counter
    session_id = None
    lt_language = 'unknown'

    try:
        # Initialize session counter
        with SEQUENCE_LOCK:
            SESSION_LAST_PROCESSED[session_id] = 0
            session_chunk_counter = 0  # Reset for this new session


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
            logger.info(f"Model for '{target_model_name}' not ready. Using first available.")
            found_key = list(loaded_models.keys())[0]
            selected_model = loaded_models[found_key]
            logger.info(f"Model selected '{selected_model}'.")

    except FileNotFoundError:
        logger.warning("No target model file found. Using first available.")
        found_key = list(loaded_models.keys())[0]
        selected_model = loaded_models[found_key]

        text_chunk_iterator = transcribe_audio_with_feedback(...)

        for text_chunk in text_chunk_iterator:
            if text_chunk.strip():
                # text_detected = 1

                # --- CRITICAL: ASSIGN SEQUENCE ID AND START THREAD ---
                with SEQUENCE_LOCK:
                    session_chunk_counter += 1
                    current_chunk_id = session_chunk_counter

                if settings.DEV_MODE:
                    logger.info(f"Chunk ID {current_chunk_id}: Starting processing for '{text_chunk[:30]}...'")

                # Start the thread as before, but pass the ID and Session ID
                thread = threading.Thread(
                    target=process_text_in_background,
                    args=(logger, lt_language, text_chunk, TMP_DIR,
                          time.time(), active_lt_url, None,  # Existing arguments
                          current_chunk_id, session_id)
                )
                thread.start()

            if not dictation_session_active.is_set():
                logger.info("Stop signal received. Gracefully exiting recording loop.")
                break

    finally:
        # --- CLEANUP LOCK STATE ---
        if session_id is not None:
            with SEQUENCE_LOCK:
                if session_id in SESSION_LAST_PROCESSED:
                    del SESSION_LAST_PROCESSED[session_id]
            # Note: We keep OUT_OF_ORDER_CACHE items until they time out/are picked up


def finalize_recording_session(logger):
    """A dedicated function to clean up after a recording session."""
    global active_transcription_thread

    if settings.DEV_MODE:
        logger.info("Finalizing recording session: All new audio intake has stopped.")

    # Set the global thread variable to None to indicate no active session.
    active_transcription_thread = None




def handle_trigger(
    # scripts/py/func/handle_trigger.py:38
        logger,
        loaded_models,
        suspicious_events,
        project_root,
        TMP_DIR,
        recording_time,
        active_lt_url
, session_id=None):
    global active_transcription_thread

    # --- ACTION 1: STOP an ongoing session ---
    if dictation_session_active.is_set():
        logger.info("🎬⏹️ Manual stop trigger detected. Signaling session to end.")
        mute_microphone()
        # unmute_microphone()


        # We just send the signal and exit immediately.
        # We DO NOT wait here for the thread to finish. This prevents
        # blocking and queuing of subsequent trigger events.

        # logger.info(f"text_detected: {text_detected}")

        dictation_session_active.clear()

        return


    # --- ACTION 2: START a new session ---

    unmute_microphone()

    session_id = object() # Wir verwenden ein Dummy-Objekt als einzigartige ID

    logger.info("🎬🏁 Trigger received. Starting new dictation session.")
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
                logger.info(f"Model for '{target_model_name}' not ready. Using first available.")
                found_key = list(loaded_models.keys())[0]
                selected_model = loaded_models[found_key]
                logger.info(f"Model selected '{selected_model}'.")

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

            global text_detected
            text_detected = 0

            text_chunk_iterator = transcribe_audio_with_feedback(
                logger, recognizer, lt_language, silence_timeout, dictation_session_active, settings.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
            )

            for text_chunk in text_chunk_iterator:
                if text_chunk.strip():
                    text_detected = 1
                    if settings.DEV_MODE:
                        logger.info(f"Processing chunk: '{text_chunk[:30]}...'")
                    thread = threading.Thread(target=process_text_in_background,
                                              args=(logger, lt_language, text_chunk, TMP_DIR,
                                                    time.time(), active_lt_url))
                    thread.start()

                if not dictation_session_active.is_set():
                    logger.info("Stop signal received. Gracefully exiting recording loop.")
                    break

            if text_detected < 1:
                # maybe user now need help to configure his mic
                # maybe times for following code:
                temp = """
                    sd.query_devices(): ~1–10ms
                    loop + Logging: ~1–5ms
                    get Standard - Device: ~1–5ms
                    Logging: < 1ms
                    """
                temp = "🎤"
                logger.info(f"🎤 just for information: input channels: {temp}")

                log_microphone_status(logger)

                # devices = sd.query_devices()
                # for idx, device in enumerate(devices):
                #     logger.info(f"🎤 {idx}: {device['name']} (input channels: {device['max_input_channels']}){temp}")
                # # Standard-Input-Device check:
                # default_input_index = sd.default.device[0]
                # default_input_device = sd.query_devices(default_input_index)
                # logger.info(f"🎤Standard: {default_input_device['name']} (Index: {default_input_index})")




        finally:
            # --- CLEANUP LOCK STATE ---
            if session_id is not None:
                with SEQUENCE_LOCK:
                    if session_id in SESSION_LAST_PROCESSED:
                        del SESSION_LAST_PROCESSED[session_id]
                # Note: We keep OUT_OF_ORDER_CACHE items until they time out/are picked up

            if settings.DEV_MODE:
                logger.info(f"Session thread is finishing. Ensuring state is cleared. text_detected.")
            finalize_recording_session(logger)
            dictation_session_active.clear()

    # --- Start the session in a new thread ---
    active_transcription_thread=threading.Thread(target=session_thread_target)
    active_transcription_thread.start()




