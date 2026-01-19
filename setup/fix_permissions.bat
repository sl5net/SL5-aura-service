@echo off
echo Setze Schreibrechte fuer den Projekt-Hauptordner (Updates ohne Admin)...

:: 1. Gehe in das Verzeichnis dieses Skripts (z.B. .../SL5-Aura/setup/)
pushd "%~dp0"

:: 2. Gehe eine Ebene nach oben zum Projekt-Root (z.B. .../SL5-Aura/)
cd ..

:: 3. Speichere diesen Pfad als Ziel
set "TARGET_DIR=%CD%"

:: 4. Gehe zurück (Aufräumen)
popd

echo Ziel-Ordner ist: "%TARGET_DIR%"

:: Entfernt Schreibschutz (Read-Only) rekursiv
attrib -r "%TARGET_DIR%\*.*" /s /d

:: Rechte vergeben (Rekursiv für alle Unterordner /T)
:: (OI)(CI)F = Object Inherit, Container Inherit, Full Control

:: Deutsch
icacls "%TARGET_DIR%" /grant:r "Benutzer":(OI)(CI)F /T
icacls "%TARGET_DIR%" /grant:r "Jeder":(OI)(CI)F /T

:: Englisch / International
icacls "%TARGET_DIR%" /grant:r "Users":(OI)(CI)F /T
icacls "%TARGET_DIR%" /grant:r "Everyone":(OI)(CI)F /T

echo.
echo ========================================================
echo BERECHTIGUNGEN GESETZT.
echo Der Ordner "%TARGET_DIR%" ist nun schreibbar fuer Nutzer.
echo ========================================================
pause
