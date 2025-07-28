# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path

from config.settings import SAMPLE_RATE, TRIGGER_FILE_PATH, SILENCE_TIMEOUT
from scripts.py.func.notify import notify
import sounddevice as sd

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE
                                   , initial_silence_timeout
                                   , session_active_event
                                   ):


    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    try:
        with open(PROJECT_ROOT / "config/settings_local.py", "r") as f:
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
    session_stopped_manually = False

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000, dtype='int16', channels=1,
                               callback=audio_callback):
            logger.info(f"Dictation Session started. Initial timeout: {current_timeout}s.")

            shutdown_imminent = False







            while time.time() - last_activity_time < current_timeout:
            # while True:

                # --- Graceful Shutdown Logic ---
                # First, check if a stop has been requested.
                if not session_active_event.is_set() and not shutdown_imminent:
                    logger.info("Graceful shutdown initiated. Processing remaining audio queue...")
                    shutdown_imminent = True  # Enter shutdown mode

                try:
                    # Get data from the queue. The timeout keeps the loop responsive.
                    # If in shutdown mode, we want a very short timeout to quickly empty the queue.
                    queue_timeout = 0.05 if shutdown_imminent else 0.1
                    # data = q.get(timeout=queue_timeout)
                    data = q.get(timeout=0.1)

                    if recognizer.AcceptWaveform(data):
                        last_activity_time = time.time()  # Reset clock on full sentence
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"--> Yielding chunk: '{result['text']}'")
                            yield result['text']
                    else:
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial'):
                            last_activity_time = time.time()  # Reset clock on any speech

                    if not is_speech_started and partial_result.get('partial'):
                        is_speech_started = True
                        current_timeout = SILENCE_TIMEOUT
                        logger.info(f"Speech detected. Switched to main SILENCE_TIMEOUT: {current_timeout}s.")


                except queue.Empty:
                    pass

                    """
                    # This block is now INSIDE the while loop.
                    # If shutdown is requested and the queue is empty, finalize and exit.
                    if shutdown_imminent:
                        logger.info("Audio queue empty after stop signal. Finalizing...")
                        final_chunk2 = json.loads(recognizer.FinalResult())
                        if final_chunk2.get('text'):
                            logger.info(f"--> Yielding FINAL chunk after manual stop: '{final_chunk2['text']}'")
                            yield final_chunk2.get('text')
                            # This break is now valid because it's inside the while loop.
                        break
                    # If no shutdown, just continue the loop
                    pass
                    """

            # This message will now only be shown if the timeout is reached.

            logger.info(f"⏹️ Loop finished (likely due to timeout).")


    finally:
            # This part runs after the loop has broken, regardless of the reason.
            final_chunk = json.loads(recognizer.FinalResult())
            if final_chunk.get('text'):
                logger.info(f"--> Yielding final chunk: '{final_chunk['text']}'")
                yield final_chunk.get('text')

