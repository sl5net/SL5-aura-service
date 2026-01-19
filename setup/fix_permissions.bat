@echo off

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

echo.
echo ========================================================
echo Fertig! Rechte wurden per Vererbung gesetzt.
echo ========================================================
