# file: scripts/py/func/transcribe_audio_with_feedback.py

import queue
import json
import time
from pathlib import Path
import os

import numpy as np
from config.settings import SAMPLE_RATE
from .notify import notify
from .audio_manager import mute_microphone, unmute_microphone
from .manage_audio_routing import manage_audio_routing
from .log_memory_details import log4DEV
import sounddevice as sd

import webrtcvad  # NEU: Import für Voice Activity Detection
from scripts.py.func.audio_manager import speak_inclusive_fallback


import platform

from .config.dynamic_settings import DynamicSettings
# from ..config.dynamic_settings import DynamicSettings
settings = DynamicSettings()


# WAKE_PHANTOM

# Aktuell in Tübingen sind es 12 Grad, gefühlt wie 12 Grad. Die Vorhersage meldet: Leicht Bewölkt.
# sys.path.insert(0, str(PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE"))

# from Path(PROJECT_ROOT / "config" / "maps" / "plugins" / "internals" / "de-DE" / "aura_constants") import WAKE_PHANTOM

# import importlib
# TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
# PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
# PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
# aura_constants_path = Path(PROJECT_ROOT) / "config" / "maps" / "plugins" / "internals" / "de-DE" / "aura_constants.py"
# aura_constants_spec = importlib.util.spec_from_file_location("aura_constants_dyn", aura_constants_path)
# aura_constants_module = importlib.util.module_from_spec(aura_constants_spec)
# aura_constants_spec.loader.exec_module(aura_constants_module)
# WAKE_PHANTOM = getattr(aura_constants_module, "WAKE_PHANTOM")


# import importlib.util
# TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
# PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
# PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
# aura_constants_path = Path(PROJECT_ROOT) / "config" / "maps" / "plugins" / "internals" / "de-DE" / "aura_constants.py"
# aura_constants_spec = importlib.util.spec_from_file_location(aura_constants_path, aura_constants_path)
# aura_constants_module = importlib.util.module_from_spec(aura_constants_spec)
# WAKE_PHANTOM = getattr(aura_constants_module, "WAKE_PHANTOM")

#
# import runpy
# TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
# prf = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
# PROJECT_ROOT = Path(prf.read_text(encoding="utf-8"))
# acp = Path(PROJECT_ROOT) / "config" / "maps" / "plugins" / "internals" / "de-DE" / "aura_constants.py"
# WAKE_PHANTOM = runpy.run_path(acp)["WAKE_PHANTOM"]
#
# TMP_DIR = Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")
# PROJECT_ROOT_FILE = TMP_DIR / "sl5_aura" / "sl5net_aura_project_root"
# PROJECT_ROOT = Path(PROJECT_ROOT_FILE.read_text(encoding="utf-8"))
# aura_constants_path = Path(PROJECT_ROOT) / "config" / "maps" / "plugins" / "internals" / "de-DE" / "aura_constants.py"
# WAKE_PHANTOM = (lambda p, n: (lambda m: getattr(m, n))(
#     (lambda s: (lambda mod: (s.loader.exec_module(mod), mod)[1])(importlib.util.module_from_spec(s)))(
#         importlib.util.spec_from_file_location(p.stem, p)
#     )
# ))(aura_constants_path, "WAKE_PHANTOM")

import runpy
PROJECT_ROOT = Path("C:/tmp" if platform.system()=="Windows" else "/tmp")/"sl5_aura"/"sl5net_aura_project_root"


acp = PROJECT_ROOT / "config" / "maps"/"plugins"/"internals"/"de-DE"/"aura_constants.py"
WAKE_PHANTOM = runpy.run_path(acp)["WAKE_PHANTOM"]



global AUTO_ENTER_AFTER_DICTATION_global  # noqa: F824
# Kann man das auch schöner schreibenJetzt immer wachOkay gutAktuell in Tübingen sind es 12 Grad, gefühlt wie 12 Grad. Die Vorhersage meldet: Leicht Bewölkt.
#

# 2. Logic for 48kHz to 16kHz
NATIVE_RATE = 48000
VOSK_RATE = 16000


