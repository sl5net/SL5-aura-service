import pyaudio
import subprocess
import time

from ovos_ww_plugin_precise_lite import PreciseLiteWakeWordPlugin

def trigger_dictation_start():
    """
    Executes a simple 'touch' command to signal that dictation should start.
    """
    command = ["touch", "/tmp/vosk_trigger"]

    try:
        print(f"Executing signal command: '{' '.join(command)}'")
        # We don't need to capture the output for 'touch'
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Failed to execute command: {e}")


# --- Configuration ---
WAKEWORD_ID = "computer"
MODEL_URL = "https://github.com/MycroftAI/precise-data/raw/models-dev/computer.tar.gz"

config = {"model": MODEL_URL}

# --- Audio Setup ---
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# --- Main Application ---
ww_plugin = PreciseLiteWakeWordPlugin(config=config)
pa = pyaudio.PyAudio()
audio_stream = None

try:
    audio_stream = pa.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE
    )

    print(f"Listener ready. Say '{WAKEWORD_ID}' to trigger the command.")

    while True:
        audio_chunk = audio_stream.read(CHUNK_SIZE)
        ww_plugin.update(audio_chunk)

        if ww_plugin.found_wake_word(0):
            print(f"\n--- WAKEWORD DETECTED: {WAKEWORD_ID} ---")
            trigger_dictation_start()
            print("Signal sent. Listening again...")
            # Optional: Add a small delay to prevent immediate re-triggering
            time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping listener.")
finally:
    if audio_stream is not None:
        audio_stream.stop_stream()
        audio_stream.close()
    if pa is not None:
        pa.terminate()
    print("Resources released.")

