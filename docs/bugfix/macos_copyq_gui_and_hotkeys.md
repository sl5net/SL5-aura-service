# CopyQ macOS Troubleshooting: Invisible GUI and Manual Hotkey Configuration

This guide addresses common issues encountered on macOS (specifically Apple Silicon M-series devices) where the CopyQ graphical interface (GUI) does not appear, or global shortcuts (such as F10) need to be reassigned without accessing the GUI.

---

## 1. Troubleshooting the Invisible GUI

On macOS, CopyQ may run properly in the background while remaining visually hidden for two main reasons:
- **Off-Screen Window Coordinates**: Following resolution changes or disconnecting an external monitor, CopyQ may retain coordinates outside the visible display area.
- **Menu Bar Notch Obstruction**: On MacBook models with a camera notch, macOS automatically conceals excess menu bar icons behind the notch when the tray is full.

### Solution: Reset Geometry and Force Display

Execute the following commands in the terminal to clear off-screen coordinates and bring the window to the foreground:

```bash
copyq config geometry ""
copyq show
```

If the window still does not surface, toggle its state via CLI:

```bash
copyq toggle
```

---

## 2. Manually Changing Hotkeys Using CudaText

When a global shortcut (such as `F10`) is claimed or intercepted by another application, the shortcut can be edited directly in the configuration file using CudaText without opening the CopyQ GUI.

### Step 1: Terminate the CopyQ Process

CopyQ must be stopped before editing the configuration file to prevent it from overwriting your changes upon termination:

```bash
copyq exit
```

### Step 2: Open the Configuration in CudaText

On macOS, CopyQ command shortcuts are stored in `copyq-commands.ini`.

Open the file in CudaText:

```bash
cudatext "$HOME/Library/Application Support/copyq/copyq-commands.ini"
```

*Note: If the file does not exist in `Application Support`, open the XDG fallback location:*

```bash
cudatext "$HOME/.config/copyq/copyq-commands.ini"
```

### Step 3: Reassign the Shortcut

1- In CudaText, press `Cmd + F` to open the search bar.
2- Search for `F10` or `GlobalShortcut=F10`.
3- Replace `F10` with an available shortcut (e.g., `F9` or `Ctrl+F10` or `Meta+F10`).
4- Save the file (`Cmd + S`) and close CudaText (`Cmd + Q`).

### Step 4: Restart CopyQ

Start CopyQ again to load the updated shortcut configuration:

```bash
open -a CopyQ
```

The new global shortcut will now be active.

(updated: 8.9.'26 08:01 Tue)
