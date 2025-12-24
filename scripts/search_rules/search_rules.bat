@echo off
setlocal

:: fzf for Windows: To make the script work, you will need to have fzf installed on
:: your Windows machine (you can get it via scoop install fzf, choco install fzf, or by downloading the .exe).


:: Change directory to the location of this batch file
cd /d "%~dp0"

:: Set policy and run the script in one command
powershell.exe -NoProfile -ExecutionPolicy RemoteSigned -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force; & '.\search_rules.ps1'"

exit /b
