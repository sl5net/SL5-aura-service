@echo off
setlocal

:: Resolve the absolute project root path dynamically
for %%i in ("%~dp0.") do set "PROJECT_ROOT=%%~fi"

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
    :: Execute the PowerShell script. -NoProfile avoids loading user's PS profile.
    :: -ExecutionPolicy Bypass allows the script to run without interactive prompts.
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%UPDATE_SCRIPT%"

    echo [%DATE% %TIME%] Update check complete. Waiting 5 minutes...
    timeout /t 300 /nobreak > nul
goto loop

endlocal
