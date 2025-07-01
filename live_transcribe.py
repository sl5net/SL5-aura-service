import vosk
import sys
import sounddevice as sd
import queue
import json
import os

# --- Configuration ---
MODEL_PATH = "vosk-model-de-0.21"
LANGUAGETOOL_URL = "http://localhost:8082/v2/check"


SAMPLE_RATE = 16000
DEVICE_ID = None # Default microphone
BLOCK_SIZE = 8000 # Frames per buffer

# A queue to share audio data between the audio callback and the main thread
q = queue.Queue()

def correct_text(text: str) -> str:
    """Sends text to the LanguageTool server and applies the first correction for each match."""
    if not text.strip():
        return text

    try:
        data = {'language': 'de-DE', 'text': text}
        response = requests.post(LANGUAGETOOL_URL, data=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        matches = response.json().get('matches', [])

        # We process matches in reverse to not mess up the offsets
        for match in reversed(matches):
            if match['replacements']:
                offset = match['offset']
                length = match['length']
                replacement = match['replacements'][0]['value']
                text = text[:offset] + replacement + text[offset + length:]

        return text
    except requests.exceptions.RequestException as e:
        print(f"\n[Error] Could not connect to LanguageTool server: {e}", file=sys.stderr)
        return text # Return original text on connection error
    except Exception as e:
        print(f"\n[Error] An error occurred during correction: {e}", file=sys.stderr)
        return text



def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# --- Check if model exists ---
if not os.path.exists(MODEL_PATH):
    print(f"Model path '{MODEL_PATH}' not found. Please download and unzip a model.")
    sys.exit(1)

try:
    # --- Main Application Logic ---

    # 1. Load the Vosk model
    model = vosk.Model(MODEL_PATH)

    # 2. Create a recognizer
    recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

    # 3. Open the microphone stream
    # The 'with' block ensures the stream is properly closed
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=BLOCK_SIZE, device=DEVICE_ID,
                           dtype='int16', channels=1, callback=audio_callback):

        print("#" * 80)
        print("Press Ctrl+C to stop the recording")
        print("#" * 80)

        while True:
            # Get audio data from the queue
            data = q.get()

            # Feed the data to the recognizer
            if recognizer.AcceptWaveform(data):
                # A full utterance has been recognized
                result_json = recognizer.Result()
                result_dict = json.loads(result_json)
                print("FINAL:", result_dict['text'])
            else:
                # Partial results are available
                partial_json = recognizer.PartialResult()
                partial_dict = json.loads(partial_json)
                if partial_dict['partial']:
                    # Use a carriage return to overwrite the line
                    print("PARTIAL:", partial_dict['partial'], end='\r')

except KeyboardInterrupt:
    print("\nDone")
except Exception as e:
    print(f"An error occurred: {type(e).__name__}: {e}")
