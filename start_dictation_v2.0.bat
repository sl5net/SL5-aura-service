:: start this script like: & .\start_dictation_v2.0.bat
:: Version: v2.1

@echo off
setlocal
title SL5 Aura - One-Click Starter

:: --- Step 1: Set correct working directory ---
cd /d "%~dp0"

:: --- 2. Admin Rights Check ---
echo [*] Checking for Administrator privileges

REM Only check for admin rights if NOT running in a CI environment
if /I NOT "%CI%"=="true" (
    net session >nul 2>&1
    if %errorLevel% neq 0 (
        echo [ERROR] Re-launching with Admin rights...
        Rem powershell -Command "Start-Process '%~f0' -Verb RunAs"

        Rem powershell -Command "Start-Process cmd -ArgumentList '/c, %~f0' -Verb RunAs"

        Start-Process -FilePath "powershell.exe" -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File', $PSCommandPath) -Verb RunAs


        exit /b
    )
)

echo [SUCCESS] Running with Administrator privileges.

:: --- Step 3: VEREINFACHT - Check if venv exists, otherwise run full setup ---
if not exist ".\.venv\Scripts\python.exe" (
    echo [WARNING] Virtual environment is missing or incomplete.
    echo [ACTION] Running full setup. This may take a moment...
    pause

    REM  .\setup\windows11_setup.ps1 -Exclude "en" or .\setup\windows11_setup.ps1 -Exclude "de" or .\setup\windows11_setup.ps1 -Exclude "all".

    powershell.exe -ExecutionPolicy Bypass -File ".\setup\windows11_setup.ps1" -Exclude "en"

    if not exist ".\.venv\Scripts\python.exe" (
        echo [FATAL] Automated setup failed. Please check setup script.
        pause
        exit /b
    )
    echo [SUCCESS] Virtual environment has been set up successfully.
)
echo.

:: --- Step 4: Start background components ---
start "SL5 Type Watcher.ahk" type_watcher.ahk
start "SL5 Notification Watcher.ahk" scripts\notification_watcher.ahk
start "trigger-hotkeys.ahk" trigger-hotkeys.ahk
echo [INFO] Background watchers have been started.
echo.

:: --- Step 5: Activate venv and start the main service with auto-repair ---
echo [INFO] Activating virtual environment...
call .\.venv\Scripts\activate.bat

set REPAIR_ATTEMPTED=

:START_SERVICE_LOOP
echo [INFO] Starting the Python STT backend service...

# python -u aura_engine.py
python -X utf8 -u aura_engine.py

echo [INFO] Waiting 5 seconds for the service to initialize...
timeout /t 5 >nul

echo [INFO] Verifying service status via log file...
findstr /C:"Setup validation successful" "log\aura_engine.log" >nul 2>&1
IF %ERRORLEVEL% EQU 0 goto :CONTINUE_SCRIPT

:: --- ERROR HANDLING & REPAIR ---
echo [WARNING] Service verification failed. Log does not contain success signal.
if defined REPAIR_ATTEMPTED (
    echo [FATAL] The automatic repair attempt has failed. Please check setup manually.
    pause
    exit /b 1
)
echo [ACTION] Attempting automatic repair by reinstalling dependencies...
set REPAIR_ATTEMPTED=true
call .\.venv\Scripts\python.exe -m pip install -r requirements.txt
echo [INFO] Repair finished. Retrying service start...
echo.
goto :START_SERVICE_LOOP

:CONTINUE_SCRIPT
echo [INFO] Service verification successful.
echo [*] Triggering the service...
echo. >> "c:/tmp/sl5_record.trigger"
echo.

:: --- Final Success Message - ENTFERNT die doppelte Meldung ---
echo [SUCCESS] SL5 Aura is now running in the background.
echo This window will close automatically in a few seconds.
timeout /t 5 > nul
