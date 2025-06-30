# System-Wide Offline Dictation, Correction, and Suggestion Tool

This project provides a powerful, system-wide dictation tool that goes beyond simple speech-to-text. It **automatically corrects** your dictated text, **suggests synonyms** to improve your writing, and even includes a hotkey to **look up homophones** (e.g., "there" vs. "their") for any word on your screen.

It's a complete, offline writing assistant built on Vosk and LanguageTool.

## Key Features

*   **Dictate, Correct & Enhance:** Automatic grammar/spelling correction and synonym suggestions for your dictated text.
*   **Homophone Lookup:** Place your cursor on a word and press a hotkey to see a list of phonetically similar alternatives.
*   **Fully Automated:** Manages its own LanguageTool server. A single script starts and stops everything cleanly.
*   **Blazing Fast:** Intelligent caching ensures instant "Listening..." notifications and fast processing.
*   **Offline & Private:** 100% local. No data ever leaves your machine.
*   **Open Source & Smart:** Built with FOSS components. Auto-detects the correction language from your Vosk model.

---

## Installation Guide

*(Steps 1-4 are the same as before)*

### Step 1: Clone the Repository
### Step 2: Install System Dependencies
### Step 3: Set Up Python Environment
### Step 4: Download Models

---

## Configuration

You will need to configure two separate hotkeys for the system's two main functions.

### 1. The Main Dictation Hotkey

Set a global hotkey to trigger the dictation. The command is:
`touch /tmp/vosk_trigger`

### 2. The Homophone Lookup Hotkey

Set a *different* global hotkey to trigger the homophone lookup. This hotkey should execute a separate script. The command is:
`[path-to-your-project]/scripts/get_homophones.sh`
*(Note: Please adjust the script name if it is different.)*

**How to Set Hotkeys:** Use your Desktop Environment's keyboard settings (in XFCE, KDE, GNOME) to create two new custom shortcuts, one for each command above.

---


## Support the Project

If you find this tool useful and want to support its continued development, please consider buying me a coffee! Your support is greatly appreciated and helps fuel future improvements.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/C0C445TF6)

---


## Usage



### Starting the Service

A single script handles activating the environment and launching all background services.

1.  **Make the start script executable (one time only):**
    ```bash
    chmod +x scripts/activate-venv_and_run-server.sh
    ```

2.  **Start the Service (once per session):**
    Simply run the script from the project's root directory.
    ```bash
    ./scripts/activate-venv_and_run-server.sh
    ```
    **Leave this terminal open.**

### Day-to-Day Use

*   **To Dictate:** Click in any text box and press your **dictation hotkey**. Speak, then pause. The corrected text will be typed for you.
*   **To Look Up Homophones:** Place your cursor inside a word and press your **homophone lookup hotkey**. A notification will appear with a list of similarly sounding words.

