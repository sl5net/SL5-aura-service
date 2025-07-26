
import queue
import json
import time
from random import random

from config.settings import SILENCE_TIMEOUT, PRE_RECORDING_TIMEOUT, SAMPLE_RATE
from scripts.py.func.notify import notify
import sounddevice as sd

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE):
    q = queue.Queue()
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
                try:
                    data = q.get(timeout=current_timeout)
                    last_audio_time = time.time()

                    if recognizer.AcceptWaveform(data):
                        # Check for partial result to detect speech start
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial') and not is_speech_started:
                            is_speech_started = True

                            notify(f"started={is_speech_started}", f"is_speech_started = {is_speech_started}", "low", duration=1500, replace_tag="transcription_status")

                            # NEW: Switch to the shorter timeout once speech is detected
                            current_timeout = SILENCE_TIMEOUT
                            logger.info("Speech detected. Switched to short SILENCE_TIMEOUT.")
                        break
                except queue.Empty:
                    pass
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""
    finally:
        return json.loads(recognizer.FinalResult()).get('text', '')

