# System-Wide Dictation Tool with Vosk for Linux

This project implements a powerful, system-wide dictation feature for Manjaro Linux (and other OS like other Linux distributions, MS Windows, Mac with minor adjustments). Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

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

### Install System Dependencies

First, we will install all necessary programs and libraries using your distribution's package manager. This example uses `pacman` for Arch/Manjaro.

Open a terminal and run the following command:

```bash
# For Arch / Manjaro based systems:
sudo pacman -Syu --needed python git portaudio ffmpeg xclip xdotool libnotify unzip
```

*   `python`: The programming language we'll be using.
*   `git`: For source code management (best practice).
*   `portaudio`: An audio library required by the `sounddevice` Python package.
*   `ffmpeg`: For converting audio formats (optional, but useful).
*   `xclip`, `xdotool`: Tools for controlling the mouse, keyboard, and clipboard.
*   `libnotify`: Enables sending desktop notifications.
*   `unzip`: For decompressing the language models.


### Install Python Dependencies

The required Python packages are listed in the `requirements.txt` file, which is already included in this repository. With your virtual environment active, install them all with one command:

```bash

# Create the virtual environment named "vosk-env" inside the project folder
python -m venv vosk-env

# Activate the environment. You must do this every time you work on this project.
source vosk-env/bin/activate

pip install -r requirements.txt
```

### Download a Vosk Language Model

For high accuracy in English, we will use a model that offers a great balance of size and performance.

```bash
# Download the model (128 MB) inside your project directory
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip

# Unzip the model
unzip vosk-model-en-us-0.22-lgraph.zip
```
After unzipping, you will have a folder named `vosk-model-en-us-0.22-lgraph` in your project directory.

---



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
# Create the virtual environment named "vosk-env"
python -m venv vosk-env

# Activate the environment. You must do this every time you work on this project.
source vosk-env/bin/activate
```

### Download a Vosk Language Model

For high accuracy in English, we will use a model that offers a great balance of size and performance.

```bash
# Download the model (128 MB)
wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip

# Unzip the model
unzip vosk-model-en-us-0.22-lgraph.zip
```
After unzipping, you will have a folder named `vosk-model-en-us-0.22-lgraph` in your project directory.

---

## Configuration

The system consists of two main parts: the background service script (`dictation_service.py`) and a hotkey to trigger it.

### Part A: The Background Service Script

This script (`dictation_service.py`) runs persistently in the background. It loads the language model into memory and waits for a signal to start listening. (This README assumes you already have this script).

### Part B: Set Up the Hotkey Trigger

The background service waits for a specific file to appear (e.g., `/tmp/vosk_trigger`). When your hotkey is pressed, its only job is to create this file. You can use any tool you like for this.

#### Method 1: Using Your Desktop Environment's Settings (Recommended)

Most desktop environments (XFCE, KDE, GNOME, etc.) have a built-in keyboard shortcut manager. This is the simplest method, as it requires no extra software.

1.  Open your system's keyboard settings.
2.  Find the section for "Custom Shortcuts" or "Application Shortcuts".
3.  Add a new shortcut.
4.  For the **command**, enter: `touch /tmp/vosk_trigger`
5.  Assign your desired **hotkey**, for example `Ctrl`+`Alt`+`V`.
6.  Save and close. Your hotkey is ready.

#### Method 2: Using AutoKey (Alternative)

If you prefer a dedicated automation tool, `[AutoKey](https://github.com/autokey/autokey/wiki/Installing)` is a good option.

1.  Install it first. [github.com wiki Installing](https://github.com/autokey/autokey/wiki/Installing).
2.  Start **AutoKey** from your application menu.
3.  Click **File -> New -> Script** (may also look in the script folder for gimicks). 
4.  Paste this single line of code into the script editor: `system.exec_command('touch /tmp/vosk_trigger')`
5.  Click the **"Set"** button next to "Hotkey" and press your desired key combination.
6.  Click the **Save icon** (floppy disk) to save the script.

---

## Usage

1.  **Start the Service (once per computer session):**
    Open a terminal, navigate to your project, activate the environment, and run the service.
    ```bash
    cd ~/projects/py/STT
    source vosk-env/bin/activate
    python dictation_service.py
    ```
    **IMPORTANT:** Leave this terminal window open! As long as it's open, your dictation service is active.

2.  **Dictate:**
    *   Click inside any text box in any application.
    *   Press your hotkey (`Ctrl+Alt+V` or whatever you configured).
    *   A notification "Vosk is Listening..." should appear instantly.
    *   Speak a sentence. Pause briefly when you are finished.
    *   The recognized text will be automatically typed at your cursor's position.

---

## Optional: Start the Service Automatically on Login

To avoid starting the service manually every time, you can add it to your startup applications.

1.  Search for "Session and Startup" (or equivalent) in your application menu.
2.  Go to the "Application Autostart" tab.
3.  Click "Add".
4.  Fill in the fields:
    *   **Name:** `Vosk Dictation Service`
    *   **Description:** `Starts the background service for speech recognition`
    *   **Command:** Use the full, absolute paths to your Python executable and script. Replace `<YOUR_USERNAME>` with your actual username.
        ```
        /home/<YOUR_USERNAME>/projects/py/STT/vosk-env/bin/python /home/<YOUR_USERNAME>/projects/py/STT/dictation_service.py
        ```
5.  Click OK. The service will now start automatically the next time you log in.

