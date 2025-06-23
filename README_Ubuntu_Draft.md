This is a draft ! Means, not tested already.


# System-Wide Dictation Tool with Vosk for Ubuntu

This project implements a powerful, system-wide dictation feature for Ubuntu (and other Debian-based distributions with minor adjustments). Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

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

First, we will install all necessary programs and libraries using Ubuntu's package manager, `apt`.

Open a terminal and run the following command:

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv git portaudio19-dev ffmpeg xclip  xdotool libasound2-dev libnotify-bin autokey-gtk unzip
```

*   `python3`, `python3-pip`, `python3-venv`: The programming language and tools for managing its packages and environments.
*   `git`: For source code management (best practice).
*   `portaudio19-dev`: An audio library required by the `sounddevice` Python module.
*   `ffmpeg`: For converting audio formats (optional, but useful).
*   `xclip`, `xdotool`: Tools for controlling the mouse, keyboard, and clipboard.
*   `libnotify-bin`: Enables sending desktop notifications from scripts.
*   `autokey-gtk`: The automation software for our hotkey. Use `autokey-qt` if you are using a Qt-based desktop like KDE Plasma.
*   `unzip`: For decompressing the language models.

### Step 2: Set Up the Project Directory

We'll create a dedicated directory for our project in your home folder.

```bash
# Create the directory and change into it
mkdir -p ~/projects/py/STT
cd ~/projects/py/STT
```

### Step 3: Create a Python Virtual Environment

A virtual environment is crucial for isolating the Python packages for this project from your main system.

```bash
# Create the virtual environment named "vosk-env"
python3 -m venv vosk-env

# Activate the environment. You must do this every time you work on this project.
source vosk-env/bin/activate
```
After activation, your terminal prompt should change to show `(vosk-env)`.

### Step 4: Install Python Packages

Now, install the required Python libraries using `pip` inside your activated environment.

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

The system consists of two parts: the background service script and the AutoKey trigger.

### Part A: The Background Service Script

This script runs persistently, holds the language model in memory, and waits for a signal from the hotkey.

1.  Create a new file in your project directory:
    ```bash
    nano dictation_service.py
    ```

2.  Copy the following code completely into the file. The code is already configured for the English model.

    ```python
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
            # Check for the trigger file every 100ms
            if TRIGGER_FILE.exists():
                print("Trigger detected! Starting transcription.")
                notify("Vosk is Listening...", "Speak now.")
                TRIGGER_FILE.unlink() # Remove the file to reset the trigger

                recognized_text = transcribe_audio()

                if recognized_text:
                    print(f"Transcribed: '{recognized_text}'")
                    # Use xdotool to type the text
                    subprocess.run([XDOTOOL_PATH, "type", "--clearmodifiers", recognized_text])
                    pyperclip.copy(recognized_text) # Also copy to clipboard
                else:
                    notify("Vosk Dictation", "No text was recognized.")
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nService stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            notify("Vosk Service Error", str(e))
    ```

3.  Save and close the file (in `nano`: `Ctrl+X`, then `Y`, then `Enter`).

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

### Method 1: Manual Start (for testing)

1.  **Start the Service:** Open a terminal and run:
    ```bash
    cd ~/projects/py/STT
    source vosk-env/bin/activate
    python3 dictation_service.py
    ```
    **IMPORTANT:** Leave this terminal window open! As long as it's open, your dictation service is running. This is great for testing or one-off use.

2.  **Dictate:**
    *   Click inside any text box in any application.
    *   Press your hotkey (`Ctrl+Alt+D`).
    *   A notification "Vosk is Listening..." will appear instantly.
    *   Speak a sentence. Pause briefly when you are finished.
    *   The recognized text will be automatically typed at your cursor's position.

### Method 2: Automatic Start (Recommended)

To avoid starting the service manually every time, we can create a `systemd` user service. This is the modern, robust way to manage background tasks on Ubuntu.

1.  Create the directory for user services if it doesn't exist:
    ```bash
    mkdir -p ~/.config/systemd/user/
    ```

2.  Create a new service file:
    ```bash
    nano ~/.config/systemd/user/vosk-dictation.service
    ```

3.  Paste the following content into the file. **You must replace `<YOUR_USERNAME>` with your actual username.**

    ```ini
    [Unit]
    Description=Vosk System-Wide Dictation Service

    [Service]
    ExecStart=/home/<YOUR_USERNAME>/projects/py/STT/vosk-env/bin/python3 /home/<YOUR_USERNAME>/projects/py/STT/dictation_service.py
    Restart=on-failure
    RestartSec=5

    [Install]
    WantedBy=default.target
    ```

4.  Save and close the file (`Ctrl+X`, `Y`, `Enter`).

5.  Enable and start the service:
    ```bash
    systemctl --user daemon-reload
    systemctl --user enable --now vosk-dictation.service
    ```
    The `--now` flag starts it immediately. It will now automatically start every time you log in.

6.  (Optional) You can check the status of your service at any time with:
    ```bash
    systemctl --user status vosk-dictation.service
    ```

Enjoy your new system-wide dictation setup