# def manage_audio_routing(mode):
#     """
#     Automates the pactl commands based on the selected mode.
#     """
#     # Always attempt to clean up existing virtual modules first to avoid duplicates
#     subprocess.run(["pactl", "unload-module", "module-loopback"], capture_output=True)
#     subprocess.run(["pactl", "unload-module", "module-null-sink"], capture_output=True)
#
#     if mode == 'MIC_AND_DESKTOP':
#         # 1. Create the virtual sink
#         subprocess.run(["pactl", "load-module", "module-null-sink", "sink_name=mic_and_desktop_Sink"], check=True)
#         # 2. Route Microphone to the virtual sink
#         subprocess.run(["pactl", "load-module", "module-loopback", "source=@DEFAULT_SOURCE@", "sink=mic_and_desktop_Sink"], check=True)
#         # 3. Route Desktop Audio (Monitor) to the virtual sink
#         # Note: Replace '60' with the dynamic detection or the confirmed ID for your desktop monitor
#         subprocess.run(["pactl", "load-module", "module-loopback", "source=60", "sink=mic_and_desktop_Sink"], check=True)




def _handle_final_result(recognizer, logger):
    result = json.loads(recognizer.Result())
    text = result.get('text')
    if text:
        logger.info(f"________________________________ {text} __________________________________________")
        logger.info(f"📢📢📢 ######################### {text} ##########################################")
        logger.info("📢📢📢             🎙️ 🎤 ")
        logger.info(f"📢📢📢-----> Yielding chunk: 📢 {text}")
        return text
    return None




def _get_downsampled_data2(raw_data, input_rate):
    """Converts raw queue data to 16kHz PCM if needed.
    Sie erscheinen namentlich nur in PulseAudio/PipeWire-Tools (pavucontrol, pactl, pw-top).

    In sounddevice (ALSA) erscheinen sie fast nie als eigene Einträge, sondern sind „versteckt“ hinter den generischen Brücken-Geräten:
    Device 8 (pipewire)
    Device 9 (pulse)
    Device 10 (default)

    """
    if input_rate == 48000:
        audio_np = np.frombuffer(raw_data, dtype=np.int16)
        # return audio_np[::3].tobytes() ; alt. 2026-0101-1137
        data = audio_np[::3, 0].tobytes()  # Nur linker Kanal, jedes 3. Sample
        return data
    return raw_data

# py/func/transcribe_audio_with_feedback.py:47
def _get_downsampled_data(raw_data, input_rate, logger):
    if input_rate == 48000:

        # Im Test (1.1.'26 13:04 Thu) war die Lösung B mit dem Headset deutlich besser.

        # Lösung B:
        # version before: 1.1.'26 12:19 Thu
        # funktioniert aber ist kein echtes mono:
        logger.debug("Downsampling 48kHz Stereo to 16kHz Mono")
        audio_np = np.frombuffer(raw_data, dtype=np.int16)
        return audio_np[::3].tobytes()

        # Lösung A:
        # 1. Von Bytes zu Stereo-Array (2 Kanäle) .... neer versuch mit mono 1.1.'26 12:45 Thu
        audio_np = np.frombuffer(raw_data, dtype=np.int16).reshape(-1, 2)
        return audio_np[::3, 0].tobytes()

        # return data

        #  noqa: F841
        comments = """
Lösung A (reshape) vermutlich technisch besser? #  noqa:
Warum?
Bei Lösung B springst du im Zeitverlauf zwischen linkem und rechtem Kanal hin und her (L0, R1, L3, R4...).
Das erzeugt Phasenfehler und Verzerrungen.
Die Fehlerquote steigt, wenn links und rechts unterschiedliche Signale liegen (z. B. Stimme links, Musik rechts).
Lösung A ist nimmst nur einen Kanal (Links).
Wichtig: Bleib bei channels=2 im RawInputStream, sonst stürzt Lösung A mit einem Fehler ab!
        """
        comments2 = comments # noqa: F841

        # 1. Von Bytes zu Stereo-Array (2 Kanäle)
        audio_np = np.frombuffer(raw_data, dtype=np.int16).reshape(-1, 2)
        # 2. Nur linken Kanal [:, 0] nehmen & jedes 3. Sample [::3]
        return audio_np[::3, 0].tobytes()

    else:
        # happen when now input some times 3.1.'26 05:57 Sat.

        log4DEV(f'transcribe_audio_with_feedback.py:86 input_rate: {input_rate}',logger)
        return raw_data
        # data = raw_data
