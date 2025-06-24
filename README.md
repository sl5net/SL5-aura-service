# System-Wide Dictation Tool with Vosk for Manjaro Linux

This project implements a powerful, system-wide dictation feature for Manjaro Linux (and other Linux distributions with minor adjustments). Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

The system is designed to combine high accuracy (using large offline language models) with instant responsiveness (using a background service architecture).

## Features

*   **System-Wide:** Works in any application that accepts text input.
*   **High Accuracy:** Uses large, precise offline language models from Vosk.
*   **Fast Response:** Thanks to a persistent background service, there is no loading delay when activating the hotkey.
*   **Offline & Private:** All speech recognition happens locally on your computer. No data is sent to the cloud.
*   **Customizable:** Easily switch to other languages (e.g., German) by swapping the Vosk model.
*   **Open Source:** Based entirely on free and open-source tools.

---

## Installation Guide

This guide will walk you through the entire setup process, step by step.

### Step 1: Install System Dependencies

First, we will install all necessary programs and libraries using Manjaro's package manager, `pacman`.

Open a terminal and run the following command:

```bash
sudo pacman -Syu --needed python git portaudio ffmpeg xclip xdotool libnotify autokey unzip
```

*   `python`: The programming language we'll be using.
*   `git`: For source code management (best practice).
*   `portaudio`: An audio library required by `sounddevice`.
*   `ffmpeg`: For converting audio formats (optional, but useful).
*   `xclip`, `xdotool`: Tools for controlling the mouse, keyboard, and clipboard.
*   `libnotify`: Enables sending desktop notifications.
*   `autokey`: The automation software for our hotkey.
*   `unzip`: For decompressing the language models.

### Step 2: Set Up the Project Directory

We'll create a dedicated directory for our project.

```bash
# Create the directory and change into it
mkdir -p ~/projects/py/STT
cd ~/projects/py/STT
```

### Step 3: Create a Python Virtual Environment

A virtual environment is crucial for isolating the Python packages for this project from your main system.

```bash
# Create the virtual environment named "vosk-tts"
python -m venv vosk-tts

# Activate the environment. You must do this every time you work on this project.
source vosk-tts/bin/activate
```
After activation, your terminal prompt should change to show `(vosk-tts)`.

### Step 4: Install Python Packages

Now, install the required Python libraries using `pip`.

```bash
pip install vosk sounddevice pyperclip
```

### Step 5: Download a Vosk Language Model

For high accuracy in English, we will use the `vosk-model-en-us-0.22-lgraph` model, which offers a great balance of size and performance.

```bash
# Download the model (128 MB)
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip

# Unzip the model
unzip vosk-model-en-us-0.22-lgraph.zip
```
After unzipping, you will have a folder named `vosk-model-en-us-0.22-lgraph` in your project directory.

---

## Configuration

The system consists of two scripts: the background service and the AutoKey trigger.

### Part A: The Background Service Script

This script runs persistently, holds the language model in memory, and waits for a signal from the hotkey.

