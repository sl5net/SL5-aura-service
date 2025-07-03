# System-Wide Offline Dictation, Correction, and Suggestion Tool

This project provides a powerful, system-wide dictation tool that goes beyond simple speech-to-text. It **automatically corrects** your dictated text, **suggests synonyms** to improve your writing, and even includes a hotkey to **look up homophones** (e.g., "there" vs. "their") for any word on your screen.

It's a complete, offline writing assistant built on Vosk and LanguageTool.

[![Watch short AI-Demo System-wide offline dictation](https://img.youtube.com/vi/GqidoRiRBy0/maxresdefault.jpg)](https://youtu.be/GqidoRiRBy0)


## Key Features

*   **Dictate, Correct & Enhance:** Automatic grammar/spelling correction and synonym suggestions for your dictated text.
*   **Homophone Lookup:** Place your cursor on a word and press a hotkey to see a list of phonetically similar alternatives.
*   **Fully Automated:** Manages its own LanguageTool server. A single script starts and stops everything cleanly.
*   **Blazing Fast:** Intelligent caching ensures instant "Listening..." notifications and fast processing.
*   **Offline & Private:** 100% local. No data ever leaves your machine.
*   **Open Source & Smart:** Built with FOSS components. Auto-detects the correction language from your Vosk model.

---

### Using AutoKey on Linux

- [AutoKey Releases](https://github.com/autokey/autokey/releases/)
- [AutoKey Installation Wiki](https://github.com/autokey/autokey/wiki/Installing)

#### For Ubuntu or Other Debian Derivatives

**Easy Method:**  
If you are running Ubuntu or another Debian-based distro, simply install AutoKey using the provided `.deb` files. This will handle dependencies and system integration (such as launcher menus) automatically. After installation, AutoKey (with one or both of its frontends) should be operational.


---

### 1. Main Dictation Hotkey

Set a global hotkey to trigger dictation. The command to use is:
```sh
touch /tmp/vosk_trigger
```

---

### Additional Requirements

Please make sure there are two text files.  Could be empty.

Untracked files:

        config/model_name.txt (in newer versions it's already included)
        config/model_name_lastused.txt (in newer versions it's already included)
        config/model_name.txt_lastused (Probably not needed)

#### Java (version >17)

Make sure you have a recent Java version installed. For example:
```sh
sudo apt install openjdk-21-jdk
```

#### inotifywait

**Ubuntu/Debian:**
```sh
sudo apt update
sudo apt install inotify-tools
```

**Manjaro/Arch:**
```sh
sudo pacman -S inotify-tools
```

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


---

### 2. Homophone Lookup Hotkey

Set a *different* global hotkey to trigger homophone lookup. This hotkey should execute a separate script:
```sh
[path-to-your-project]/get_suggestions.py
```

---

#### How to Set Hotkeys

Use your Desktop Environment’s keyboard settings tool (in XFCE, KDE, GNOME, etc.) to create two new custom shortcuts—one for each of the commands above.

---

## Support the Project

If you find this tool useful and want to support our team's continued development, please consider buying us a coffee! Your support is greatly appreciated and helps fuel future improvements.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

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
    
### Download Models and External Tools

- **Vosk-Sprachmodell:** [Vosk Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 
  

### Day-to-Day Use

*   **To Dictate:** Click in any text box and press your **dictation hotkey**. Speak, then pause. The corrected text will be typed for you.
*   **To Look Up Homophones:** Place your cursor inside a word and press your **homophone lookup hotkey**. A list of similarly sounding words will writen.

