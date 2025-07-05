# System-Wide Dictation Tool with Vosk for Windows

This project implements a powerful, system-wide dictation feature for Windows. Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

This guide adapts the original Linux concept for Windows, using native tools and the popular automation software, **AutoHotkey**.

## Features

*   **System-Wide:** Works in any application that accepts text input.
*   **High Accuracy:** Uses large, precise offline language models from Vosk.
*   **Fast Response:** Thanks to a persistent background service, there is no loading delay when activating the hotkey.
*   **Offline & Private:** All speech recognition happens locally on your computer. No data is sent to the cloud.
*   **Customizable:** Easily switch to other languages by swapping the [Vosk model](https://alphacephei.com/vosk/models).
*   **Open Source:** Based entirely on free and open-source tools.

---

## Installation Guide

This guide will walk you through the entire setup process, step by step.

### Step 1: Install System Dependencies

First, we will install the necessary software. We recommend installing from the official websites to ensure you get the latest versions.

1.  **Python for Windows:**
    *   Go to the [official Python website](https://www.python.org/downloads/windows/).
    *   Download the latest Python 3 installer.
    *   Run the installer. **IMPORTANT:** On the first screen of the installer, check the box that says **"Add Python to PATH"**. This is crucial for the commands to work. Click "Install Now".

2.  **Git for Windows (Optional, but good practice):**
    *   Go to the [Git for Windows website](https://git-scm.com/download/win).
    *   Download and run the installer, accepting the default settings.

3.  **AutoHotkey:**
    *   Go to the [official AutoHotkey website](https://www.autohotkey.com/).
    *   Download and install the latest version (v2.0 is recommended).

### Step 2: Set Up the Project Directory

We'll create a dedicated directory for our project.

1.  Open **File Explorer**.
2.  Navigate to your user folder (e.g., `C:\Users\YourUsername`).
3.  Create a new folder structure: `projects\py\STT`. The final path should look like: `C:\Users\YourUsername\projects\py\STT`.
4.  Open a Command Prompt by typing `cmd` in the File Explorer address bar (while inside the `STT` folder) and pressing Enter.

### Step 3: Create a Python Virtual Environment

A virtual environment isolates the Python packages for this project from your main system. In the Command Prompt you just opened, run:

```cmd
:: Create the virtual environment named "vosk-env"
python -m venv vosk-env

:: Activate the environment. You must do this every time you work on this project.
.\vosk-env\Scripts\activate
```
After activation, your terminal prompt should change to show `(vosk-env)`.

### Step 4: Install Python Packages

Now, install the required Python libraries using `pip`. We will add `pyautogui`, a library that allows Python to control the keyboard for typing out the text on Windows.

```cmd
pip install vosk sounddevice pyperclip pyautogui
```

### Step 5: Download a Vosk Language Model

For high accuracy in English, we will use the `vosk-model-en-us-0.22-lgraph` model.

1.  Download the model from this link: [vosk-model-en-us-0.22-lgraph.zip](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip) (128 MB).
2.  Open the downloaded `.zip` file.
3.  Extract the folder inside (`vosk-model-en-us-0.22-lgraph`) into your project directory (`C:\Users\YourUsername\projects\py\STT`).

---

## Configuration

The system consists of two scripts: the Python background service and the AutoHotkey trigger script.

### Part A: The Python Background Service

This script runs in the background, holds the language model in memory, and waits for a signal. **This version is modified to use `pyautogui` for typing.**

1.  In your project folder, create a new file named `dictation_service.py`.
2.  Copy the following code into the file.

    ```python
    # File: C:\Users\YourUsername\projects\py\STT\dictation_service.py
    import vosk
    import sys
    import sounddevice as sd
    import queue
    import json
    import pyperclip
    import time
    import tempfile
    import pyautogui
    from pathlib import Path

    # --- Configuration ---
    SCRIPT_DIR = Path(__file__).resolve().parent
    MODEL_NAME = "vosk-model-en-us-0.22-lgraph" # English model
    MODEL_PATH = SCRIPT_DIR / MODEL_NAME
    # Use the system's temporary directory for the trigger file
    TRIGGER_FILE = Path(tempfile.gettempdir()) / "vosk_trigger"
    SAMPLE_RATE = 16000

    # --- Helper Functions ---
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
    except Exception as e:
        print(f"FATAL ERROR: Could not load model. {e}")
        sys.exit(1)

    while True:
        try:
            if TRIGGER_FILE.exists():
                print("Trigger detected! Starting transcription.")
                TRIGGER_FILE.unlink() # Remove the file to reset the trigger

                recognized_text = transcribe_audio()

                if recognized_text:
                    print(f"Transcribed: '{recognized_text}'")
                    # Use pyautogui to type the text automatically
                    pyautogui.typewrite(recognized_text)
                    pyperclip.copy(recognized_text) # Also copy to clipboard
                else:
                    print("No text was recognized.")
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nService stopped by user.")
            break
        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
    ```

### Part B: The AutoHotkey Script

This script creates the global hotkey that signals the Python service.

1.  In your project folder (`C:\Users\YourUsername\projects\py\STT`), right-click, go to **New**, and select **AutoHotkey Script**.
2.  Name the file `vosk_trigger.ahk`.
3.  Right-click the new file and choose **Edit script**.
4.  Delete any existing text and paste the following code. This sets the hotkey to **`Ctrl` + `Alt` + `D`**.

    ```autohotkey
    ; Vosk Dictation Trigger for Windows
    ; Hotkey: Ctrl+Alt+D

    ^!d::
    {
        ; Create an empty file in the temp directory to signal the Python script
        FileAppend, "", A_Temp . "\vosk_trigger"
        ; Show a notification that we are listening
        TrayTip, "Vosk is Listening...", "Speak now.", 1
    }
    return
    ```
5.  Save and close the file.

---

## Usage

1.  **Start the Service (once per computer session):**
    *   Open a Command Prompt, navigate to your project directory, and activate the environment as shown in Step 2 and 3.
    *   Run the Python service:
        ```cmd
        cd C:\Users\YourUsername\projects\py\STT
        .\vosk-env\Scripts\activate
        python dictation_service.py
        ```
    *   **IMPORTANT:** Leave this command prompt window open! You can minimize it. As long as it's open, the service is running.

2.  **Start the Hotkey Script:**
    *   Navigate to your project folder in File Explorer.
    *   Double-click the `vosk_trigger.ahk` script. You will see a green "H" icon appear in your system tray (bottom-right of the screen).

3.  **Dictate:**
    *   Click inside any text box.
    *   Press your hotkey (`Ctrl+Alt+D`).
    *   A notification "Vosk is Listening..." will appear.
    *   Speak a sentence. Pause briefly when you are finished.
    *   The recognized text will be automatically typed for you.

---

## Optional: Start Everything Automatically at Login

To avoid starting the scripts manually every time, you can add them to your Windows startup folder.

1.  **Create a Launcher for the Python Service:**
    *   In your project folder, create a new text file. Name it `launch_vosk_service.bat`.
    *   Edit the file and paste the following command. **Replace `YourUsername` with your actual username.** This script will start the Python service in its environment without keeping a command window open.
        ```batch
        @echo off
        start "Vosk Service" /B "C:\Users\YourUsername\projects\py\STT\vosk-env\Scripts\python.exe" "C:\Users\YourUsername\projects\py\STT\dictation_service.py"
        ```
    *   Save the file.

2.  **Add Shortcuts to the Startup Folder:**
    *   Press `Win` + `R` to open the Run dialog.
    *   Type `shell:startup` and press Enter. This will open your user's Startup folder.
    *   Go back to your project folder (`C:\Users\YourUsername\projects\py\STT`).
    *   Right-click `launch_vosk_service.bat` and select **Copy**. Go to the Startup folder and right-click -> **Paste shortcut**.
    *   Right-click `vosk_trigger.ahk` and select **Copy**. Go to the Startup folder and right-click -> **Paste shortcut**.

Now, both the background service and the hotkey script will start automatically the next time you log into Windows. Enjoy your new dictation tool
