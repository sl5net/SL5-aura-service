
import queue
import json
import time     
from scripts.py.func.notify import notify
from scripts.py.func.check_memory_critical import check_memory_critical
from scripts.py.func.normalize_punctuation import normalize_punctuation
import sounddevice as sd

from config.settings import SILENCE_TIMEOUT2

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE, SILENCE_TIMEOUT, SAMPLE_RATE):
    q = queue.Queue()
    def audio_callback(indata, frames, time, status):
        if status: logger.warning(f"Audio status: {status}")
        q.put(bytes(indata))
    recognizer.SetWords(True)
    notify(f"Vosk is Listening {LT_LANGUAGE} ...", "Speak now. It will stop on silence.", "normal", icon="microphone-sensitivity-high-symbolic")
    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
            last_audio_time = time.time()
            while time.time() - last_audio_time < SILENCE_TIMEOUT2:
                try:
                    data = q.get(timeout=0.3)
                    last_audio_time = time.time()
                    if recognizer.AcceptWaveform(data):
                        break
                except queue.Empty:
                    pass
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return ""
    finally:
        return json.loads(recognizer.FinalResult()).get('text', '')

