# Command Prompt (CMD) Integration (Windows)

To make interacting with the STT (Speech-to-Text) CLI easier from the Windows Command Prompt, you can create a `s.bat` batch file and place it on your `PATH`. This allows you to simply type `s "your question"` in any CMD window.

> **Note:** CMD (cmd.exe) is the legacy Windows shell and has significant limitations compared to PowerShell or Unix shells. For a richer experience, consider using the [PowerShell Integration](./powershell-integration.md) or [WSL Integration](./wsl-integration.md) instead.

## Setup Instructions

### 1. Create a directory for your personal scripts (if not already done)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. Add that directory to your PATH (one-time setup)

Open **System Properties → Environment Variables** and add `%USERPROFILE%\bin` to your user `PATH` variable.

Alternatively, run this in an elevated CMD prompt (takes effect after re-opening CMD):

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. Create the batch file

Open Notepad or any text editor and save the following as `%USERPROFILE%\bin\s.bat`:

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

### 4. Test it

Open a new CMD window (so the updated PATH is loaded) and type:

```cmd
s your question here
```

## CMD-Specific Notes

- **No native process timeout**: CMD has no equivalent of Unix `timeout`. This script delegates the timeout logic inline to PowerShell's `WaitForExit`. PowerShell must be available (it is on all modern Windows systems).
- **`PROJECT_ROOT`**: Set this as a permanent user environment variable via System Properties, or hardcode the path in the `.bat` file.
- **Helper scripts**: `update_github_ip.bat` and `start_service.bat` must exist on your `PATH` or in `%USERPROFILE%\bin`. These are the CMD equivalents of the `update_github_ip` and `start_service` shell functions.
- **`bash` for the Kiwix script**: If WSL is installed, `bash` is available in CMD and the `.sh` script will run directly. Otherwise, adapt `kiwix-docker-start-if-not-running.sh` to a `.bat` equivalent.
- **Quote handling**: CMD has strict and fragile quoting rules. If your query contains special characters (`&`, `|`, `>`, `<`), wrap the whole query in double quotes: `s "your & question"`.
- **`set /p` limitation**: `set /p` only reads the first line of a file. For multi-line output, use `type` to print the file directly (as done in the long-timeout branch).

## Features

- **Dynamic Paths**: Automatically resolves paths via the `PROJECT_ROOT` environment variable.
- **Auto-Restart**: If the backend is down, calls `start_service.bat` and attempts to start local Wikipedia services.
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.
