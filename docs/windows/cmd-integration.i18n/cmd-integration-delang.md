# Integration der Eingabeaufforderung (CMD) (Windows)

Um die Interaktion mit der STT-CLI (Speech-to-Text) über die Windows-Eingabeaufforderung zu vereinfachen, können Sie eine „s.bat“-Batchdatei erstellen und diese in Ihrem „PATH“ platzieren. Dadurch können Sie einfach „Ihre Frage“ in ein beliebiges CMD-Fenster eingeben.

> **Hinweis:** CMD (cmd.exe) ist die alte Windows-Shell und weist im Vergleich zu PowerShell- oder Unix-Shells erhebliche Einschränkungen auf. Für ein umfassenderes Erlebnis sollten Sie stattdessen die Verwendung von [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-delang.md) oder [WSL Integration](.././wsl-integration.i18n/wsl-integration-delang.md) in Betracht ziehen.

## Einrichtungsanweisungen

### 1. Erstellen Sie ein Verzeichnis für Ihre persönlichen Skripte (falls noch nicht geschehen)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. Fügen Sie dieses Verzeichnis zu Ihrem PATH hinzu (einmalige Einrichtung)

Öffnen Sie **Systemeigenschaften → Umgebungsvariablen** und fügen Sie „%USERPROFILE%\bin“ zu Ihrer Benutzervariablen „PATH“ hinzu.

Alternativ führen Sie dies in einer CMD-Eingabeaufforderung mit erhöhten Rechten aus (wird nach dem erneuten Öffnen von CMD wirksam):

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. Erstellen Sie die Batchdatei

Öffnen Sie Notepad oder einen beliebigen Texteditor und speichern Sie Folgendes als „%USERPROFILE%\bin\s.bat“:

```bat
@echo off
:: --- STT Project Path Resolution ---

setlocal EnableDelayedExpansion

:: Check for arguments
if "%~1"=="" (
    echo question ^<your question^>
    exit /b 1
)

:: Collect all arguments into one string
set "QUERY=%*"

:: Call helper functions (must be defined or available on PATH)
call update_github_ip.bat

set SHORT_TIMEOUT_SECONDS=2
set LONG_TIMEOUT_SECONDS=70

:: Path shortcuts (adjust PROJECT_ROOT to your actual path if not set as env var)
set "PY_EXEC=%PROJECT_ROOT%\.venv\Scripts\python.exe"
set "CLI_SCRIPT=%PROJECT_ROOT%\scripts\py\cli_client.py"

:: Create a temp file
set "TEMP_FILE=%TEMP%\stt_output_%RANDOM%.txt"
set "TEMP_FILE_ERR=%TEMP%\stt_err_%RANDOM%.txt"

:: --- 1. First try (short timeout via 'timeout' workaround) ---
:: CMD has no built-in process timeout. We use 'start /wait' with a watchdog approach.
:: For a true timeout, PowerShell is called inline as a helper:
powershell -NoProfile -Command ^
    "$proc = Start-Process -FilePath '%PY_EXEC%' ^
        -ArgumentList '-u','%CLI_SCRIPT%','%QUERY%','--lang','de-DE','--unmasked' ^
        -RedirectStandardOutput '%TEMP_FILE%' ^
        -RedirectStandardError '%TEMP_FILE_ERR%' ^
        -NoNewWindow -PassThru; ^
    $done = $proc.WaitForExit(%SHORT_TIMEOUT_SECONDS%000); ^
    if (-not $done) { $proc.Kill(); exit 124 } else { exit $proc.ExitCode }"

set EXIT_CODE=%ERRORLEVEL%

:: Read output
set "OUTPUT="
if exist "%TEMP_FILE%" (
    set /p OUTPUT=<"%TEMP_FILE%"
    del "%TEMP_FILE%" "%TEMP_FILE_ERR%" 2>nul
)

:: --- Service check ---
findstr /C:"Verbindungsfehler" "%TEMP_FILE%" >nul 2>&1
set CONN_ERR=%ERRORLEVEL%

tasklist /FI "IMAGENAME eq streamlit.exe" 2>nul | find /I "streamlit.exe" >nul
set STREAMLIT_RUNNING=%ERRORLEVEL%

if %CONN_ERR%==0 (goto :restart)
if %STREAMLIT_RUNNING% NEQ 0 (goto :restart)
goto :check_exit

:restart
echo Service-Check: Backend oder Frontend fehlt. Starte neu...
call start_service.bat
echo ++++++++++++++++++++++++++++++++++++++++++++++++++
set "KIWIX_SCRIPT=%PROJECT_ROOT%\config\maps\plugins\standard_actions\wikipedia_local\de-DE\kiwix-docker-start-if-not-running.sh"
if exist "%KIWIX_SCRIPT%" (
    bash "%KIWIX_SCRIPT%"
)
echo ++++++++++++++++++++++++++++++++++++++++++++++++++
echo BITTE ERNEUT EINGEBEN: s %QUERY%
exit /b 1

:check_exit
if %EXIT_CODE%==124 (goto :long_timeout)
if %EXIT_CODE%==0 (
    echo %OUTPUT%
    exit /b 0
)
goto :error

:long_timeout
echo answer ^> %SHORT_TIMEOUT_SECONDS% sec. set Timeout= %LONG_TIMEOUT_SECONDS% s...

set "TEMP_FILE_2=%TEMP%\stt_output2_%RANDOM%.txt"
set "TEMP_FILE_2_ERR=%TEMP%\stt_err2_%RANDOM%.txt"

powershell -NoProfile -Command ^
    "$proc = Start-Process -FilePath '%PY_EXEC%' ^
        -ArgumentList '-u','%CLI_SCRIPT%','%QUERY%','--lang','de-DE','--unmasked' ^
        -RedirectStandardOutput '%TEMP_FILE_2%' ^
        -RedirectStandardError '%TEMP_FILE_2_ERR%' ^
        -NoNewWindow -PassThru; ^
    $done = $proc.WaitForExit(%LONG_TIMEOUT_SECONDS%000); ^
    if (-not $done) { $proc.Kill(); exit 124 } else { exit $proc.ExitCode }"

set EXIT_CODE_2=%ERRORLEVEL%

if exist "%TEMP_FILE_2%" (
    type "%TEMP_FILE_2%"
    del "%TEMP_FILE_2%" "%TEMP_FILE_2_ERR%" 2>nul
)

if %EXIT_CODE_2% NEQ 0 (
    echo WARNUNG: Timeout ^> %LONG_TIMEOUT_SECONDS% Sec.
)
exit /b 0

:error
echo ERROR
echo %OUTPUT%
exit /b %EXIT_CODE%
```

