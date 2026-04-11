# 명령 프롬프트(CMD) 통합(Windows)

Windows 명령 프롬프트에서 STT(Speech-to-Text) CLI와 더 쉽게 상호 작용하려면 `s.bat` 배치 파일을 만들어 `PATH`에 배치할 수 있습니다. 이를 통해 CMD 창에 '질문''을 간단히 입력할 수 있습니다.

> **참고:** CMD(cmd.exe)는 레거시 Windows 셸이며 PowerShell 또는 Unix 셸에 비해 상당한 제한이 있습니다. 보다 풍부한 경험을 위해서는 [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-kolang.md) 또는 [WSL Integration](.././wsl-integration.i18n/wsl-integration-kolang.md)를 대신 사용하는 것이 좋습니다.

## 설정 지침

### 1. 개인 스크립트용 디렉터리를 만듭니다(아직 수행하지 않은 경우).

```cmd
mkdir %USERPROFILE%\bin
```

### 2. 해당 디렉터리를 PATH에 추가합니다(일회성 설정).

**시스템 속성 → 환경 변수**를 열고 사용자 `PATH` 변수에 `%USERPROFILE%\bin`을 추가합니다.

또는 관리자 권한 CMD 프롬프트에서 이를 실행합니다(CMD를 다시 연 후에 적용됨).

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. 배치 파일 생성

메모장이나 텍스트 편집기를 열고 다음을 `%USERPROFILE%\bin\s.bat`로 저장합니다.

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

### 4. 테스트해 보세요

새 CMD 창을 열고(업데이트된 PATH가 로드됨) 다음을 입력합니다.

```cmd
s your question here
```

## CMD 관련 참고 사항

- **기본 프로세스 시간 초과 없음**: CMD에는 Unix `timeout`에 해당하는 기능이 없습니다. 이 스크립트는 시간 초과 논리를 PowerShell의 `WaitForExit`에 인라인으로 위임합니다. PowerShell을 사용할 수 있어야 합니다(모든 최신 Windows 시스템에 있음).
- **`PROJECT_ROOT`**: 시스템 속성을 통해 이를 영구 사용자 환경 변수로 설정하거나 `.bat` 파일에 경로를 하드코딩합니다.
- **도우미 스크립트**: `update_github_ip.bat` 및 `start_service.bat`는 `PATH` 또는 `%USERPROFILE%\bin`에 있어야 합니다. 이는 `update_github_ip` 및 `start_service` 셸 함수에 해당하는 CMD입니다.
- **Kiwix 스크립트용 `bash`**: WSL이 설치된 경우 CMD에서 `bash`를 사용할 수 있으며 `.sh` 스크립트가 직접 실행됩니다. 그렇지 않으면 `kiwix-docker-start-if-not-running.sh`를 `.bat`에 상응하는 것으로 조정하세요.
- **견적 처리**: CMD에는 엄격하고 깨지기 쉬운 인용 규칙이 있습니다. 쿼리에 특수 문자(`&`, `|`, `>`, `<`)가 포함된 경우 전체 쿼리를 큰따옴표(`s "your &question"`)로 묶습니다.
- **`set /p` 제한**: `set /p`는 파일의 첫 번째 줄만 읽습니다. 여러 줄로 출력하려면 'type'을 사용하여 파일을 직접 인쇄하세요(장시간 제한 분기에서 수행된 것처럼).

## 특징

- **동적 경로**: `PROJECT_ROOT` 환경 변수를 통해 경로를 자동으로 확인합니다.
- **자동 재시작**: 백엔드가 다운되면 `start_service.bat`을 호출하고 로컬 Wikipedia 서비스 시작을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.