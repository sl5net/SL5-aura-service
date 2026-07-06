# CLI Workflow Tools Installation Guide

Some actions in the path navigator plugin rely on external command-line utilities to perform fuzzy searches, list files, and manipulate the clipboard. If these tools are missing, you will see a warning in the system console.

Below are the installation instructions for each supported operating system.

## Required Utilities

* **`fzf`**: General-purpose command-line fuzzy finder.
* **`find`** (or `fd`): Standard file-searching utility.
* **Clipboard Tool**: Used to pipe output directly to your system clipboard.
  * **Linux:** `xclip` (requires X11 environment).
  * **macOS:** `pbcopy` (pre-installed).
  * **Windows:** `clip` (pre-installed).
* **`file`**: Determines file types for full terminal previews.

---

## Installation Instructions

### 1. Linux (Arch / Manjaro)
Since your system runs on Manjaro, you can install the required packages using `pacman`:

```bash
sudo pacman -S fzf findutils xclip file
```

### 2. Linux (Debian / Ubuntu / Mint)
On Debian-based systems, use `apt`:

```bash
sudo apt update
sudo apt install fzf findutils xclip file
```

### 3. macOS
Use the [Homebrew](https://brew.sh/) package manager to install the missing tools:

```bash
brew install fzf findutils
# Note: 'pbcopy' and 'file' are native on macOS.
```

### 4. Windows
If you are using Windows, we recommend installing `fzf` via [Scoop](https://scoop.sh/) or [Winget](https://github.com/microsoft/winget-cli):

```powershell
# Using Winget
winget install junegunn.fzf

# Using Scoop
scoop install fzf
```
```

