@echo off
setlocal

:: Resolve the absolute parent directory of the script's folder
set /p PROJECT_ROOT=<"C:\tmp\sl5_aura\sl5net_aura_project_root"

:: Define the PowerShell update script path
set "UPDATE_SCRIPT=%PROJECT_ROOT%\update\update_for_windows_users.ps1"

echo.
echo ====================================================================
echo SL5 Aura Auto-Updater (5-min interval)
echo Monitoring branch: %PROJECT_ROOT%
echo To stop, close this window or press Ctrl+C.
echo ====================================================================
echo.

:loop
    echo [%DATE% %TIME%] Checking for updates...
    :: Set environment variable to bypass the interactive prompt inside PowerShell
    set "AURA_AUTO_UPDATE=true"
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%UPDATE_SCRIPT%"

    echo [%DATE% %TIME%] Update check complete.
    echo Press ANY KEY to check again immediately, or wait 5 minutes...
    timeout /t 300
goto loop
