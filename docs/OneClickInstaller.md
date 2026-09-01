# 1-Click Installer (Zero-Setup)

Get **Aura** up and running on your machine with a single click. No programming knowledge, terminal commands, or manual Python setup required.

---

## Zero Prerequisites

You do **not** need:
- Python pre-installed
- Git or code repositories
- Command-line or terminal experience

---

## Quick Start

### Method 1: Web One-Liner (Fastest & Recommended for Linux / macOS)
Saves ~30 seconds of manual file handling and starts immediately in your terminal:

**Linux & macOS:**
#### Web One-Liner CodeBerg
```bash
curl -sSL https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | bash
```
or
#### Web One-Liner GitHub
```bash
curl -sSL https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.sh | bash
```

**Windows (PowerShell):**
#### Web One-Liner CodeBerg
# not tested - please use Method 2 (standalone binary) for Windows
```bash
irm https://codeberg.org/seeh/SL5-aura-service/raw/branch/master/web_install.sh | iex
```
or
#### Web One-Liner github
```bash
irm https://raw.githubusercontent.com/sl5net/SL5-aura-service/master/web_install.ps1 | iex
```

Method 2: Standalone Binary (Windows & Desktop Click)

### 2.1 Download the Installer
Download the single installer file matching your operating system from the [Latest GitHub Release]:

- **Windows:** [aura-installer-windows.exe](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-windows.exe.zip)
- **Linux:** [aura-installer-linux](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-linux)
- **macOS:** [aura-installer-macos](https://github.com/sl5net/SL5-aura-service/releases/latest/download/aura-installer-macos)


### 2.2. Run the Installer

rename aura-installer-windows.exe.zip to aura-installer-windows.exe

Double-click the downloaded file. A setup window will appear and automatically prepare the environment.

### 2.3. Start Dictating
Once finished, Aura creates a desktop shortcut and starts listening immediately.

---

## What Happens Automatically?

When you run the installer, Aura automatically:
- Configures the local, private speech recognition engine.
- Downloads the default voice models.
- Sets up all necessary system shortcuts and desktop launchers.

---

## Installation Details & Requirements

- **Installation Duration:** Approximately 2–3 minutes.
- **Disk Space Required:** Minimum ~1.5 GB (up to 2.5 GB depending on selected language models).
- **Installation Directory:**
  - **Linux & macOS:** `~/opt/sl5-aura-service`
  - **Windows:** `%LOCALAPPDATA%\sl5-aura-service`

---

## Next Steps

- **Grandma-Mode:** Type a single word into your rule file and watch Aura auto-create rules.
- **Learn with Koans:** Explore step-by-step concepts in [Getting Started](GettingStarted.md).
