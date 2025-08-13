# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path
import os

from config.settings import SAMPLE_RATE
from scripts.py.func.notify import notify
from scripts.py.func.audio_manager import mute_microphone, unmute_microphone
import sounddevice as sd

import webrtcvad  # NEU: Import für Voice Activity Detection

def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE
                                   , initial_silence_timeout
                                   , session_active_event
                                   ):
    unmute_microphone()

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    local_config_path = PROJECT_ROOT / "config/settings_local.py"
    default_config_path = PROJECT_ROOT / "config/settings.py"
    config_to_read = local_config_path if local_config_path.exists() else default_config_path
    try:
        with open(PROJECT_ROOT / config_to_read, "r") as f:
            for line in f:
                if line.strip().startswith("PRE_RECORDING_TIMEOUT"):
                    initial_silence_timeout = float(line.split("=")[1].strip())
                if line.strip().startswith("SPEECH_PAUSE_TIMEOUT"):
                    SPEECH_PAUSE_TIMEOUT = float(line.split("=")[1].strip())
                    break

    except (FileNotFoundError, ValueError, IndexError) as e:
        logger.warning(f"Could not read local config override ({e}), continuing with defaults.")

    logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SPEECH_PAUSE_TIMEOUT}")

    # --- NEU: VAD Initialisierung ---
    vad = webrtcvad.Vad()
    vad.set_mode(1)  # Wir starten mit dem sanftesten Modus (weniger aggressiv)
    FRAME_DURATION_MS = 30  # VAD arbeitet am besten mit 10, 20 oder 30 ms Frames
    FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)
    FRAME_BYTES = FRAME_SIZE * 2  # int16 = 2 bytes per sample

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

    # If the script is running in a Continuous Integration environment (like GitHub Actions),
    # there is no audio hardware. We skip the entire recording part and yield a success message.
    if os.getenv('CI'):
        logger.info("CI environment detected. Skipping microphone-dependent recording.")
        logger.info("Yielding a test string to signal success.")
        yield "CI_TEST_SUCCESS"
        return # Wichtig: Beendet die Funktion hier, damit der restliche Code nicht ausgeführt wird.

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

                    # --- MODIFIZIERT: Voice Activity Detection mit webrtcvad ---
                    # Wir prüfen den Audio-Chunk mit VAD, bevor wir ihn an Vosk geben.
                    is_voice_active_in_chunk = False
                    # Wir müssen den Chunk in VAD-kompatible Frames aufteilen
                    for i in range(0, len(data), FRAME_BYTES):
                        frame = data[i:i + FRAME_BYTES]
                        if len(frame) == FRAME_BYTES:
                            if vad.is_speech(frame, SAMPLE_RATE):
                                is_voice_active_in_chunk = True
                                break  # Stimme gefunden, Rest des Chunks irrelevant

                    # Wir füttern die Daten immer an Vosk für die Transkription
                    is_speech_finalized = recognizer.AcceptWaveform(data)

                    if is_speech_finalized:
                        last_activity_time = time.time()  # Aktivität bei finalem Ergebnis
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"             🎙️ 🎤 ")
                            logger.info(f"---> Yielding chunk: '{result['text']}'")
                            yield result['text']
                    else:
                        partial_result = json.loads(recognizer.PartialResult())
                        # Aktivität, wenn VAD Stimme erkennt ODER Vosk ein Teilergebnis hat
                        if is_voice_active_in_chunk or partial_result.get('partial'):
                            last_activity_time = time.time()  # Aktivität erkannt, Timer zurücksetzen

                    # Timeout-change wehen first activity
                    if not is_speech_started and (is_voice_active_in_chunk or partial_result.get('partial')):
                        is_speech_started = True
                        current_timeout = SPEECH_PAUSE_TIMEOUT
                        logger.info(f"Speech detected. Switched to main SPEECH_PAUSE_TIMEOUT: {current_timeout}s.")

                except queue.Empty:
                    pass

                    # --- Exit-Logik using VAD-Modus-Wechsel as fallback and also mute_microphone ---

                    # 1. Prüfen, ob manueller Stopp angefordert wurde
                    if not session_active_event.is_set() and not graceful_shutdown_initiated:

                        success = mute_microphone()
                        if success:
                            logger.info("--- Test action completed. ---")

                        logger.info("Manual stop detected. Resetting activity clock for graceful shutdown.")

                        # --- HIER IST DIE GEWÜNSCHTE ÄNDERUNG ---
                        logger.info("Switching VAD mode to 1 (aggressive) for final voice detection.")
                        vad.set_mode(1)
                        # --- ENDE DER ÄNDERUNG ---

                        last_activity_time = time.time()
                        graceful_shutdown_initiated = True

                        if current_timeout > 2:
                            current_timeout = 2.0
                        logger.info(f"Graceful shutdown initiated. Final timeout set to {current_timeout}s.")

                    # 2. Prüfen auf Timeout
                    if time.time() - last_activity_time > current_timeout:
                        logger.info(f"⏹️ Loop finished (timeout of {current_timeout:.1f}s reached).")
                        break

    finally:
        # The finally block remains as is.
        logger.info("Session has ended. Yielding final safety-net chunk.")
        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text'):
            yield final_chunk.get('text')
