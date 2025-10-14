# scripts/py/func/checks/test_dictation_session_logic.py

import unittest.mock
import wave
import time
import logging
from pathlib import Path
import vosk
import threading
import numpy as np

# sounddevice Import ist NICHT mehr nötig, da wir eigene Mocks verwenden.
# import sounddevice as sd

# Ensure the script can find the modules in the parent directory
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from scripts.py.func.transcribe_audio_with_feedback import transcribe_audio_with_feedback
from config.settings import TRIGGER_FILE_PATH, SAMPLE_RATE

# --- Basic Configuration ---
# Stelle sicher, dass dies die einzige Logging-Konfiguration ist,
# oder dass andere Konfigurationen den TypeError in dynamic_settings.py behoben haben.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MODEL_PATH = "models/vosk-model-small-en-us-0.15"
TEST_WAV_PATH = Path(__file__).resolve().parent / "test_audio_16k.wav"


# --- Eigene Mock-Klassen für CallbackTime und CallbackFlags ---
# Diese sind notwendig, da sounddevice sie nicht direkt als Top-Level-Objekte exportiert.
class MockCallbackTime:
    def __init__(self, input_buffer_dac_time=0, current_time=0, output_buffer_dac_time=0):
        self.input_buffer_dac_time = input_buffer_dac_time
        self.current_time = current_time
        self.output_buffer_dac_time = output_buffer_dac_time

    def __repr__(self):
        return f"MockCallbackTime(current_time={self.current_time})"


class MockCallbackFlags:
    # `sounddevice.CallbackFlags` ist ein `enum.IntFlag`, wir brauchen nur Basis-Funktionalität
    # für den Mock. Ein einfacher Integer reicht oft.
    input_overflow = 1  # Beispielflag
    output_underflow = 2  # Beispielflag

    def __init__(self, flags=0):
        self._flags = flags

    def __bool__(self):  # Ermöglicht `if status_flags:` Checks
        return self._flags != 0

    def __repr__(self):
        return f"MockCallbackFlags(flags={self._flags})"

    # Füge weitere Properties hinzu, falls deine `transcribe_audio_with_feedback` spezifische Flags prüft

class MockRawInputStream:
    def __init__(self, samplerate, blocksize, dtype, channels, callback):
        logging.info("MockRawInputStream: Initialized.")
        self._callback = callback
        self._samplerate = samplerate
        self._blocksize = blocksize
        self._channels = channels
        self._dtype = dtype
        self._wav_file = wave.open(str(TEST_WAV_PATH), 'rb')

        # Assertions/Checks für WAV-Datei-Kompatibilität
        if self._wav_file.getframerate() != samplerate:
            raise ValueError(
                f"WAV file sample rate mismatch: Expected {samplerate}, got {self._wav_file.getframerate()}")
        if self._wav_file.getnchannels() != channels:
            raise ValueError(f"WAV file channel mismatch: Expected {channels}, got {self._wav_file.getnchannels()}")
        # np.iinfo(dtype).bits gibt die Bittiefe des Datentyps zurück (z.B. 16 für int16)
        if self._wav_file.getsampwidth() * 8 != np.iinfo(dtype).bits:
            logging.warning(
                f"WAV file sample width mismatch with dtype: Expected {np.iinfo(dtype).bits}-bit, got {self._wav_file.getsampwidth() * 8}-bit. Attempting conversion.")

        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run_simulation)
        self._is_active = False  # Initialisiere auf False

    def _run_simulation(self):
        logging.info("MockRawInputStream: Simulation thread started.")
        self._is_active = True  # SETZT DEN STREAM ALS AKTIV
        try:
            while not self._stop_event.is_set():
                # Lese Roh-Bytes aus der WAV-Datei
                byte_data = self._wav_file.readframes(self._blocksize)
                if not byte_data:
                    logging.info("MockRawInputStream: End of WAV file reached.")
                    break

                # Konvertiere Bytes zu einem NumPy-Array mit dem angegebenen Datentyp
                audio_data_np = np.frombuffer(byte_data, dtype=self._dtype)

                # Reshape für (frames, channels), falls notwendig (Vosk erwartet oft Mono)
                # Annahme: 'audio_data_np' ist bei Mono (len,) und bei Stereo (len,) aber interlaced.
                # reshape(-1, self._channels) formt es korrekt um.
                audio_data_np = audio_data_np.reshape(-1, self._channels)

                # Erstelle Instanzen deiner Mock-Klassen für den Callback
                # Wichtig: current_time im MockCallbackTime könnte inkrementiert werden,
                # um realistischere Zeitstempel zu simulieren. Hier vereinfacht.
                dummy_time = MockCallbackTime(current_time=time.time())
                status_flags = MockCallbackFlags()  # Keine Fehler melden im Testfall

                # Rufe den eigentlichen Callback auf, den transcribe_audio_with_feedback bereitstellt
                self._callback(audio_data_np, len(audio_data_np), dummy_time, status_flags)

                # Simuliere Echtzeit, indem für die Dauer des Audioblocks gewartet wird
                # (len(audio_data_np) / self._channels) ist die Anzahl der Frames bei Multi-Channel
                # ODER len(audio_data_np) bei Mono, wenn audio_data_np ist (frames,)
                # Bei reshape(-1, self._channels) ist len(audio_data_np) die Anzahl der Frames.
                time.sleep(float(len(audio_data_np)) / self._samplerate)

        finally:
            self._is_active = False  # STREAM WIRD ALS INAKTIV MARKTIERT
            logging.info("MockRawInputStream: Simulation thread finished.")

    @property
    def active(self):
        return self._is_active

    def __enter__(self):
        logging.info("MockRawInputStream: Starting simulation.")
        self._thread.start()
        # Gib dem Thread eine kleine Pause, um zu starten und _is_active auf True zu setzen
        time.sleep(0.01)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info("MockRawInputStream: Stopping simulation.")
        self._stop_event.set()
        # Warte auf den Thread mit Timeout, um Hängenbleiben zu verhindern
        self._thread.join(timeout=5)
        if self._thread.is_alive():
            logging.warning("MockRawInputStream: Simulation thread did not terminate gracefully.")
        self._wav_file.close()
        logging.info("MockRawInputStream: Cleanup complete.")


