REM setup/windows11_setup_with_ahk_copyq.bat
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

cd /d "%~dp0"

REM 1. Call the existing core setup script
REM Now running with Admin rights, so the PS1 won't try to crash-elevate itself.

@REM  -Exclude 'en'"
 
CALL "%~dp0windows11_setup.bat" -Exclude 'en'
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
@REM setup/windows11_setup_with_ahk_copyq.bat:34
powershell.exe -ExecutionPolicy Bypass -File "%~dp0install_ahk_copyq.ps1"





call "%~dp0glogg_installer.bat"


REM --- FZF INSTALLATION START ---
ECHO Installing fzf (Fuzzy Finder)...
winget install -e --id junegunn.fzf --source winget --accept-package-agreements --accept-source-agreements
IF %ERRORLEVEL% NEQ 0 (
    ECHO fzf was already installed or an error occurred.
) ELSE (
    ECHO fzf installed successfully.
)
REM --- FZF INSTALLATION END ---




ECHO.
ECHO ========================================================
ECHO Installation finished.
ECHO start "Aura Dictation" (maybe ~ 30s)...
ECHO ========================================================

@REM CALL "%~dp0..\start_dictation_v2.1.bat"
START "" explorer "%~dp0..\start_dictation_v2.1.bat"

