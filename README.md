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

### Teil B 1 : AutoKey ist nicht nötig für den Hotkey 

    
i got this to work thank you! i'm using it right now!

i suggest the that you mention in the docs that auto key isn't needed. A person can set up a hot key in whatever operating system or desktop they're using. i first tried installing auto key with yay and it had to install about seven or eight dependencies so i prefer not to use it and i have removed it.

In xfce, I've added control alt V as the hot key



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
