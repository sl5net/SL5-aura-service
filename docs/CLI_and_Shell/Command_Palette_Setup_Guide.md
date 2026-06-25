# Command Palette & Map Search Guide

This guide explains how to set up and use the system-wide, location-independent **Command Palette** for SL5 Aura. It allows you to search through your Map Rules interactively, see live execution previews from the local SQLite cache, and instantly type the selected output at your active cursor.

## Prerequisites

Ensure the following background services and tools are installed and active:
1. **`fzf`** (Fuzzy Finder)
2. **CopyQ** (Clipboard Manager, used for global hotkey orchestration)
3. **`type_watcher.sh`** (Aura background typing daemon)

---

## CopyQ Global Shortcut Setup

To launch the Command Palette instantly from any active window (e.g., your browser or text editor), configure a global hotkey in CopyQ:

1. Open **CopyQ** and press `F6` (or go to **Commands** / **Befehle**).
2. Click **Add** (Hinzufügen) and name it `Aura Command Palette`.
3. Set your desired **Global Shortcut** (e.g., `Meta+S` or `Ctrl+Alt+S`).
4. Set the **Type** to `Command` (Befehl).
5. Paste the following JavaScript code in the command box:

```javascript
copyq:
// Hardcoded Linux config
var isWindows = false;
var tmp_dir = isWindows ? 'C:/tmp' : '/tmp';

// Dynamically resolve PROJECT_ROOT from Aura temp configuration
var rootFile = File(tmp_dir + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';

if (rootFile.open()) {
    project_root = str(rootFile.readAll()).replace(/[\r\n]/g, '').trim();
    rootFile.close();
}

if (!project_root) {
    project_root = '~/projects/py/STT'; // Default fallback path
}

var search_script = project_root + '/scripts/search_rules/search_rules.sh';

// Execute floating terminal window running the search script
execute('konsole', '-e', 'bash', '-c', 'SEARCH_FILES_FILTER="*.py|*.txt|*.md" bash "' + search_script + '"');