### 4. Testen Sie es

Öffnen Sie ein neues CMD-Fenster (damit der aktualisierte PATH geladen wird) und geben Sie Folgendes ein:

```cmd
s your question here
```

## CMD-spezifische Hinweise

- **Kein nativer Prozess-Timeout**: CMD hat kein Äquivalent zum Unix-Timeout. Dieses Skript delegiert die Timeout-Logik inline an „WaitForExit“ von PowerShell. PowerShell muss verfügbar sein (auf allen modernen Windows-Systemen).
- **`PROJECT_ROOT`**: Legen Sie dies als permanente Benutzerumgebungsvariable über die Systemeigenschaften fest oder codieren Sie den Pfad in der „.bat“-Datei fest.
- **Hilfsskripte**: „update_github_ip.bat“ und „start_service.bat“ müssen in Ihrem „PATH“ oder in „%USERPROFILE%\bin“ vorhanden sein. Dies sind die CMD-Äquivalente der Shell-Funktionen „update_github_ip“ und „start_service“.
- **`bash` für das Kiwix-Skript**: Wenn WSL installiert ist, ist `bash` in CMD verfügbar und das `.sh`-Skript wird direkt ausgeführt. Andernfalls passen Sie „kiwix-docker-start-if-not-running.sh“ an ein „.bat“-Äquivalent an.
- **Zitathandhabung**: CMD hat strenge und fragile Zitatregeln. Wenn Ihre Abfrage Sonderzeichen enthält (`&`, `|`, `>`, `<`), schließen Sie die gesamte Abfrage in doppelte Anführungszeichen ein: `s „Ihre & Frage“`.
- **``set /p`-Einschränkung**: `set /p` liest nur die erste Zeile einer Datei. Für eine mehrzeilige Ausgabe verwenden Sie „type“, um die Datei direkt zu drucken (wie im Long-Timeout-Zweig).

## Merkmale

- **Dynamische Pfade**: Löst Pfade automatisch über die Umgebungsvariable „PROJECT_ROOT“ auf.
- **Auto-Neustart**: Wenn das Backend ausgefallen ist, ruft es „start_service.bat“ auf und versucht, lokale Wikipedia-Dienste zu starten.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.