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

## Installation

Before you can use the application, you need to run a one-time setup script to install dependencies and download the required models. These scripts are located in the `setup/` directory.

### For Linux and macOS

You only need to run the script that matches your operating system.

1.  **Make the script executable:**
    Open a terminal in the project's root directory and run the `chmod` command on the appropriate script. For example, if you are on Ubuntu:
    ```shell
    chmod +x setup/ubuntu_setup.sh
    ```

2.  **Run the setup script:**
    Now, execute the script. The script will ask for your password to install system packages.
    ```shell
    bash setup/ubuntu_setup.sh
    ```

    Choose the script for your system:
    *   `setup/arch_setup.sh`
    *   `setup/manjaro_setup.sh`
    *   `setup/ubuntu_setup.sh` (for Ubuntu, Debian, or other derivatives)
    *   `setup/macos_setup.sh`

### For Windows

The application's core file-watching feature is not yet compatible with Windows. However, you can run the setup script to prepare the environment for future compatibility or development.

The script must be run with administrator privileges.

1.  Open **File Explorer** and navigate to the `setup` folder inside the project directory.
2.  Right-click on the `windows_setup.ps1` file.
3.  From the context menu, select **"Run with PowerShell"**.
4.  If prompted by a User Account Control (UAC) dialog, click **Yes** to allow the script to make changes.

The script will then install all necessary tools and models.

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

by Using 
```shell
setup/{OS Name}_setup...
```

### Windows OS

install AutoHotkey version 2
run server
`type_watcher.ahk`

follwong Vosk-Models will be downloaded and used automatically:

| Model                                                                                  | Size | Word error rate/Speed                                                                         | Notes                                     | License    |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter)                       | Accurate generic US English model         | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)       | 1.9G | 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx) | Big German model for telephony and server | Apache 2.0 |

This table provides an overview of different Vosk models, including their size, word error rate or speed, notes, and license information.

- **Vosk-Models:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**License of LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

   
```sh
cd ~/projects/py/STT/
wget https://languagetool.org/download/LanguageTool-6.6.zip
unzip LanguageTool-6.6.zip
```


### Day-to-Day Use

*   **To Dictate:** Click in any text box and press your **dictation hotkey**. Speak, then pause. The corrected text will be typed for you.
*   **To Look Up Homophones:** Place your cursor inside a word and press your **homophone lookup hotkey**. A list of similarly sounding words will writen.

