REM windows11_setup.bat
@echo off
ECHO start Windows 11 Setup-Script...

REM PowerShell, use Execution Policy this time
REM %* passes all arguments (e.g., -Exclude "en") given to the BAT file to the PowerShell script.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0\windows11_setup.ps1" %*

REM NOTE: The Python script call should ideally be inside the PowerShell script,
REM as the virtual environment (.\.venv) is only guaranteed to be set up *after* the PS1 script finishes.
REM Assuming the PS1 script now handles all necessary setup and model downloading/filtering.

call .\.venv\Scripts\python.exe scripts/py/func/setup_initial_model.py

ECHO
ECHO Script is ended.
ECHO You can close the window
REM pause

