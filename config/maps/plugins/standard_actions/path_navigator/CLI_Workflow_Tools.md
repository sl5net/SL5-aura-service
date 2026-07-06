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



## 1. Fast File Selection (Aura Command)

The `path_navigator` action uses the following Git-aware `fzf` command. Its purpose is to output a file path directly into the system clipboard.

**Command Logic:**
- Uses `git ls-files` inside a Git repository (excludes ignored files).
- Falls back to `find . -type f` outside a Git repository.
- Outputs the selected path to the clipboard using `xclip -selection clipboard`.

## 2. Fast File Execution (The 'k' Function)

To complete the loop, the custom shell function `k` is used. This function takes the path from the clipboard and instantly opens the file in `kate`.

### Implementation

Add the following function to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

### Usage

1.  Use the `path_navigator` command (e.g., type `search file` in your trigger tool).
2.  Find and select the desired file (e.g., `src/main/config.py`).
3.  In your terminal, type `k` and press **ENTER**.
4.  The file opens instantly in Kate.
```
