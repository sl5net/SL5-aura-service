
import queue
import json
import time
from pathlib import Path
from random import random

from config.settings import SILENCE_TIMEOUT, PRE_RECORDING_TIMEOUT, SAMPLE_RATE, TRIGGER_FILE_PATH
from scripts.py.func.notify import notify
import sounddevice as sd

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE):
    q = queue.Queue()

    manual_stop_trigger = Path(TRIGGER_FILE_PATH)

    def audio_callback(indata, frames, time, status):
        if status: logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))
    recognizer.SetWords(True)
    # media-record
    # microphone-sensitivity-high-symbolic

    if random() > 0.5:
        notify(f"Listening {LT_LANGUAGE} ...", f"Speak now. It will stop on silence of {SILENCE_TIMEOUT}ms .", "low", icon="media-record")
    else:
        notify(f"Speak now.", f"It will stop on silence of {SILENCE_TIMEOUT}ms .", "low", icon="media-record")

    is_speech_started = False
    current_timeout = PRE_RECORDING_TIMEOUT

    try:

        notify(f"try", f"...", "low", duration=1500,
               replace_tag="transcription_status")

        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            last_audio_time = time.time()


            while time.time() - last_audio_time < SILENCE_TIMEOUT:
                # --- NEW: Check for manual stop trigger at the start of every loop ---
                if manual_stop_trigger.exists():
                    logger.info("⏹️ Manual stop trigger detected. Stopping recording.")
                    manual_stop_trigger.unlink(missing_ok=True)  # Clean up the trigger file
                    break # Exit the recording loop immediately

                try:
                    data = q.get(timeout=current_timeout)
                    last_audio_time = time.time()

                    if recognizer.AcceptWaveform(data):
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial') and not is_speech_started:
                            is_speech_started = True
                            current_timeout = SILENCE_TIMEOUT
                            logger.info("Speech detected. Switched to short SILENCE_TIMEOUT.")
                        break
                except queue.Empty:
                    # This is not an error, just a timeout. The outer while-loop will check if it's time to stop.
                    pass
            # --- NEW: This block runs only if the while loop finishes naturally (due to timeout) ---
            logger.info(f"⏹️ Recording stopped due to silence timeout {current_timeout}sec.")

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""
    finally:
        return json.loads(recognizer.FinalResult()).get('text', '')

