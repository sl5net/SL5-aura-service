@echo off

:: setup/fix_permissions.bat



pushd "%~dp0"
cd ..
set "TARGET_DIR=%CD%"
popd

echo Ziel: "%TARGET_DIR%"

:: Wir setzen die Rechte NUR auf den Hauptordner.
:: (OI)(CI) sorgt dafuer, dass alle Unterordner/Dateien das automatisch erben.
:: Das dauert nur 1 Sekunde.

:: Deutsch
icacls "%TARGET_DIR%" /grant:r "Benutzer":(OI)(CI)F /grant:r "Jeder":(OI)(CI)F

:: Englisch / International
icacls "%TARGET_DIR%" /grant:r "Users":(OI)(CI)F /grant:r "Everyone":(OI)(CI)F



set "TARGET_DIR=C:\tmp\sl5_aura"

:: 1. Verzeichnis erstellen (falls nicht vorhanden)
if not exist "%TARGET_DIR%" mkdir "%TARGET_DIR%"

:: 2. Rechte setzen
:: /grant      = Rechte gewähren
:: *S-1-5-32-545 = SID für die Gruppe "Benutzer" (lokal) - sicherer als "Jeder"
:: (OI)        = Object Inherit (Dateien erben Rechte)
:: (CI)        = Container Inherit (Unterordner erben Rechte)
:: F           = Full Control (Vollzugriff - Lesen, Schreiben, Löschen)
:: /t          = Rekursiv auf bereits existierende Unterelemente anwenden

icacls "%TARGET_DIR%" /grant *S-1-5-32-545:(OI)(CI)F /t

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ACHTUNG: Keine Admin-Rechte!
    echo Bitte prüfen ob das Script in C:\tmp\sl5_aura schreiben kann.
    echo Eventuell noch mal starten so: Rechtsklick auf die Datei -> "Als Administrator ausfuehren"
    timeout /t 4
)

echo Rechte für %TARGET_DIR% verarbeitet.




echo.
echo ========================================================
echo Fertig! Rechte wurden (hoffentlich) per Vererbung gesetzt.
echo ========================================================
