@echo off
cd /d "%~dp0"

set INSTALLER=glogg-latest-x86_64-setup.exe
set URL=http://glogg.bonnefon.org/files/%INSTALLER%
if exist "%ProgramFiles%\glogg\glogg.exe" (
    echo glogg is already installed.
    exit /b
)
echo Downloading %INSTALLER%...
powershell -Command "Invoke-WebRequest -Uri '%URL%' -OutFile '%INSTALLER%'"
echo Installing glogg...
:: /S = Silent
:: /D=Path = Optional output directory
"%INSTALLER%" /S
del "%INSTALLER%"
echo glogg installation complete.

reg add "HKCR\*\shell\Open with glogg" /ve /d "Open with glogg" /f
reg add "HKCR\*\shell\Open with glogg\command" /ve /d "\"C:\Program Files\glogg\glogg.exe\" \"%1\"" /f

