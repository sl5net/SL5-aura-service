REM uninstall_ahk_copyq.bat
REM script_name: setup/uninstall_ahk_copyq.bat
@echo off
ECHO Starting Uninstallation of Client Tools (AutoHotkey + CopyQ)...

REM --- ADMIN CHECK START ---
REM Uninstallations via Winget/MSI usually require Admin privileges.
FSUTIL dirty query %systemdrive% >nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~dpnx0\"\" %* ' -Verb RunAs"
    EXIT /B
)
ECHO [OK] Admin privileges confirmed.
REM --- ADMIN CHECK END ---


REM Ensure we are in the script directory to find the ps1 file
CD /D "%~dp0"

ECHO Running uninstallation script...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0\uninstall_ahk_copyq.ps1"

ECHO.
ECHO Uninstallation process completed.
PAUSE
