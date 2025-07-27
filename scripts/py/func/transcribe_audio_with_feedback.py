# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path

from config.settings import SAMPLE_RATE, TRIGGER_FILE_PATH, SILENCE_TIMEOUT
from scripts.py.func.notify import notify
import sounddevice as sd


# MODIFIED: This function is now a generator, using 'yield' to stream results.
def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE, initial_silence_timeout):
    q = queue.Queue()
    manual_stop_trigger = Path(TRIGGER_FILE_PATH)

    def audio_callback(indata, frames, time, status):
        if status: logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))

    recognizer.SetWords(True)
    notify(f"Listening {LT_LANGUAGE}...", "Speak now. Will stop on silence.", "low", icon="media-record",
           replace_tag="transcription_status")

    is_speech_started = False
    current_timeout = initial_silence_timeout

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1,
                               callback=audio_callback):
            logger.info(f"Dictation Session started. Initial timeout: {current_timeout}s.")

            while True:
                if manual_stop_trigger.exists():
                    logger.info("⏹️ Manual stop trigger detected. Ending session.")
                    manual_stop_trigger.unlink(missing_ok=True)
                    break
                try:
                    data = q.get(timeout=current_timeout)

                    if recognizer.AcceptWaveform(data):
                        # NEW: When VOSK has a result, yield it immediately.
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"--> Yielding chunk: '{result['text']}'")
                            yield result['text']

                    if not is_speech_started:
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial'):
                            is_speech_started = True
                            current_timeout = SILENCE_TIMEOUT
                            logger.info(f"Speech detected. Switched to main SILENCE_TIMEOUT: {current_timeout}s.")
                except queue.Empty:
                    logger.info(f"⏹️ Silence detected for {current_timeout}s. Ending session.")
                    break
    finally:
        # NEW: Always process and yield the final text in the buffer.
        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text'):
            logger.info(f"--> Yielding final chunk: '{final_chunk['text']}'")
            yield final_chunk.get('text')