def _get_audio_data(q, input_rate):
    """Fetches and downsamples audio if necessary."""
    try:
        raw_data = q.get(timeout=0.1)
        if input_rate == 48000:
            return np.frombuffer(raw_data, dtype=np.int16)[::3].tobytes()
        return raw_data
    except queue.Empty:
        return None


def _is_voice_active2(data, vad, frame_bytes):
    """Checks a 16kHz chunk for voice activity."""
    for i in range(0, len(data), frame_bytes):
        frame = data[i:i + frame_bytes]
        if len(frame) == frame_bytes and vad.is_speech(frame, 16000):
            return True
    return False


def _is_voice_active(data, vad, frame_bytes, SAMPLE_RATE):
    for i in range(0, len(data), frame_bytes):
        frame = data[i:i + frame_bytes]
        if len(frame) == frame_bytes:
            if vad.is_speech(frame, SAMPLE_RATE):
                return True
    return False


def get_device_id(device_setting, logger):
    # examples: None, MIC_AND_DESKTOP
    if device_setting is None:
        logger.info('transcribe_audio_with_feedback.py:110 get_device_id: device_setting is None')
        return None  # System-Default

    # 1. Dynamisch die ID der Brücke finden
    devices = sd.query_devices()
    pulse_id = next((i for i, d in enumerate(devices) if 'pulse' in d['name'].lower()), None)
    if pulse_id:
        return pulse_id

    # 2. Adresse für diese Brücke festlegen
    # if settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP':
    #     os.environ["PULSE_SOURCE"] = "mic_and_desktop_Sink.monitor"
    #     device_id = pulse_id


    try:
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            if device_setting.lower() in dev['name'].lower():
                log4DEV(f'transcribe_audio_with_feedback.py: get_device_id: i: {i}',logger)
                # log4DEV("whats this?", logger)
                return i
    except (ValueError, TypeError):
        logger.info(f'ValueError: {ValueError}')
        logger.info(f'TypeError: {TypeError}')
        logger.info(f'transcribe_audio_with_feedback.py: get_device_id: device_setting: {device_setting}')
        return int(device_setting)
    return None






