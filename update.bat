@echo off
:: file: update.bat
:: Description: One-click updater for Windows users.
:: This script requests admin rights and then runs the main PowerShell update script.

pushd "%~dp0"


if "%CI%"=="true" goto run_script

:: ---------------------------------------------------------
:: 1. SCHREIB-TEST (Write Permission Check)
:: ---------------------------------------------------------
:: Wir versuchen, eine unsichtbare Test-Datei zu erstellen.
echo test > ".write_permission_check.tmp" 2>nul

if exist ".write_permission_check.tmp" (
    :: ERFOLG: Wir koennen schreiben!
    :: Datei wieder loeschen
    del ".write_permission_check.tmp"
    echo Schreibrechte vorhanden. Starten ohne Admin-Rechte...
    goto run_script
)




:: 1. Check for administrative privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo Requesting administrative privileges to run the updater...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /b
)

call "%~dp0setup\fix_permissions.bat"


:: 2. Now that we have admin rights, run the actual PowerShell updater script
::    -ExecutionPolicy Bypass: Temporarily allows the script to run without changing system settings.
::    -File: Specifies the script to execute.
:run_script
echo Starting the update process...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0update\update_for_windows_users.ps1"

echo.
echo The update script has finished. This window can be closed.

powershell -c "[System.Media.SystemSounds]::Asterisk.Play()"
