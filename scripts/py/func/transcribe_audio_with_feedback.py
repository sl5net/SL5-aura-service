# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path

from config.settings import SAMPLE_RATE
from scripts.py.func.notify import notify
import sounddevice as sd

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE
                                   , initial_silence_timeout
                                   , session_active_event
                                   ):

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    local_config_path = PROJECT_ROOT / "config/settings_local.py"
    default_config_path = PROJECT_ROOT / "config/settings.py"
    config_to_read = local_config_path if local_config_path.exists() else default_config_path
    try:
        with open(PROJECT_ROOT / config_to_read, "r") as f:
            for line in f:
                if line.strip().startswith("PRE_RECORDING_TIMEOUT"):
                    initial_silence_timeout = float(line.split("=")[1].strip())
                if line.strip().startswith("SILENCE_TIMEOUT"):
                    SILENCE_TIMEOUT = float(line.split("=")[1].strip())
                    break

    except (FileNotFoundError, ValueError, IndexError) as e:
        logger.warning(f"Could not read local config override ({e}), continuing with defaults.")

    logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SILENCE_TIMEOUT}")

    q = queue.Queue()
    # manual_stop_trigger = Path(TRIGGER_FILE_PATH)

    # In transcribe_audio_with_feedback.py

    # ... (am Anfang der Funktion) ...
    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        """
        This function is called by the sounddevice library for each audio chunk.
        """
        if status:
            logger.warning(f"Audio status: {status}")

        # --- START OF THE CRITICAL FIX (YOUR IDEA) ---
        # If the session is supposed to be stopped, we don't stop the stream.
        # Instead, we feed it silence. This ensures a clean finalization.
        if not session_active_event.is_set():
            # Create a block of silence of the same size as the input data.
            silence = bytes(len(indata))
            q.put(silence)
        else:
            # If the session is active, put the real audio data into the queue.
            q.put(bytes(indata))
        # --- END OF THE CRITICAL FIX ---


    recognizer.SetWords(True)
    notify(f"Listening {LT_LANGUAGE}...", "Speak now. Will stop on silence.", "low", icon="media-record",
           replace_tag="transcription_status")

    is_speech_started = False
    current_timeout = initial_silence_timeout
    last_activity_time = time.time()  # Our independent activity clock.
    # session_stopped_manually = False

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000, dtype='int16', channels=1,
                               callback=audio_callback):
            logger.info(f"Dictation Session started. Initial timeout: {current_timeout}s.")

            # This flag ensures we only reset the timer once.
            graceful_shutdown_initiated = False

            while True:

                # === START: DIAGNOSTIC LOGGING ===
                logger.debug(
                    f"Loop Top | "
                    f"Active: {session_active_event.is_set()} | "
                    f"Time Since Activity: {time.time() - last_activity_time:.2f}s"
                )
                # === END: DIAGNOSTIC LOGGING ===

                try:
                    # Get data from the queue with a short timeout to keep the loop responsive.
                    data = q.get(timeout=0.1)

                    # Feed the data to Vosk and check if it's considered speech.
                    is_speech = recognizer.AcceptWaveform(data)
                    if is_speech:
                        last_activity_time = time.time()  # Reset clock
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"--> Yielding chunk: '{result['text']}'")
                            yield result['text']
                    else:
                        # Also reset clock on partial results to keep the session alive.
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial'):
                            last_activity_time = time.time()  # Reset clock

                    # Switch to the shorter timeout as soon as any speech is detected.
                    if not is_speech_started and partial_result.get('partial'):
                        is_speech_started = True
                        current_timeout = SILENCE_TIMEOUT
                        logger.info(f"Speech detected. Switched to main SILENCE_TIMEOUT: {current_timeout}s.")

                except queue.Empty:
                    pass

                # --- THIS IS THE MODIFIED EXIT LOGIC ---

                # 1. Check if a manual stop has been requested AND we haven't handled it yet.
                if not session_active_event.is_set() and not graceful_shutdown_initiated:
                    logger.info("Manual stop detected. Resetting activity clock for graceful shutdown.")
                    # THIS IS THE KEY: Manually reset the timer one last time.
                    last_activity_time = time.time()
                    graceful_shutdown_initiated = True  # Mark as handled.

                # 2. Check for timeout. This check now works correctly because the
                #    timer has been reset on manual stop.
                if time.time() - last_activity_time > current_timeout:
                    logger.info(f"⏹️ Loop finished (timeout of {current_timeout:.1f}s reached).")
                    break

    finally:
        # The finally block remains as is.
        logger.info("Session has ended. Yielding final safety-net chunk.")
        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text'):
            yield final_chunk.get('text')

