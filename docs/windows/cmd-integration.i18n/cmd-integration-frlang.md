# Intégration de l'invite de commande (CMD) (Windows)

Pour faciliter l'interaction avec la CLI STT (Speech-to-Text) à partir de l'invite de commande Windows, vous pouvez créer un fichier batch « s.bat » et le placer sur votre « PATH ». Cela vous permet de taper simplement « votre question » dans n'importe quelle fenêtre CMD.

> **Remarque :** CMD (cmd.exe) est l'ancien shell Windows et présente des limitations importantes par rapport aux shells PowerShell ou Unix. Pour une expérience plus riche, envisagez plutôt d'utiliser le [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-frlang.md) ou le [WSL Integration](.././wsl-integration.i18n/wsl-integration-frlang.md).

## Instructions de configuration

### 1. Créez un répertoire pour vos scripts personnels (si ce n'est pas déjà fait)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. Ajoutez ce répertoire à votre PATH (configuration unique)

Ouvrez **Propriétés système → Variables d'environnement** et ajoutez `%USERPROFILE%\bin` à la variable `PATH` de votre utilisateur.

Vous pouvez également l'exécuter dans une invite CMD élevée (prend effet après la réouverture de CMD) :

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. Créez le fichier batch

Ouvrez le Bloc-notes ou n'importe quel éditeur de texte et enregistrez ce qui suit sous `%USERPROFILE%\bin\s.bat` :

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

### 4. Testez-le

Ouvrez une nouvelle fenêtre CMD (pour que le PATH mis à jour soit chargé) et tapez :

```cmd
s your question here
```

## Notes spécifiques à CMD

- **Pas de timeout de processus natif** : CMD n'a pas d'équivalent au `timeout` Unix. Ce script délègue la logique de délai d'attente en ligne à « WaitForExit » de PowerShell. PowerShell doit être disponible (c'est sur tous les systèmes Windows modernes).
- **`PROJECT_ROOT`** : définissez-la comme variable d'environnement utilisateur permanente via les propriétés système, ou codez en dur le chemin dans le fichier `.bat`.
- **Scripts d'aide** : `update_github_ip.bat` et `start_service.bat` doivent exister sur votre `PATH` ou dans `%USERPROFILE%\bin`. Ce sont les équivalents CMD des fonctions shell `update_github_ip` et `start_service`.
- **`bash` pour le script Kiwix** : Si WSL est installé, `bash` est disponible dans CMD et le script `.sh` s'exécutera directement. Sinon, adaptez `kiwix-docker-start-if-not-running.sh` en un équivalent `.bat`.
- **Gestion des devis** : CMD a des règles de cotation strictes et fragiles. Si votre requête contient des caractères spéciaux (`&`, `|`, `>`, `<`), placez l'intégralité de la requête entre guillemets doubles : `s "votre & question"`.
- **Limitation `set /p`** : `set /p` ne lit que la première ligne d'un fichier. Pour une sortie multiligne, utilisez `type` pour imprimer le fichier directement (comme dans la branche long-timeout).

## Caractéristiques

- **Chemins dynamiques** : résout automatiquement les chemins via la variable d'environnement `PROJECT_ROOT`.
- **Auto-Restart** : si le backend est en panne, appelle `start_service.bat` et tente de démarrer les services Wikipédia locaux.
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.