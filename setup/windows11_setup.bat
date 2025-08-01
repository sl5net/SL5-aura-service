@echo off
ECHO Starte das Windows 11 Setup-Skript...

REM Dieser Befehl startet PowerShell, umgeht die Execution Policy NUR für diese eine Ausführung
REM und führt dein Skript aus. Der Pfad ist relativ, es funktioniert also immer.
powershell.exe -ExecutionPolicy Bypass -File "%~dp0\windows11_setup.ps1"

ECHO
ECHO Das Skript wurde beendet.
ECHO Du kannst dieses Fenster jetzt schliessen.
pause