Copy the following code, paste it into a terminal, and press enter. **Note:** The `MODEL_NAME` has been changed for the English model.

    ```python
    cat <<'EOF' > dictation_service.py
    # File: ~/projects/py/STT/dictation_service.py
    import vosk
    import sys
    import sounddevice as sd
    import queue
    import json
    import pyperclip
    import subprocess
    import time
    from pathlib import Path

    # --- Configuration ---
    SCRIPT_DIR = Path(__file__).resolve().parent
    MODEL_NAME = "vosk-model-en-us-0.22-lgraph" # English model
    MODEL_PATH = SCRIPT_DIR / MODEL_NAME
    TRIGGER_FILE = Path("/tmp/vosk_trigger") # Our signal file

    NOTIFY_SEND_PATH = "/usr/bin/notify-send"
    XDOTOOL_PATH = "/usr/bin/xdotool"
    SAMPLE_RATE = 16000

    # --- Helper Functions ---
    def notify(summary, body=""):
        try:
            subprocess.run([NOTIFY_SEND_PATH, summary, body, "-t", "2000"], check=True)
        except Exception:
            print(f"NOTIFY: {summary} - {body}")

    def transcribe_audio():
        q = queue.Queue()
        def audio_callback(indata, frames, time, status):
            q.put(bytes(indata))

        try:
            with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000,
                                   dtype='int16', channels=1, callback=audio_callback):
                while True:
                    data = q.get()
                    if recognizer.AcceptWaveform(data):
                        break
            result = json.loads(recognizer.Result())
            return result.get('text', '')
        except Exception as e:
            print(f"Error during transcription: {e}")
            return ""

    # --- Main Service Logic ---
    print("--- Vosk Dictation Service ---")
    if not MODEL_PATH.exists():
        print(f"FATAL ERROR: Model not found at {MODEL_PATH}")
        sys.exit(1)

    print(f"Loading model '{MODEL_NAME}'... This may take a few seconds.")
    try:
        model = vosk.Model(str(MODEL_PATH))
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Model loaded successfully. Service is waiting for a trigger.")
        notify("Vosk Service Ready", "Hotkey is now active.")
    except Exception as e:
        print(f"FATAL ERROR: Could not load model. {e}")
        sys.exit(1)

    while True:
        try:
            if TRIGGER_FILE.exists():
                print("Trigger detected! Starting transcription.")
                notify("Vosk is Listening...", "Speak now.")
                TRIGGER_FILE.unlink()

                recognized_text = transcribe_audio()

                if recognized_text:
                    print(f"Transcribed: '{recognized_text}'")
                    subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", recognized_text])
                    pyperclip.copy(recognized_text)
                else:
                    notify("Vosk Dictation", "No text was recognized.")

            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nService stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            notify("Vosk Service Error", str(e))
EOF
    ```

### Part B: Configure AutoKey for the Hotkey

1.  Start **AutoKey** from your application menu.
2.  Click **File -> New -> Script**.
3.  Give the script a name, e.g., `Vosk Trigger`.
4.  Delete all the sample code in the right-hand pane.
5.  Paste this **single line** of code:
    ```python
    system.exec_command('touch /tmp/vosk_trigger')
    ```
6.  Click the **"Set"** button next to "Hotkey" at the top.
7.  Press your desired key combination, e.g., **`Ctrl` + `Alt` + `D`**. Click OK.
8.  Click the **Save icon** (floppy disk) to save the script.

---

## Usage

1.  **Start the Service (once per computer session):**
    Open a terminal and run:
    ```bash
    cd ~/projects/py/STT
    source vosk-tts/bin/activate
    python dictation_service.py
    ```
    **IMPORTANT:** Leave this terminal window open! As long as it's open, your dictation service is running.

2.  **Dictate:**
    *   Click inside any text box in any application.
    *   Press your hotkey (`Ctrl+Alt+D`).
    *   A notification "Vosk is Listening..." will appear instantly.
    *   Speak a sentence. Pause briefly when you are finished.
    *   The recognized text will be automatically typed at your cursor's position.

---

## Optional: Start the Service Automatically

To avoid starting the service manually every time, you can add it to your startup applications.

1.  Search for "Session and Startup" in your application menu.
2.  Go to the "Application Autostart" tab.
3.  Click "Add".
4.  Fill in the fields:
    *   **Name:** `Vosk Dictation Service`
    *   **Description:** `Starts the background service for speech recognition`
    *   **Command:** Copy the **full path** to the script here. Replace `<YOUR_USERNAME>` with your actual username.
        ```
        /home/<YOUR_USERNAME>/projects/py/STT/vosk-tts/bin/python /home/<YOUR_USERNAME>/projects/py/STT/dictation_service.py
        ```
5.  Click OK. The service will now start automatically the next time you log in.

Enjoy
