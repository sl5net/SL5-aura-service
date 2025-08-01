:: start this script like: & .\start_dictation_v2.0.bat
:: Version: v2.0

@echo off
setlocal
title SL5 Dictation - One-Click Starter

:: --- Step 1: Set correct working directory ---
cd /d "%~dp0"

:: --- Step 2: Ensure Administrator privileges ---
echo [*] Checking for Administrator privileges
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo [INFO] Administrative privileges needed. Relaunching
    powershell.exe -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)
echo [SUCCESS] Running with Administrator privileges.
echo.

:: --- Step 3: Check virtual environment health and auto-repair ---
set VENV_HEALTHY=true
if not exist ".\.venv" (
    set VENV_HEALTHY=false
) else (
    :: echo -31-
    :: .venv/Scripts/activate
    echo -33-
    echo [*] Performing venv health check (checking for 'requests' module)
    ".\.venv\scripts\python" -c "import requests" >nul 2>&1
    if %errorLevel% NEQ 0 (
        echo [WARNING] Health check failed. 'requests' module not found in venv.
        set VENV_HEALTHY=false
    ) else (
       echo [SUCCESS] Virtual environment is healthy.
    )
)
echo -40-

if "%VENV_HEALTHY%"=="false" (
    echo [ACTION] Rebuilding the virtual environment. This may take a moment.
    if exist ".\.venv" (
        echo [INFO] Removing outdated virtual environment
        rmdir /s /q .\.venv
    )
    echo [INFO] Running full setup
    powershell.exe -ExecutionPolicy Bypass -File ".\setup\windows11_setup.ps1"

    echo [INFO] Re-validating environment after rebuild
    if not exist ".\.venv\Scripts\python" (
        echo [FATAL] Automated setup failed. Please check setup script.
        pause
        exit /b
    )
    echo [SUCCESS] Virtual environment has been rebuilt successfully.
)
echo.
echo -63-

start "SL5 Type Watcher" type_watcher.ahk
start "SL5 Notification Watcher" scripts\notification_watcher.ahk

echo -72-

echo [INFO] Aktiviere die virtuelle Python-Umgebung...
:: 'call' wird verwendet, damit die Umgebung im selben Fenster aktiv bleibt
call .\.venv\Scripts\activate.bat
if %errorLevel% NEQ 0 (
    echo [FATAL] Konnte die virtuelle Umgebung nicht aktivieren.
    pause
    exit /b
)

echo [INFO] Virtuelle Umgebung ist aktiv.
:: --- Start, Verifizierung und automatische Reparatur ---
set REPAIR_ATTEMPTED=

:START_SERVICE_LOOP
echo [INFO] Starte den Python STT Backend-Server...

:: Start the service in the background
start "SL5 Dictation" python -u dictation_service.py

echo [INFO] Warte 5 Sekunden, damit der Service starten kann...
timeout /t 5 >nul

echo [INFO] Pruefe, ob das "Setup validation successful" Signal geloggt wurde...

:: findstr setzt ERRORLEVEL 0, wenn der Text gefunden wird, sonst 1
findstr /C:"Setup validation successful" "log\dictation_service.log" >nul 2>&1

IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Erfolgs-Signal im Log gefunden. Service laeuft.
    goto :CONTINUE_SCRIPT
)

:: --- FEHLERBEHANDLUNG ---
echo [WARNING] Erfolgs-Signal im Log nicht gefunden.

if defined REPAIR_ATTEMPTED (
    echo [FATAL] Automatischer Reparaturversuch ist fehlgeschlagen.
    pause
    exit /b 1
)

echo [ACTION] Starte automatische Reparatur: Installiere 'requirements.txt' neu.
set REPAIR_ATTEMPTED=true
call .\.venv\Scripts\python.exe -m pip install -r requirements.txt

echo [INFO] Reparatur abgeschlossen. Versuche den Service erneut zu starten...
goto :START_SERVICE_LOOP


:CONTINUE_SCRIPT
:: Dein restliches Skript (Trigger, etc.)
echo [*] Triggering the service using the vosk_trigger file
echo. >> "c:/tmp/sl5_record.trigger"
echo [SUCCESS] SL5 Dictation ist jetzt aktiv.
timeout /t 4 >nul


:: --- Step 4: Launch all application components ---
:: echo [*] Launching SL5 Dictation components in the background
:: start "SL5 STT Backend" cmd /k "call .\scripts\restart_venv_and_run-server.sh > .\log\restart_venv_and_run-server_pre.log 2>&1"



echo [SUCCESS] SL5 Dictation is now running in the background.
echo This window will close automatically.
timeout /t 4 > nul
