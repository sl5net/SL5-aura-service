# System-Wide Offline Dictation, Correction, and Suggestion Tool

This project provides a powerful, system-wide dictation tool that goes beyond simple speech-to-text. It **automatically corrects** your dictated text, **suggests synonyms** to improve your writing, and even includes a hotkey to **look up homophones** (e.g., "there" vs. "their") for any word on your screen.

It's a complete, offline writing assistant built on Vosk and LanguageTool.

[![Watch short AI-Demo System-wide offline dictation](https://img.youtube.com/vi/-Qxd3qQFmPo/maxresdefault.jpg)](https://youtu.be/-Qxd3qQFmPo)


## Key Features

*   **Offline & Private:** 100% local. No data ever leaves your machine.
*   **Dictate, Correct & Enhance:** Automatic grammar/spelling correction and synonym suggestions.
*   **Conservative RAM Usage:** Intelligently manages memory, preloading models only if enough free RAM is available, ensuring other applications (like your PC games) always have priority.
*   **Cross-Platform:** Works on Linux, macOS, and Windows.
*   **Fully Automated:** Manages its own LanguageTool server. A single script handles the startup process on Linux/macOS.
*   **Blazing Fast:** Intelligent caching ensures instant "Listening..." notifications and fast processing.

## Documentation

For a complete technical reference, including all modules and scripts, please visit our official documentation page. It is automatically generated and always up-to-date.

[**Go to Documentation >>**](https://sl5net.github.io/Vosk-System-Listener/)


### Build Status
[![Linux](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/ubuntu_setup.yml/badge.svg)](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/ubuntu_setup.yml)
[![macOS](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/macos_setup.yml/badge.svg)](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/macos_setup.yml)
[![Windows 11](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/windows11_setup.yml/badge.svg)](https://github.com/sl5net/Vosk-System-Listener/actions/workflows/windows11_setup.yml)
[![Documentation](https://img.shields.io/badge/documentation-live-brightgreen)](https://sl5net.github.io/Vosk-System-Listener/)

---

## Installation

The setup is a simple, two-step process:
1.  Clone this repository to your computer.
2.  Run the one-time setup script for your operating system.

The setup scripts handle everything: system dependencies, Python environment, and downloading the necessary models and tools (~4GB) directly from our GitHub Releases for maximum speed.

#### For Linux & macOS & windows
Open a terminal in the project's root directory and run the script for your system:
```bash
# For Ubuntu/Debian, Manjaro/Arch, macOs  or other derivatives

bash setup/{your-os}_setup.sh

# For Windows in Admin-Powershell

setup/windows_setup.ps1
```

#### For Windows
1.  **Install [AutoHotkey v2](https://www.autohotkey.com/)**. This is required for the text-typing watcher.
2.  Run the setup script with administrator privileges **"Run with PowerShell"**.

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

1.  **Start the Main Service:** Run `activate-venv_and_run-server.bat`. or start from `.venv` the service with `python3`
2.  **Start the Text Watcher:** Double-click `type_watcher.ahk`.



You must have both the main service and the watcher running for dictation to work.

### 2. Configure Your Hotkey

To trigger dictation, you need a global hotkey that creates a specific file. We highly recommend the cross-platform tool [CopyQ](https://github.com/hluk/CopyQ).

#### Our Recommendation: CopyQ

Create a new command in CopyQ with a global shortcut.

**Command for Linux/macOS:**
```bash
touch /tmp/sl5_record.trigger
```

**Command for Windows use [CopyQ](https://github.com/hluk/CopyQ):**
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

### 3. Start Dictating!
Click in any text field, press your hotkey, and a "Listening..." notification will appear. Speak clearly, then pause. The corrected text will be typed for you.

---

### bit grafically look to see whats behind:

      
![pydeps -v -o dependencies.svg scripts/py/func/main.py](doc_sources/dependencies.svg)


## Advanced Configuration (Optional)

You can customize the application's behavior by creating a local settings file.

1.  Navigate to the `config/` directory.
2.  Create a copy of `settings_local.py_Example.txt` and rename it to `settings_local.py`.
3.  Edit `settings_local.py` to override any setting from the main `config/settings.py` file.

This `settings_local.py` file is ignored by Git, so your personal changes won't be overwritten by updates.

# Used Models:


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
