@echo off
setlocal
title SL5 Aura - One-Click Starter

:: cmd /k "echo on & call start_dictation_v2.1.bat"


echo DBG1: before cd
cd /d "%~dp0"



:: start this script like: & .\start_dictation_v2.1.bat
:: Version: v2.1
;;

:: --- 2. Admin Rights Check ---
echo [*] Checking for Administrator privileges

REM Only check for admin rights if NOT running in a CI environment
if /I NOT "%CI%"=="true" (
    net session >nul 2>&1
    if %errorLevel% neq 0 (
        echo [ERROR] Re-launching with Admin rights...
        REM update test: 2026-0122-1421
        REM  powershell -Command "Start-Process '%~f0' -Verb RunAs"

        REM powershell -Command "Start-Process cmd -ArgumentList '/c, %~f0' -Verb RunAs"

        REM Start-Process -FilePath "powershell.exe" -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File', $PSCommandPath) -Verb RunAs

        REM Start-Process -FilePath "powershell.exe" -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File', $PSCommandPath -Verb RunAs
        REM powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0\start_dictation_v2.0.ps1"
        powershell -Command "Start-Process cmd -ArgumentList '/c, """%~f0"""' -Verb RunAs"


        exit /b
    )
)
















echo [SUCCESS] Running with Administrator privileges.

echo DBG8: about to check venv
if not exist ".\.venv\Scripts\python.exe" (
  echo DBG9: venv missing
  pause
  powershell.exe -ExecutionPolicy Bypass -File ".\setup\windows11_setup.ps1" -Exclude "en"
  if not exist ".\.venv\Scripts\python.exe" (
    echo DBG10: venv still missing
    pause
    exit /b
  )
  echo DBG11: venv created
)
echo DBG12: after venv block

echo DBG13: stop processes via powershell 1

powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*type_watcher.ahk*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo DBG14: after ps1

powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*notification_watcher.ahk*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo DBG15: after ps2

powershell -NoProfile -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and ($_.CommandLine -like '*trigger-hotkeys.ahk*') } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

echo DBG16: after ps3

set "AHK_EXE="
if exist "%ProgramFiles%\AutoHotkey\v2\AutoHotkey64.exe" set "AHK_EXE=%ProgramFiles%\AutoHotkey\v2\AutoHotkey64.exe"
if exist "%ProgramFiles%\AutoHotkey\AutoHotkey.exe" if not defined AHK_EXE set "AHK_EXE=%ProgramFiles%\AutoHotkey\AutoHotkey.exe"
if not defined AHK_EXE (
    echo [WARNING] AutoHotkey executable not found in %ProgramFiles%. Trying file association instead.
)


echo DBG17: about to start AHK processes
start "" "%AHK_EXE%" "%~dp0scripts\notification_watcher.ahk" >nul 2>&1
echo DBG18: started notification_watcher
start "" "%AHK_EXE%" "%~dp0trigger-hotkeys.ahk" >nul 2>&1
echo DBG19: started trigger-hotkeys
start "" "%AHK_EXE%" "%~dp0type_watcher.ahk" >nul 2>&1
echo DBG20: started type_watcher

echo DBG21: checking errorlevel=%errorlevel%
if "%errorlevel%"=="0" (
  echo [INFO] Admin-Hotkeys are already running.
) else (
  echo [INFO] Starting Hotkeys in User-Mode...
  timeout /t 2 /nobreak >nul
  start "" "%~dp0trigger-hotkeys.ahk"
)
echo DBG22: after hotkey-start
echo [INFO] Background watchers have been started.


# there should be a task (when you not admin) AuraDictation_Hotkeys (for use keys like F10) that is already installed during installation as admin.
# maybe we should check this also in the start script?


:START_SERVICE_LOOP
echo [INFO] Starting the Python STT backend service...

.venv\Scripts\activate

:: python -u aura_engine.py
python -X utf8 -u aura_engine.py

echo [INFO] Waiting 5 seconds for the service to initialize...
timeout /t 5 >nul

echo [INFO] Verifying service status via log file...
findstr /C:"Setup validation successful" "log\aura_engine.log" >nul 2>&1
IF "%errorlevel%"=="0" goto :CONTINUE_SCRIPT

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
type nul > "C:\tmp\sl5_record.trigger"

echo.

:: --- Final Success Message - ENTFERNT die doppelte Meldung ---
echo [SUCCESS] SL5 Aura is now running in the background.
echo This window will close automatically in a few seconds.
timeout /t 5 > nul

