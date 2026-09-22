> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../Command_Palette_Setup_Guide.md).*

# Command Palette & Map Search Guide

This guide explains how to set up and use the system-wide, location-independent **Command Palette** for SL5 Aura. It allows you to search through your Map Rules interactively, see live execution previews from the local SQLite cache, and instantly type the selected output at your active cursor.

## Prerequisites

Ensure the following background services and tools are installed and active:
1. `fzf` (Fuzzy Finder)
2. **CopyQ** (Clipboard Manager, used for global hotkey orchestration)
3. `type_watcher.sh`** (Aura background typing daemon)

---

CopyQ Global Shortcut Setup

To launch the Command Palette instantly from any active window (e.g., your browser or text editor), configure a global hotkey in CopyQ:

1. Open **CopyQ** and press `F6` (or go to **Commands** / **Commands**).
2. Click **Add** and name it `Aura Command Palette`.
3. Set your desired **Global Shortcut** (e.g., `Meta+S` or `Ctrl+Alt+S`).
4. Set the **Type** to `Command` (command).
5. Paste the following JavaScript code in the command box:

__CODE_BLOCK_0__
