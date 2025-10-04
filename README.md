# System-Wide Offline Voice to Commands or Text, Pluggable System

# SL5 Aura Service - Features & OS Compatibility

Welcome to SL5 Aura Service! This document provides a quick overview of our key features and their operating system compatibility.

Aura goes beyond simple speech-to-text. This allows customization.

It's a complete, offline assistant built on Vosk and LanguageTool.

[![SL5 Aura – Live Coding Example 3.10.2025](https://img.youtube.com/vi/2YYkaY2dIcs/maxresdefault.jpg)]([https://youtu.be/2YYkaY2dIcs](https://www.youtube.com/watch?v=tEijy8WRFCI))


## Key Features

*   **Offline & Private:** 100% local. No data ever leaves your machine.
*   **Conservative RAM Usage:** Intelligently manages memory, preloading models only if enough free RAM is available, ensuring other applications (like your PC games) always have priority.
*   **Cross-Platform:** Works on Linux, macOS, and Windows.
*   **Fully Automated:** Manages its own LanguageTool server (but you can use a external also). 
*   **Blazing Fast:** Intelligent caching ensures instant "Listening..." notifications and fast processing.

## Documentation

For a complete technical reference, including all modules and scripts, please visit our official documentation page. It is automatically generated and always up-to-date.

[**Go to Documentation >>**](https://sl5net.github.io/SL5-aura-service/)


### Build Status
[![Linux Manjaro](https://img.shields.io/badge/Manjaro-Tested-27ae60?style=for-the-badge&logo=manjaro)](https://youtu.be/D9ylPBnP2aQ)
[![Linux Ubuntu](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/ubuntu_setup.yml)
[![Linux Suse](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/suse_setup.yml)
[![macOS](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml/badge.svg)](https://github.com/sl5net/SL5-aura-service/actions/workflows/windows11_setup_bat.yml)

[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/SL5-aura-service/)

---

## Installation

The setup is a two-step process:
1.  Clone this repository to your computer.
2.  Run the one-time setup script for your operating system.

The setup scripts handle everything: system dependencies, Python environment, and downloading the necessary models and tools (~4GB) directly from our GitHub Releases for maximum speed.

#### For Linux & macOS & windows
Open a terminal in the project's root directory and run the script for your system:
```bash
# For Ubuntu/Debian, Manjaro/Arch, macOs  or other derivatives

bash setup/{your-os}_setup.sh

# For Windows in Admin-Powershell

setup/windows11_setup.ps1
```

#### For Windows
Run the setup script with administrator privileges **"Run with PowerShell"**.

**Install a tool for read and run e.g. [CopyQ](https://github.com/hluk/CopyQ) or [AutoHotkey v2](https://www.autohotkey.com/)**. This is required for the text-typing watcher.

---

## Usage

### 1. Start the Services

#### On Linux & macOS
A single script handles everything. It starts the main dictation service and the file watcher automatically in the background.
```bash
# Run this from the project's root directory
./scripts/restart_venv_and_run-server.sh
```

#### On Windows
Starting the service is a **two-step manual process**:

1.  **Start the Main Service:** Run `start_dictation_v2.0.bat`. or start from `.venv` the service with `python3`

### 2. Configure Your Hotkey

To trigger dictation, you need a global hotkey that creates a specific file. We highly recommend the cross-platform tool [CopyQ](https://github.com/hluk/CopyQ).

#### Our Recommendation: CopyQ

Create a new command in CopyQ with a global shortcut.

**Command for Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Command for Windows when use [CopyQ](https://github.com/hluk/CopyQ):**
```js
copyq:
var filePath = 'c:/tmp/sl5_record.trigger';

var f = File(filePath);

if (f.openAppend()) {
    f.close();
} else {
    popup(
        'error',
        'cant read or open:\n' + filePath
        + '\n' + f.errorString()
    );
}
```


**Command for Windows when use [AutoHotkey](https://AutoHotkey.com):**
```sh
; trigger-hotkeys.ahk
; AutoHotkey v2 Skript
#SingleInstance Force ; Stellt sicher, dass nur eine Instanz des Skripts läuft

;===================================================================
; Hotkey zum Auslösen des STT Triggers
; Drücke Strg + Alt + T, um die Trigger-Datei zu schreiben.
;===================================================================
f9::
f10::
f11::
{
    local TriggerFile := "c:\tmp\sl5_record.trigger"
    FileAppend("t", TriggerFile)
    ToolTip("STT Trigger ausgelöst!")
    SetTimer(() => ToolTip(), -1500)
}
```


### 3. Start Dictating!
Click in any text field, press your hotkey, and a "Listening..." notification will appear. Speak clearly, then pause. The corrected text will be typed for you.

---


## Advanced Configuration (Optional)

You can customize the application's behavior by creating a local settings file.

1.  Navigate to the `config/` directory.
2.  Create a copy of `settings_local.py_Example.txt` and rename it to `settings_local.py`.
3.  Edit `settings_local.py` to override any setting from the main `config/settings.py` file.

This `settings_local.py` file is ignored by Git, so your personal changes won't be overwritten by updates.


## Key Scripts for Windows Users

Here is a list of the most important scripts to set up, update, and run the application on a Windows system.

### Setup & Update
*   `setup/setup.bat`: The main script for the **initial one-time setup** of the environment.
* [or](https://github.com/sl5net/SL5-aura-service/actions/runs/16548962826/job/46800935182) `Run powershell -Command "Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .\setup\windows11_setup.ps1"`

*   `update.bat` : Rund these from Project folder **get the latest code and dependencies**.

### Running the Application
*   `start_dictation_v2.0.bat`: A primary script to **start the dictation service**.

### Core & Helper Scripts
*   `dictation_service.py`: The core Python service (usually started by one of the scripts above).
*   `get_suggestions.py`: A helper script for specific functionalities.




## 🚀 Key Features & OS Compatibility

Legend for OS Compatibility:  
*   🐧 **Linux** (e.g., Arch, Ubuntu)  
*   🍏 **macOS**  
*   🪟 **Windows**  
*   📱 **Android** (for mobile-specific features)  

---

### **Core Speech-to-Text (STT) Engine**
    Our primary engine for offline speech recognition and audio processing.

**STT-Core/** 🐧 🍏 🪟  
├─ `dictation_service.py` (Main Python service orchestrating STT) 🐧 🍏 🪟  
├┬ **Live Hot-Reload** (Config & Maps) 🐧 🍏 🪟  
│├ **Text Processing & Correction/** Grouped by Language ( e.g. `de-DE`, `en-US`, ... )   
│├ 1. `normalize_punctuation.py` (Standardizes punctuation post-transcription) 🐧 🍏 🪟  
│├ 2. **Intelligent Pre-Correction** (`FuzzyMap Pre` - applied before LT for performance) 🐧 🍏 🪟  
│├ 3. `correct_text_by_languagetool.py` (Integrates LanguageTool for grammar/style correction) 🐧 🍏 🪟  
│└ 4. **Intelligent Post-Correction** (`FuzzyMap` - applied behind LT) 🐧 🍏 🪟  
├┬ **Model Management/**   
│├─ `prioritize_model.py` (Optimizes model loading/unloading based on usage) 🐧 🍏 🪟  
│└─ `setup_initial_model.py` (Configures the first-time model setup) 🐧 🍏 🪟  
├─ **Adaptive VAD Timeout** 🐧 🍏 🪟  
├─ **Adaptive Hotkey (Start/Stop)** 🐧 🍏 🪟  
└─ **Instant Language Switching** (via model preloading) 🐧 🍏 🪟

**SystemUtilities/**   
├┬ **LanguageTool Server Management/**   
│├─ `start_languagetool_server.py` (Initializes the local LanguageTool server) 🐧 🍏 🪟  
│└─ `stop_languagetool_server.py` (Shuts down the LanguageTool server) 🐧 🍏 
├─ `monitor_mic.sh` (e.g. for use with Headset without use keyboard and Monitor) 🐧 🍏 🪟  

### **Model & Package Management**  
    Tools for robust handling of large language models.  

**ModelManagement/** 🐧 🍏 🪟  
├─ **Robust Model Downloader** (GitHub Release chunks) 🐧 🍏 🪟  
├─ `split_and_hash.py` (Utility for repo owners to split large files and generate checksums) 🐧 🍏 🪟  
└─ `download_all_packages.py` (Tool for end-users to download, verify, and reassemble multi-part files) 🐧 🍏 🪟  


### **Development & Deployment Helpers**  
    Scripts for environment setup, testing, and service execution.  

**DevHelpers/**  
├┬ **Virtual Environment Management/**  
│├ `scripts/restart_venv_and_run-server.sh` (Linux/macOS) 🐧 🍏  
│└ `scripts/restart_venv_and_run-server.ahk` (Windows) 🪟  
├┬ **System-wide Dictation Integration/**  
│├ Vosk-System-Listener Integration 🐧 🍏 🪟  
│├ `scripts/monitor_mic.sh` (Linux-specific microphone monitoring) 🐧  
│└ `scripts/type_watcher.ahk` (AutoHotkey listens for recognized text and types it out system-wide) 🪟  
└─ **CI/CD Automation/**  
    └─ Expanded GitHub Workflows (Installation, testing, docs deployment) 🐧 🍏 🪟 *(Runs on GitHub Actions)*  

### **Upcoming / Experimental Features**  
    Features currently under development or in draft status.  

**ExperimentalFeatures/**  
├─ **ENTER_AFTER_DICTATION_REGEX** Example activation rule "(ExampleAplicationThatNotExist|Pi, your personal AI)" 🐧  
├┬Plugins
│╰┬ **Live Lazy-Reload** (*) 🐧 🍏 🪟  
(*Changes to Plugin activation/deactivation, and their configurations, are applied on the next processing run without service restart.*)
│ ├ **git commands** (Voice control for send git commands) 🐧 🍏 🪟  
│ ├ **wannweil** (Map for Location Germany-Wannweil) 🐧 🍏 🪟  
│ ├ **Poker Plugin (Draft)** (Voice control for poker applications) 🐧 🍏 🪟  
│ └ **0 A.D. Plugin (Draft)** (Voice control for 0 A.D. game) 🐧   
├─ **Sound Output when Start or End a Session** (Description pending) 🐧   
├─ **Speech Output for Visually Impaired** (Description pending) 🐧 🍏 🪟  
└─ **SL5 Aura Android Prototype** (Not fully offline yet) 📱  

---

*(Note: Specific Linux distributions like Arch (ARL) or Ubuntu (UBT) are covered by the general Linux 🐧 symbol. Detailed distinctions might be covered in installation guides.)*









<details>
<summary>Click to see the command used to generate this script list</summary>

```bash
{ find . -maxdepth 1 -type f \( -name "dictation_service.py" -o -name "get_suggestions.py" \) ; find . -path "./.venv" -prune -o -path "./.env" -prune -o -path "./backup" -prune -o -path "./LanguageTool-6.6" -prune -o -type f \( -name "*.bat" -o -name "*.ahk" -o -name "*.ps1" \) -print | grep -vE "make.bat|notification_watcher.ahk"; }
```
</details>


### bit grafically look to see whats behind:

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


# Used Models:

Recommendation: use models from Mirror https://github.com/sl5net/SL5-aura-service/releases/tag/v0.2.0.1 (probably faster)

This Ziped models must be saved into `models/` folder

`mv vosk-model-*.zip models/`


| Model                                                                                  | Size | Word error rate/Speed                                                                         | Notes                                     | License    |
| -------------------------------------------------------------------------------------- | ---- | --------------------------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| [vosk-model-en-us-0.22](https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip) | 1.8G | 5.69 (librispeech test-clean)<br/>6.05 (tedlium)<br/>29.78 (callcenter)                       | Accurate generic US English model         | Apache 2.0 |
| [vosk-model-de-0.21](https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip)       | 1.9G | 9.83 (Tuda-de test)<br/>24.00 (podcast)<br/>12.82 (cv-test)<br/>12.42 (mls)<br/>33.26 (mtedx) | Big German model for telephony and server | Apache 2.0 |

This table provides an overview of different Vosk models, including their size, word error rate or speed, notes, and license information.


- **Vosk-Models:** [Vosk-Model List](https://alphacephei.com/vosk/models)
- **LanguageTool:**  
   (6.6) [https://languagetool.org/download/](https://languagetool.org/download/) 

**License of LanguageTool:** [GNU Lesser General Public License (LGPL) v2.1 or later](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)

---

## Support the Project
If you find this tool useful, please consider buying us a coffee! Your support helps fuel future improvements.

[![ko-fi](https://storage.ko-fi.com/cdn/useruploads/C0C445TF6/qrcode.png?v=5151393b-8fbb-4a04-82e2-67fcaea9d5d8?v=2)](https://ko-fi.com/C0C445TF6)

[Stripe-Buy Now](https://buy.stripe.com/3cIdRa1cobPR66P1LP5kk00)


