# File: scripts/py/func/transcribe_audio_with_feedback.py
import queue
import json
import time
from random import random

from config.settings import SILENCE_TIMEOUT, PRE_RECORDING_TIMEOUT, SAMPLE_RATE
from scripts.py.func.notify import notify
import sounddevice as sd


def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE, stop_event):
    """
    Records and transcribes audio, stopping on manual trigger, initial timeout, or silence.
    """
    q = queue.Queue()

    def audio_callback(indata, frames, time, status):
        """This function is called from a separate thread for each audio block."""
        if status:
            logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))

    recognizer.SetWords(True)

    # --- User Notification ---
    if random() > 0.5:
        notify(f"Listening {LT_LANGUAGE} ...", f"Speak now. Stops after {PRE_RECORDING_TIMEOUT}s of inactivity.", "low",
               icon="media-record", replace_tag="transcription_status")
    else:
        notify(f"Speak now.", f"Stops after {PRE_RECORDING_TIMEOUT}s of inactivity.", "low", icon="media-record",
               replace_tag="transcription_status")

    # --- State and Timer Initialization ---
    is_speech_started = False
    start_time = time.time()  # Timer for the overall PRE_RECORDING_TIMEOUT
    # This timer tracks the last moment we detected actual speech activity.
    last_speech_activity_time = time.time()

    final_text = ""
    stop_reason = "unknown"

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1,
                               callback=audio_callback):

            while not stop_event.is_set():
                # --- CHECK ALL STOP CONDITIONS ON EACH LOOP ---

                # 1. Check for initial timeout (if no speech has started yet)
                if not is_speech_started and (time.time() - start_time > PRE_RECORDING_TIMEOUT):
                    stop_reason = f"no speech detected within the initial {PRE_RECORDING_TIMEOUT}s timeout."
                    break

                # 2. Check for silence timeout (only after speech has started)
                if is_speech_started and (time.time() - last_speech_activity_time > SILENCE_TIMEOUT):
                    stop_reason = f"silence of >{SILENCE_TIMEOUT}s detected."
                    break

                # --- PROCESS AUDIO DATA FROM THE QUEUE ---
                try:
                    # Use a short, non-blocking timeout on the queue.
                    # This allows the loop to run frequently to check the stop conditions above.
                    data = q.get(timeout=0.1)
                except queue.Empty:
                    # No audio data in the queue, just continue to the next loop iteration
                    # to check the stop conditions again.
                    continue

                # We have audio data, now feed it to the recognizer
                if recognizer.AcceptWaveform(data):
                    # The recognizer detected a definitive end of an utterance.
                    # We can treat this like a silence timeout.
                    # Update the last speech time to ensure the loop exits cleanly on the next iteration.
                    last_speech_activity_time = 0

                    # Check for a partial result to see if the user is speaking
                partial_result = json.loads(recognizer.PartialResult())
                if partial_result.get('partial'):
                    # Speech is happening!

                    # If this is the first time we've heard speech, update our state.
                    if not is_speech_started:
                        is_speech_started = True
                        logger.info("Speech detected. Switching to SILENCE_TIMEOUT logic.")
                        notify("Listening...", "I can hear you now!", "low", duration=2000,
                               replace_tag="transcription_status")

                    # Crucially, update the timer every time we detect speech activity.
                    last_speech_activity_time = time.time()

            # --- LOOP HAS ENDED, DETERMINE WHY ---
            if stop_event.is_set():
                logger.info("⏹️ Recording stopped by manual trigger.")
            else:
                logger.info(f"⏳ Recording stopped: {stop_reason}")

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""  # Return empty string on error
    finally:
        # Always get the final result from the recognizer
        result_json = json.loads(recognizer.FinalResult())
        final_text = result_json.get('text', '')

        logger.info(f"Final recognized text: '{final_text}'")

        return final_text