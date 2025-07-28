# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path

from config.settings import SAMPLE_RATE, TRIGGER_FILE_PATH, SILENCE_TIMEOUT
from scripts.py.func.notify import notify
import sounddevice as sd

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE, initial_silence_timeout):

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    try:
        with open(PROJECT_ROOT / "config/settings_local.py", "r") as f:
            for line in f:
                if line.strip().startswith("PRE_RECORDING_TIMEOUT"):
                    initial_silence_timeout = float(line.split("=")[1].strip())
                if line.strip().startswith("SILENCE_TIMEOUT"):
                    SILENCE_TIMEOUT = float(line.split("=")[1].strip())
                    break
    except FileNotFoundError:
        logger.warning(f"file not found 2025-0728-1339")
        pass
    except Exception as e:
        logger.warning(f"error: {e}")
        pass

    logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SILENCE_TIMEOUT}")

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
    last_activity_time = time.time()  # Our independent activity clock.
    session_stopped_manually = False

    try:
        with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=4000, dtype='int16', channels=1,
                               callback=audio_callback):
            logger.info(f"Dictation Session started. Initial timeout: {current_timeout}s.")

            # MODIFIED: The loop is now controlled by our activity clock.
            while time.time() - last_activity_time < current_timeout:
                if manual_stop_trigger.exists():
                    logger.info("⏹️ Manual stop trigger detected. Ending session.")
                    manual_stop_trigger.unlink(missing_ok=True)
                    session_stopped_manually = True
                    break
                try:
                    # We use a short timeout here just to not block the loop.
                    data = q.get(timeout=0.1)

                    # KEY CHANGE: Reset the clock if we hear anything that looks like speech.
                    is_speech = recognizer.AcceptWaveform(data)
                    if is_speech:
                        last_activity_time = time.time()  # Reset clock
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"--> Yielding chunk: '{result['text']}'")
                            yield result['text']
                    else:
                        # Also reset clock on partial results to keep session alive during speech.
                        partial_result = json.loads(recognizer.PartialResult())
                        if partial_result.get('partial'):
                            last_activity_time = time.time()  # Reset clock

                    if not is_speech_started and partial_result.get('partial'):
                        is_speech_started = True
                        current_timeout = SILENCE_TIMEOUT
                        logger.info(f"Speech detected. Switched to main SILENCE_TIMEOUT: {current_timeout}s.")
                except queue.Empty:
                    # This is now expected. The outer 'while' loop handles the actual timeout.
                    pass

            if not session_stopped_manually:
                logger.info(f"⏹️ Silence detected for {current_timeout}s. Ending session.")

    finally:
        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text'):
            logger.info(f"--> Yielding final chunk: '{final_chunk['text']}'")
            yield final_chunk.get('text')