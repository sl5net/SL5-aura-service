This is a draft ! Means, not tested already.


# System-Wide Dictation Tool with Vosk for Ubuntu

This project implements a powerful, system-wide dictation feature for Ubuntu (and other Debian-based distributions with minor adjustments). Once set up, you can press a hotkey in any text field (browser, editor, chat, etc.) to immediately start dictating. The spoken text will be automatically typed out for you.

The system is designed to combine high accuracy (using large offline language models) with instant responsiveness (using a background service architecture).

## Features

*   **System-Wide:** Works in any application that accepts text input.
*   **High Accuracy:** Uses large, precise offline language models from Vosk.
*   **Fast Response:** Thanks to a persistent background service, there is no loading delay when activating the hotkey.
*   **Offline & Private:** All speech recognition happens locally on your computer. No data is sent to the cloud.
*   **Customizable:** Easily switch to other languages (e.g., German) by swapping the [Vosk model](https://alphacephei.com/vosk/models).
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


  
i got this to work thank you! i'm using it right now!

i suggest the that you mention in the docs that auto key isn't needed. A person can set up a hot key in whatever operating system or desktop they're using. i first tried installing auto key with yay and it had to install about seven or eight dependencies so i prefer not to use it and i have removed it.

In xfce, I've added control alt V as the hot key



### Part A: The Background Service Script

This script runs persistently, holds the language model in memory, and waits for a signal from the hotkey.


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
