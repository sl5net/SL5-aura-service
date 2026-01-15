REM windows11_setup_with_ahk_copyq.bat
REM script_name: setup/windows11_setup_with_ahk_copyq.bat
@echo off
ECHO Starting Setup Variant: Core System + AutoHotkey + CopyQ...

REM --- ADMIN CHECK START ---
REM Force the script to run as Administrator.
REM If FSUTIL fails, we are not Admin -> Relaunch via PowerShell.
FSUTIL dirty query %systemdrive% >nul
IF %ERRORLEVEL% NEQ 0 (
    ECHO Requesting Administrator privileges...
    REM Restart this batch file with RunAs (Admin) and pass all original arguments
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~dpnx0\"\" %* ' -Verb RunAs"
    EXIT /B
)
ECHO Admin privileges confirmed.
REM --- ADMIN CHECK END ---

REM 1. Call the existing core setup script
REM Now running with Admin rights, so the PS1 won't try to crash-elevate itself.
CALL "%~dp0windows11_setup.bat" %*

REM Check if the core setup failed
IF %ERRORLEVEL% NEQ 0 (
    ECHO setup/windows11_setup_with_ahk_copyq.bat:25
    ECHO Core setup encountered errors. Skipping client tools installation.
@REM     PAUSE
@REM     EXIT /B %ERRORLEVEL%
)

ECHO Core setup completed. Moving to AHK and CopyQ installation...

REM 2. Run the specific client tools installation script
powershell.exe -ExecutionPolicy Bypass -File "%~dp0install_ahk_copyq.ps1"

ECHO Setup variant completed.
PAUSE