def transcribe_audio_with_feedback(logger, recognizer, LT_LANGUAGE
                                   , initial_silence_timeout
                                   , session_active_event
                                   , AUTO_ENTER_AFTER_DICTATION_global
                                   ):
    last_toggle = 0
    ENABLE_WAKE_WORD = False

    manage_audio_routing(settings.AUDIO_INPUT_DEVICE, logger)

    if 'AUTO_ENTER_AFTER_DICTATION_global' not in globals():
        # This checks if the global variable has been defined at all.
        # This would catch a NameError before it happens.
        logger.warning("AUTO_ENTER_AFTER_DICTATION_global is not defined in the global scope.")

    unmute_microphone()

    # settings are read via DynamicSettings (settings object), which supports live reload
    initial_silence_timeout = settings.PRE_RECORDING_TIMEOUT
    SPEECH_PAUSE_TIMEOUT = settings.SPEECH_PAUSE_TIMEOUT
    ENABLE_WAKE_WORD = settings.ENABLE_WAKE_WORD
    AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = settings.AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
    if AUTO_ENTER_AFTER_DICTATION_REGEX_APPS != AUTO_ENTER_AFTER_DICTATION_global:
        AUTO_ENTER_AFTER_DICTATION_global = AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
        AUTO_ENTER_FLAG_FILE = Path("/tmp/sl5_aura/sl5_auto_enter.flag")
        with open(AUTO_ENTER_FLAG_FILE, "w") as flag_f:
            flag_f.write(str(AUTO_ENTER_AFTER_DICTATION_REGEX_APPS))
        logger.info(f"AUTO_ENTER_AFTER_DICTATION_REGEX_APPS written to {AUTO_ENTER_FLAG_FILE}: {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")
    logger.info(f"initial_timeout , timeout: {initial_silence_timeout} , {SPEECH_PAUSE_TIMEOUT}")
    logger.info(f"AUTO_ENTER_AFTER_DICTATION_REGEX_APPS = {AUTO_ENTER_AFTER_DICTATION_REGEX_APPS}")

    # scripts/py/func/transcribe_audio_with_feedback.py:262
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

    def audio_callback(indata, frames, time2, status):
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
    # Bestimme die Input-Rate basierend auf dem Device
    # py/func/transcribe_audio_with_feedback.py:215
    if settings.AUDIO_INPUT_DEVICE == 'MIC_AND_DESKTOP':
        input_rate = 48000  # Native Rate für virtuelle Sinks
        device_name = 'mic_and_desktop_Sink.monitor'
        os.environ["PULSE_SOURCE"] = device_name
    else:
        input_rate = 16000  # Standard für Mic/Vosk
        device_name = settings.AUDIO_INPUT_DEVICE


    device_id = get_device_id(device_name,logger)
    # logger.info(f"…/py/func/transcribe_audio_with_feedback.py:224 Using 🖥️ device name: {device_name} --> device_id: {device_id}")

    # 1.2.'26 11:53 Sun: erhöhe den blocksize Parameter auf z.B. 16000 oder 24000
    # 1.2.'26 11:53 Sun: was 4800 > 10600

    try:
        with sd.RawInputStream(samplerate=input_rate, blocksize=10600,
                               dtype='int16', channels=1, device=device_id,
                               callback=audio_callback):
            logger.info(f"Dictation Session started. Initial timeout: {current_timeout}s.")
            graceful_shutdown_initiated = False
            transcribe_audio_with_feedback._debug_count = 0
            while True:
                try:

                    if not hasattr(transcribe_audio_with_feedback, '_debug_count'):
                        transcribe_audio_with_feedback._debug_count = 0

                    listen_persistent_flag = (Path("C:/tmp") if platform.system() == "Windows" else Path(
                        "/tmp")) / "sl5_aura" / "aura_vosk_listen_persistent.flag"

                    is_listen_persistent = listen_persistent_flag.exists()

                    logger.debug(f"Loop Top | Active: {session_active_event.is_set()} | Time Since Activity: {time.time() - last_activity_time:.2f}s")
                    try:

                        # py/func/transcribe_audio_with_feedback.py:242
                        raw_data = q.get(timeout=0.1)
                        data = _get_downsampled_data(raw_data, input_rate,logger)
                        # is_voice_active_in_chunk = _is_voice_active(data, vad, FRAME_BYTES,SAMPLE_RATE)
                        is_voice_active_in_chunk = _is_voice_active(data, vad, FRAME_BYTES,16000)
                        # rms = np.sqrt(np.mean(np.frombuffer(data, dtype=np.int16).astype(np.float32) ** 2))
                        # if transcribe_audio_with_feedback._debug_count % 20 == 0:
                        #     logger.info(f"DEBUG: RMS={rms:.2f} | Rate={input_rate}")

                        # scripts/py/func/transcribe_audio_with_feedback.py:362
                        # is_listen_persistent verwenden?


                        suspend_flag = (Path("C:/tmp") if platform.system() == "Windows" else Path("/tmp")) / "sl5_aura" / "aura_vosk_suspended.flag"
                        is_suspended = suspend_flag.exists()
                        if not ENABLE_WAKE_WORD and is_suspended:
                            continue
                        is_speech_finalized = recognizer.AcceptWaveform(data)

                        # 2. SOFORT das Partial Result prüfen (Wichtig für Wake-Words!)

                        # if not vad.is_speech(frame):
                        #     continue

                        partial_result = json.loads(recognizer.PartialResult())
                        partial_text = partial_result.get('partial', '').lower()

                        suspend_flag = (Path("C:/tmp") if platform.system() == "Windows" else Path(
                            "/tmp")) / "sl5_aura" / "aura_vosk_suspended.flag"
                        is_suspended = suspend_flag.exists()


                        #

                        #Wie ist das bitteWie ist das bitteAktuell in Tübingen sind es 0 Grad, gefühlt wie -0 Grad. Die Vorhersage meldet: Wolkenlos.
                        modus = 'toggle'
                        if modus == 'toggle' and ENABLE_WAKE_WORD:

                            WAKE_WORD = 'teleskop'


                            if any(w in partial_text.lower() for w in [WAKE_WORD, "tedesco", "cellist", "tennis" ]):
                                if time.time() - last_toggle > 2.0:  # 2 sec cooldown
                                    last_toggle = time.time()
                                    if is_suspended:
                                        suspend_flag.unlink(missing_ok=True)  # WAKE UP
                                        listen_persistent_flag.touch()
                                        logger.info("🚀 System ACTIVE (wake) — persistent listening enabled")
                                        # logger.info("🚀 System ACTIVE")
                                        speak_inclusive_fallback("Wake-Word", 'en-US')
                                    else:
                                        suspend_flag.touch()  # GO TO SLEEP
                                        logger.info("💤 System SUSPENDED")
                                        speak_inclusive_fallback("System SUSPENDED", 'en-US')
                                    recognizer.Reset()

                                    # Sofort weitermachen (kein Yield nötig, oder "Bin wach" sagen)
                                    last_activity_time = time.time()

                                    # speak_fallback(f"Wake-Word", 'de-DE')

                                    continue


                            if is_listen_persistent:
                                # TODO: how long nobody has spoken?

                                if time.time() - last_activity_time > 5.0 and len(partial_text.lower()) < len(WAKE_WORD):
                                    recognizer.Reset()
                                    continue


                                if any(w in partial_text.lower() for w in WAKE_PHANTOM):

                                    #if any(w in partial_text.lower() for w in
                                    #       ["einen"]):
                                    # partial_text = partial_text.replace("einen", "").strip()
                                    recognizer.Reset()
                                    continue



                        # Wenn wir im "Warte-Modus" sind (z.B. durch dein suspend_flag geprüft)
                        # Einen BantusMein nächstes Wetter
                        if is_suspended and ENABLE_WAKE_WORD:
                            # Wir prüfen sofort das Teilergebnis auf das Wake-Word 🌵
                            # "kakturs" oder "teleskop" - je nachdem wie du es aussprichst 🌵

                            if modus == 'remove suspend_flag only': # when using this mode: you need rules for start sleeping. mabe there: config/maps/wake-up/de-DE/FUZZY_MAP_pre.py:31
                                # 🌵
                                if "kakturs" in partial_text.lower() or "teleskop" in partial_text.lower():
                                    logger.info("🚀 Wake-Word erkannt! Aktiviere System...")

                                    # Flag-Datei löschen, damit das System wieder normal arbeitet
                                    suspend_flag.unlink(missing_ok=True)

                                    # WICHTIG: Recognizer resetten, damit das Wake-Word
                                    # nicht in die nächste Text-Ausgabe rutscht
                                    recognizer.Reset()

                                    # Sofort weitermachen (kein Yield nötig, oder "Bin wach" sagen)
                                    last_activity_time = time.time()

                                    # speak_fallback(f"Wake-Word", 'de-DE')
                                    speak_inclusive_fallback("Wake-Word", 'en-US')

                                    continue


                        if is_speech_finalized:
                            last_activity_time = time.time()
                            text = _handle_final_result(recognizer, logger)
                            if text:
                                yield text
                        else:
                            #partial_result = json.loads(recognizer.PartialResult())
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
                    if not is_listen_persistent and time.time() - last_activity_time > current_timeout:

                        if is_suspended:
                            # log4DEV(f"is_suspended -> dont execute -> ty sleep and wait for active command", logger)
                            last_activity_time = time.time()
                            pass
                        else:
                            logger.info(f"⏹️ Loop finished (timeout of {current_timeout:.1f}s reached).")
                            mute_microphone(logger, onlySound=True)
                            # "Mute" sound: quick down-bending tone
                            break

                except queue.Empty:
                    pass

    finally:

        # The finally block remains as is.
        logger.info("Session has ended. Yielding final safety-net chunk.")

        final_chunk = json.loads(recognizer.FinalResult())
        if final_chunk.get('text').strip():
            yield final_chunk.get('text')