class TestDictationLogic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """This method is run once for the entire test class."""
        logging.info("--- TestDictationLogic: Setting up class resources ---")
        trigger_file = Path(TRIGGER_FILE_PATH)
        if trigger_file.exists():
            logging.warning(f"setUpClass: Found and removed existing trigger file at {TRIGGER_FILE_PATH}")
            trigger_file.unlink()

        cls.assertTrue(Path(MODEL_PATH).exists(), f"Vosk model not found at {MODEL_PATH}")
        # vosk.SetLogLevel(0) # Optional: für detaillierteres Vosk-Logging
        cls.model = vosk.Model(MODEL_PATH)
        logging.info("--- TestDictationLogic: Class resources setup complete ---")

    def setUp(self):
        """This method is run before each test, ensuring a clean state."""
        # Das Modell wird einmal in setUpClass geladen, hier ist nichts weiter nötig.
        pass

    @unittest.mock.patch('scripts.py.func.transcribe_audio_with_feedback.sd.RawInputStream', new=MockRawInputStream)
    def test_transcription_with_short_pause_yields_one_chunk(self):
        """
        Tests if continuous speech (with short pauses) is correctly transcribed as a single chunk.
        This test uses the current test_audio_16k.wav.
        """
        logging.info("--- Starting test: transcription with short pause yields one chunk ---")
        recognizer = vosk.KaldiRecognizer(self.model, SAMPLE_RATE)

        expected_text = "the first test sequence is now complete ready to proceed with the second phase"

        test_session_event = threading.Event()
        test_session_event.set()  # Event ist immer aktiv für diesen Test

        generator = transcribe_audio_with_feedback(logging, recognizer, "en-US",
                                                   initial_silence_timeout=10.0,
                                                   session_active_event=test_session_event,
                                                   AUTO_ENTER_AFTER_DICTATION_global=0)

        transcribed_chunks = []
        try:
            # Iteriere durch den Generator, um alle Chunks zu sammeln
            for chunk in generator:
                if chunk:  # Sammle nur nicht-leere Chunks
                    transcribed_chunks.append(chunk)
        except Exception as e:
            logging.error(f"Error during transcription: {e}", exc_info=True)

        logging.info(f"Final transcribed chunks: {transcribed_chunks}")

        # Erwartung ist 1 Chunk
        self.assertEqual(len(transcribed_chunks), 1,
                         f"Expected exactly one chunk for short-pause audio. Got {len(transcribed_chunks)} chunks: {transcribed_chunks}")
        self.assertEqual(transcribed_chunks[0], expected_text,
                         "The transcribed content of the single chunk is incorrect.")
        logging.info("--- Test successfully completed! ---")

    @unittest.skip("Requires a new audio file with a distinct 1-2 second pause between sentences.")
    @unittest.mock.patch('scripts.py.func.transcribe_audio_with_feedback.sd.RawInputStream', new=MockRawInputStream)
    def test_transcription_with_long_pause_yields_multiple_chunks(self):
        """
        Tests if speech with long pauses is correctly transcribed into multiple chunks.
        This test is currently skipped and needs a suitable audio file to be enabled.
        """
        logging.info("--- Starting test: transcription with long pause yields multiple chunks ---")
        recognizer = vosk.KaldiRecognizer(self.model, SAMPLE_RATE)

        expected_texts = [
            "the first test sequence is now complete",
            "ready to proceed with the second phase"
        ]

        # Hinweis: Dieser Test ist mit dem aktuellen MockRawInputStream und der `test_audio_16k.wav`
        # Datei nicht aussagekräftig, da der Mock das gesamte Audio als einen Stream sendet.
        # Um diesen Test zu aktivieren, bräuchte man eine komplexere MockRawInputStream,
        # die Pausen simuliert, oder eine spezielle Audio-Datei.

        test_session_event = threading.Event()
        test_session_event.set()  # Event ist immer aktiv für diesen Test

        generator = transcribe_audio_with_feedback(logging, recognizer, "en-US",
                                                   initial_silence_timeout=10.0,
                                                   session_active_event=test_session_event,
                                                   # Auch hier session_active_event übergeben
                                                   AUTO_ENTER_AFTER_DICTATION_global=0)

        transcribed_chunks = []
        try:
            for chunk in generator:
                if chunk:
                    transcribed_chunks.append(chunk)
        except Exception as e:
            logging.error(f"Error during transcription: {e}", exc_info=True)

        logging.info(f"Final transcribed chunks: {transcribed_chunks}")
        self.assertEqual(len(transcribed_chunks), len(expected_texts), "Incorrect number of chunks transcribed.")

        for i, expected in enumerate(expected_texts):
            self.assertEqual(transcribed_chunks[i], expected, f"Mismatch in chunk {i}")
        logging.info("--- Test successfully completed! ---")


if __name__ == '__main__':
    unittest.main()
