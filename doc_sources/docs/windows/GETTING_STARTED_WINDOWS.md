# Getting Started on Windows

## Step 1: Run the Setup
Double-click `setup/windows11_setup_with_ahk_copyq.bat`.
- Right-click → "Run as administrator" if prompted.
- The script installs Python, AutoHotkey v2, CopyQ, and downloads the voice models (~4GB).
- This takes approximately 8-10 minutes.

## Step 2: Start Aura
Double-click `start_aura.bat` in the project folder.
You should hear a startup sound — Aura is ready.

**Nothing happened?** Check the log:
log\aura_engine.log

## Step 3: Configure Your Hotkey
The setup installs CopyQ automatically. To trigger dictation:
1. Open CopyQ → Commands → Add command
2. Set the command to:
cmd /c echo. > C:\tmp\sl5_record.trigger
3. Assign a global shortcut (e.g. `F9`)

## Step 4: First Dictation
1. Click into any text field
2. Press your hotkey — wait for the "Listening..." notification
3. Say "Hello World"
4. Press the hotkey again — the text appears

## Step 5: Find Voice Commands
Say: **"Aura Search"** — a window opens with all available rules.

## Troubleshooting
| Symptom | Fix |
|---|---|
| No startup sound | Check `log\aura_engine.log` |
| Hotkey does nothing | Check if `C:\tmp\sl5_record.trigger` is created |
| Text not typed | Check if `type_watcher.ahk` is running in Task Manager |
| Crash on start | Run setup again as Administrator |

> Full troubleshooting: [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
