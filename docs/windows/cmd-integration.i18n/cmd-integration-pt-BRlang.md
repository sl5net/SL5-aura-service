# Integração com prompt de comando (CMD) (Windows)

Para facilitar a interação com a CLI STT (Speech-to-Text) a partir do prompt de comando do Windows, você pode criar um arquivo em lote `s.bat` e colocá-lo em seu `PATH`. Isso permite que você simplesmente digite `s "sua pergunta"` em qualquer janela do CMD.

> **Observação:** CMD (cmd.exe) é o shell herdado do Windows e tem limitações significativas em comparação aos shells PowerShell ou Unix. Para uma experiência mais rica, considere usar o [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-pt-BRlang.md) ou o [WSL Integration](.././wsl-integration.i18n/wsl-integration-pt-BRlang.md).

## Instruções de configuração

### 1. Crie um diretório para seus scripts pessoais (se ainda não tiver feito isso)

```cmd
mkdir %USERPROFILE%\bin
```

### 2. Adicione esse diretório ao seu PATH (configuração única)

Abra **Propriedades do Sistema → Variáveis de Ambiente** e adicione `%USERPROFILE%\bin` à variável `PATH` do seu usuário.

Como alternativa, execute isso em um prompt CMD elevado (entra em vigor após reabrir o CMD):

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. Crie o arquivo em lote

Abra o Bloco de Notas ou qualquer editor de texto e salve o seguinte como `%USERPROFILE%\bin\s.bat`:

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

### 4. Teste

Abra uma nova janela CMD (para que o PATH atualizado seja carregado) e digite:

__CODE_BLOCO_3__

## Notas específicas do CMD

- **Sem tempo limite de processo nativo**: CMD não tem equivalente ao `timeout` do Unix. Este script delega a lógica de tempo limite embutida no `WaitForExit` do PowerShell. O PowerShell deve estar disponível (está em todos os sistemas Windows modernos).
- **`PROJECT_ROOT`**: Defina isso como uma variável de ambiente de usuário permanente através das Propriedades do Sistema ou codifique o caminho no arquivo `.bat`.
- **Scripts auxiliares**: `update_github_ip.bat` e `start_service.bat` devem existir em seu `PATH` ou em `%USERPROFILE%\bin`. Estes são os equivalentes CMD das funções shell `update_github_ip` e `start_service`.
- **`bash` para o script Kiwix**: Se o WSL estiver instalado, `bash` estará disponível no CMD e o script `.sh` será executado diretamente. Caso contrário, adapte `kiwix-docker-start-if-not-running.sh` para um equivalente `.bat`.
- **Tratamento de cotações**: o CMD tem regras de cotação rígidas e frágeis. Se sua consulta contiver caracteres especiais (`&`, `|`, `>`, `<`), coloque toda a consulta entre aspas duplas: `s "sua & pergunta"`.
- **limitação `set /p`**: `set /p` só lê a primeira linha de um arquivo. Para saída multilinha, use `type` para imprimir o arquivo diretamente (como feito na ramificação de longo tempo limite).

## Características

- **Caminhos Dinâmicos**: Resolve caminhos automaticamente através da variável de ambiente `PROJECT_ROOT`.
- **Reinicialização automática**: Se o backend estiver inativo, chama `start_service.bat` e tenta iniciar os serviços locais da Wikipédia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.