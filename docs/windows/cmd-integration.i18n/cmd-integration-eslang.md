# Integración del símbolo del sistema (CMD) (Windows)

Para facilitar la interacción con la CLI STT (Voz a Texto) desde el símbolo del sistema de Windows, puede crear un archivo por lotes `s.bat` y colocarlo en su `PATH`. Esto le permite simplemente escribir "su pregunta" en cualquier ventana de CMD.

> **Nota:** CMD (cmd.exe) es el shell heredado de Windows y tiene limitaciones significativas en comparación con los shells de PowerShell o Unix. Para una experiencia más rica, considere usar [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-eslang.md) o [WSL Integration](.././wsl-integration.i18n/wsl-integration-eslang.md) en su lugar.

## Instrucciones de configuración

### 1. Cree un directorio para sus scripts personales (si aún no lo ha hecho)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. Agregue ese directorio a su RUTA (configuración única)

Abra **Propiedades del sistema → Variables de entorno** y agregue `%USERPROFILE%\bin` a su variable `PATH` de usuario.

Alternativamente, ejecute esto en un mensaje de CMD elevado (entra en vigor después de volver a abrir CMD):

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. Cree el archivo por lotes

Abra el Bloc de notas o cualquier editor de texto y guarde lo siguiente como `%USERPROFILE%\bin\s.bat`:

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

### 4. Pruébalo

Abra una nueva ventana de CMD (para que se cargue la RUTA actualizada) y escriba:

```cmd
s your question here
```

## Notas específicas de CMD

- **Sin tiempo de espera de proceso nativo**: CMD no tiene equivalente al "tiempo de espera" de Unix. Este script delega la lógica de tiempo de espera en línea a `WaitForExit` de PowerShell. PowerShell debe estar disponible (está en todos los sistemas Windows modernos).
- **`PROJECT_ROOT`**: configúrelo como una variable de entorno de usuario permanente a través de Propiedades del sistema, o codifique la ruta en el archivo `.bat`.
- **Scripts de ayuda**: `update_github_ip.bat` y `start_service.bat` deben existir en su `PATH` o en `%USERPROFILE%\bin`. Estos son los equivalentes CMD de las funciones de shell `update_github_ip` y `start_service`.
- **`bash` para el script Kiwix**: si WSL está instalado, `bash` está disponible en CMD y el script `.sh` se ejecutará directamente. De lo contrario, adapte `kiwix-docker-start-if-not-running.sh` a un equivalente `.bat`.
- **Manejo de cotizaciones**: CMD tiene reglas de cotización estrictas y frágiles. Si su consulta contiene caracteres especiales (`&`, `|`, `>`, `<`), incluya toda la consulta entre comillas dobles: `s "su & pregunta"`.
- **Limitación de `set /p`**: `set /p` solo lee la primera línea de un archivo. Para salida de varias líneas, use `type` para imprimir el archivo directamente (como se hace en la rama de tiempo de espera prolongado).

## Características

- **Rutas dinámicas**: Resuelve rutas automáticamente a través de la variable de entorno `PROJECT_ROOT`.
- **Reinicio automático**: si el backend no funciona, llama a `start_service.bat` e intenta iniciar los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.