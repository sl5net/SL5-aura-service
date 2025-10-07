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

global AUTO_ENTER_AFTER_DICTATION_global  # noqa: F824



def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE
                                   , initial_silence_timeout
                                   , session_active_event
                                   , AUTO_ENTER_AFTER_DICTATION_global
                                   ):

    if 'AUTO_ENTER_AFTER_DICTATION_global' not in globals():
        # This checks if the global variable has been defined at all.
        # This would catch a NameError before it happens.
        logger.warning(f"AUTO_ENTER_AFTER_DICTATION_global is not defined in the global scope.")


    unmute_microphone()

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
    local_config_path = PROJECT_ROOT / "config/settings_local.py"
    default_config_path = PROJECT_ROOT / "config/settings.py"
    config_to_read = local_config_path if local_config_path.exists() else default_config_path

    try:
        with open(PROJECT_ROOT / config_to_read, "r") as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line.startswith("PRE_RECORDING_TIMEOUT"):
                    initial_silence_timeout = float(line.split("=")[1].strip())
                elif stripped_line.startswith("SPEECH_PAUSE_TIMEOUT"):
                    SPEECH_PAUSE_TIMEOUT = float(line.split("=")[1].strip())
                elif stripped_line.startswith("AUTO_ENTER_AFTER_DICTATION_REGEX_APPS"): # 1 means one Enter, 2 means Enter two times
                    value_without_whitespaces = str(line.split("=")[1].strip())
                    value_without_quotes = value_without_whitespaces.strip('"')
                    AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = value_without_quotes

                    if AUTO_ENTER_AFTER_DICTATION_REGEX_APPS != AUTO_ENTER_AFTER_DICTATION_global:
                        logger.info(f"{AUTO_ENTER_AFTER_DICTATION_REGEX_APPS} != {AUTO_ENTER_AFTER_DICTATION_global} =====> Updated AUTO_ENTER_AFTER_DICTATION_REGEX_APPS: =====> {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")
                        logger.info(f"{AUTO_ENTER_AFTER_DICTATION_REGEX_APPS} != {AUTO_ENTER_AFTER_DICTATION_global} =====> Updated AUTO_ENTER_AFTER_DICTATION_REGEX_APPS: =====> {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")
                        logger.info(f"{AUTO_ENTER_AFTER_DICTATION_REGEX_APPS} != {AUTO_ENTER_AFTER_DICTATION_global} =====> Updated AUTO_ENTER_AFTER_DICTATION_REGEX_APPS: =====> {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")
                        logger.info(f"{AUTO_ENTER_AFTER_DICTATION_REGEX_APPS} != {AUTO_ENTER_AFTER_DICTATION_global} =====> Updated AUTO_ENTER_AFTER_DICTATION_REGEX_APPS: =====> {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")
                        # global AUTO_ENTER_AFTER_DICTATION_global
                        AUTO_ENTER_AFTER_DICTATION_global = AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
                        # Define the path for the AutoEnter flag file
                        AUTO_ENTER_FLAG_FILE = Path("/tmp/sl5_auto_enter.flag")
                        with open(AUTO_ENTER_FLAG_FILE, "w") as flag_f:
                            flag_f.write(str(AUTO_ENTER_AFTER_DICTATION_REGEX_APPS))
                        logger.info(f"AUTO_ENTER_AFTER_DICTATION_REGEX_APPS written to {AUTO_ENTER_FLAG_FILE}: {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")


    except (FileNotFoundError, ValueError, IndexError) as e:
        logger.warning(f"Could not read local config override ({e}), continuing with defaults.")
    except Exception as e:
        logger.warning(f"warning: {e}")

    logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SPEECH_PAUSE_TIMEOUT}")
    logger.info(f"AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")

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
        yield ""
        return


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

                    # --- MODIFIEd: Voice Activity Detection mit webrtcvad ---
                    # we proof Audio-Chunk with VAD, before send to Vosk
                    is_voice_active_in_chunk = False
                    # must be splitted in Chunk VAD-kompatible Frames
                    for i in range(0, len(data), FRAME_BYTES):
                        frame = data[i:i + FRAME_BYTES]
                        if len(frame) == FRAME_BYTES:
                            if vad.is_speech(frame, SAMPLE_RATE):
                                is_voice_active_in_chunk = True
                                break  # voice found, rest of Chunks irrelevant

                    # Wir füttern die Daten immer an Vosk für die Transkription
                    is_speech_finalized = recognizer.AcceptWaveform(data)

                    if is_speech_finalized:
                        last_activity_time = time.time()  # Aktivität bei finalem Ergebnis
                        result = json.loads(recognizer.Result())
                        if result.get('text'):
                            logger.info(f"📢📢📢             🎙️ 🎤 ")
                            logger.info(f"📢📢📢             🎙️ 🎤 ")
                            logger.info(f"📢📢📢-----> Yielding chunk: 📢 {result['text']}'")
                            yield result['text']
                    else:
                        partial_result = json.loads(recognizer.PartialResult())
                        # Aktivität, wenn VAD Stimme erkennt ODER Vosk ein Teilergebnis hat
                        if is_voice_active_in_chunk or partial_result.get('partial'):
                            last_activity_time = time.time()  # Aktivität erkannt, Timer zurücksetzen

                    # Timeout-change when first activity
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

                        mute_microphone(logger, onlySound=True)
                        # "Mute" sound: quick down-bending tone

                        break

    finally:

        # The finally block remains as is.
        logger.info("Session has ended. Yielding final safety-net chunk.")

        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text').strip():
            yield final_chunk.get('text')
