@echo off
ECHO start Windows 11 Setup-Script...

REM PowerShell, use Execution Policy this time
powershell.exe -ExecutionPolicy Bypass -File "%~dp0\windows11_setup.ps1"

call .\.venv\Scripts\python.exe scripts/py/func/setup_initial_model.py

ECHO
ECHO Script is ended.
ECHO You can close the window
pause
