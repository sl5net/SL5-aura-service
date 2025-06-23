# System-Wide Dictation Tool with Vosk for macOS

This project implements a powerful, system-wide dictation feature for macOS. Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

This guide uses macOS's built-in **Automator** for hotkey creation and `launchd` for running the background service, ensuring a clean and native integration.

## Features

*   **System-Wide:** Works in any application that accepts text input.
*   **High Accuracy:** Uses large, precise offline language models from Vosk.
*   **Fast Response:** Thanks to a persistent background service, there is no loading delay when activating the hotkey.
*   **Offline & Private:** All speech recognition happens locally on your computer. No data is sent to the cloud.
*   **Customizable:** Easily switch to other languages by swapping the Vosk model.
*   **Open Source:** Based entirely on free and open-source tools.

---

## Installation Guide

This guide will walk you through the entire setup process, step by step.

### Step 1: Install System Dependencies

We will use [Homebrew](https://brew.sh), the standard package manager for macOS, to install the necessary tools. If you don't have Homebrew, open **Terminal** and install it with:
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

Once Homebrew is ready, run the following command in your Terminal:

```bash
brew install python git portaudio wget
```

*   `python`: The programming language we'll be using.
*   `git`: For source code management (best practice).
*   `portaudio`: An audio library required by the `sounddevice` Python module.
*   `wget`: A tool for downloading files from the command line.
*   **Note:** Tools like `osascript` (for typing and notifications) are already built into macOS.

### Step 2: Set Up the Project Directory

We'll create a dedicated directory for our project in your home folder.

```bash
# Create the directory and change into it
mkdir -p ~/projects/py/STT
cd ~/projects/py/STT
```

### Step 3: Create a Python Virtual Environment

A virtual environment is crucial for isolating the project's Python packages.

```bash
# Create the virtual environment named "vosk-env"
python3 -m venv vosk-env

# Activate the environment. You must do this every time you work on this project.
source vosk-env/bin/activate
```
After activation, your terminal prompt should change to show `(vosk-env)`.

### Step 4: Install Python Packages

Now, install the required Python libraries using `pip`.

```bash
pip install vosk sounddevice pyperclip
```

### Step 5: Download a Vosk Language Model

We will download the recommended English model.

```bash
# Download the model (128 MB)
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip

# Unzip the model
unzip vosk-model-en-us-0.22-lgraph.zip
```
After unzipping, you will have a folder named `vosk-model-en-us-0.22-lgraph` in your project directory.

---

## Configuration

The system consists of two parts: the Python background service and a macOS "Quick Action" for the hotkey.

### Part A: The Python Background Service

This script runs in the background, listens for the trigger, and uses AppleScript (`osascript`) to type the text.

1.  In your project directory, create a new file named `dictation_service.py`.
2.  Copy the following code into the file. It has been specifically modified for macOS.

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
    SAMPLE_RATE = 16000

    # --- macOS Helper Functions ---
    def notify(summary, body=""):
        # Uses AppleScript to show a native macOS notification
        try:
            script = f'display notification "{body}" with title "{summary}"'
            subprocess.run(["osascript", "-e", script], check=True)
        except Exception as e:
            print(f"macOS NOTIFY ERROR: {e}")

    def type_text(text):
        # Uses AppleScript to type text, avoiding special character issues
        # The text is escaped to be safely used in an AppleScript string
        escaped_text = text.replace('\\', '\\\\').replace('"', '\\"')
        script = f'tell application "System Events" to keystroke "{escaped_text}"'
        try:
            subprocess.run(["osascript", "-e", script], check=True)
        except Exception as e:
            print(f"macOS KEYSTROKE ERROR: {e}")

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
                    type_text(recognized_text)
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

### Part B: Configure the Hotkey with Automator

1.  Open the **Automator** app (you can find it in your Applications folder or via Spotlight search).
2.  Choose **File -> New**.
3.  Select **Quick Action** and click "Choose".
4.  At the top of the workflow window, set the dropdowns to: "Workflow receives **no input** in **any application**".
5.  From the actions library on the left, find **Run Shell Script** and drag it to the right-hand pane.
6.  In the "Run Shell Script" box, paste this single command. It creates the trigger file that our Python script is looking for.
    ```bash
    touch /tmp/vosk_trigger
    ```
7.  Go to **File -> Save** and name it `Vosk Trigger`.
8.  Now, assign a keyboard shortcut:
    *   Open **System Settings** (or System Preferences on older macOS).
    *   Go to **Keyboard -> Keyboard Shortcuts... -> Services**.
    *   Scroll down to the "General" section. You should see your "Vosk Trigger" service.
    *   Click on it, then click "Add Shortcut" and press your desired key combination (e.g., **`Control` + `Option` + `D`** or `^⌥D`).
    *   Close the settings.

---

## Usage

### 1. Grant Permissions (One-time only)

The first time you run the script, macOS will ask for permission to control your computer and access the microphone.
*   **Microphone:** The script will prompt you. Click OK.
*   **Accessibility (for typing):** macOS will block the script from typing and prompt you to grant access.
    *   Go to **System Settings -> Privacy & Security -> Accessibility**.
    *   Click the `+` button, and add your Terminal application (e.g., `Terminal.app` or `iTerm.app`). Ensure the switch next to it is turned on.

### 2. Start the Service & Dictate

1.  **Start the Service (once per session):** Open a Terminal and run:
    ```bash
    cd ~/projects/py/STT
    source vosk-env/bin/activate
    python3 dictation_service.py
    ```
    **IMPORTANT:** Leave this Terminal window open! You can minimize it. As long as it's running, your dictation service is active.

2.  **Dictate:**
    *   Click inside any text box.
    *   Press your hotkey (`^⌥D`).
    *   A notification "Vosk is Listening..." will appear.
    *   Speak a sentence, then pause. The text will be typed for you.

---

## Optional: Start the Service Automatically with `launchd`

To avoid starting the service manually, we can create a `launchd` agent.

1.  Create the directory for user agents if it doesn't exist:
    ```bash
    mkdir -p ~/Library/LaunchAgents
    ```

2.  Create a new service file (`.plist`):
    ```bash
    nano ~/Library/LaunchAgents/com.user.vosk-dictation.plist
    ```

3.  Paste the following content. **You must replace `<YOUR_USERNAME>` with your actual username.**

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.user.vosk-dictation</string>
        <key>ProgramArguments</key>
        <array>
            <string>/Users/<YOUR_USERNAME>/projects/py/STT/vosk-env/bin/python3</string>
            <string>/Users/<YOUR_USERNAME>/projects/py/STT/dictation_service.py</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>KeepAlive</key>
        <true/>
    </dict>
    </plist>
    ```

4.  Save and close the file (`Ctrl+X`, `Y`, `Enter`).

5.  Load the service. It will now start automatically every time you log in.
    ```bash
    launchctl load ~/Library/LaunchAgents/com.user.vosk-dictation.plist
    ```

Enjoy your new native, system-wide dictation tool
