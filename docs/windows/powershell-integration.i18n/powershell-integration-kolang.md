# 파워셸 통합(윈도우)

STT(Speech-to-Text) CLI와 더 쉽게 상호 작용하려면 PowerShell 프로필에 바로 가기 기능을 추가하면 됩니다. 이를 통해 PowerShell 창에 `"your 질문"`을 입력하기만 하면 됩니다.

> **적용 대상:** Windows PowerShell 5.1 및 PowerShell 7+(권장). PowerShell 7은 [Microsoft Store](https://aka.ms/powershell) 또는 `winget install Microsoft.PowerShell`을 통해 설치할 수 있습니다.

## 설정 지침

### 1. 스크립트 실행 허용(일회성 설정)

PowerShell은 기본적으로 스크립트를 차단합니다. PowerShell **관리자**를 열고 다음을 실행합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. PowerShell 프로필을 엽니다.

```powershell
notepad $PROFILE
```

파일이 아직 존재하지 않으면 먼저 생성하십시오.

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. 파일 끝에 다음 블록을 붙여넣습니다.

```powershell
# --- STT Project Path Resolution ---
function s {
    param(
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Query
    )

    if ($Query.Count -eq 0) {
        Write-Host "question <your question>"
        return
    }

    $QueryString = $Query -join " "

    Update-GithubIp   # equivalent of update_github_ip

    $SHORT_TIMEOUT_SECONDS = 2
    $LONG_TIMEOUT_SECONDS  = 70

    # Path shortcuts
    $PY_EXEC   = "$env:PROJECT_ROOT\.venv\Scripts\python.exe"
    $CLI_SCRIPT = "$env:PROJECT_ROOT\scripts\py\cli_client.py"

    $TempFile = [System.IO.Path]::GetTempFileName()

    # --- 1. First try (short timeout) ---
    $proc = Start-Process -FilePath $PY_EXEC `
        -ArgumentList "-u", "`"$CLI_SCRIPT`"", "`"$QueryString`"", "--lang", "de-DE", "--unmasked" `
        -RedirectStandardOutput $TempFile `
        -RedirectStandardError  "$TempFile.err" `
        -NoNewWindow -PassThru

    $finished = $proc.WaitForExit($SHORT_TIMEOUT_SECONDS * 1000)
    $Output   = Get-Content $TempFile -Raw -ErrorAction SilentlyContinue

    if (-not $finished) {
        # Still running — this is the timeout case
        $ExitCode = 124
    } else {
        $ExitCode = $proc.ExitCode
    }

    Remove-Item $TempFile, "$TempFile.err" -ErrorAction SilentlyContinue

    # --- Service check ---
    $streamlitRunning = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
    if (($Output -match "Verbindungsfehler") -or (-not $streamlitRunning)) {
        Write-Host "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        Start-Service-STT   # equivalent of start_service
        Write-Host "++++++++++++++++++++++++++++++++++++++++++++++++++"

        $KiwixScript = "$env:PROJECT_ROOT\config\maps\plugins\standard_actions\wikipedia_local\de-DE\kiwix-docker-start-if-not-running.sh"
        if (Test-Path $KiwixScript) {
            bash $KiwixScript
        }

        Write-Host "++++++++++++++++++++++++++++++++++++++++++++++++++"
        Write-Host "BITTE ERNEUT EINGEBEN: s $QueryString"
        return
    }

    # --- 2. Timeout OR immediate success ---
    if ($ExitCode -eq 124 -or $ExitCode -eq 0) {
        if ($ExitCode -eq 0) {
            Write-Host $Output
            return
        }

        Write-Host "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."

        $TempFile2 = [System.IO.Path]::GetTempFileName()
        $proc2 = Start-Process -FilePath $PY_EXEC `
            -ArgumentList "-u", "`"$CLI_SCRIPT`"", "`"$QueryString`"", "--lang", "de-DE", "--unmasked" `
            -RedirectStandardOutput $TempFile2 `
            -RedirectStandardError  "$TempFile2.err" `
            -NoNewWindow -PassThru

        $finished2 = $proc2.WaitForExit($LONG_TIMEOUT_SECONDS * 1000)
        $Output2   = Get-Content $TempFile2 -Raw -ErrorAction SilentlyContinue
        $ExitCode2 = if ($finished2) { $proc2.ExitCode } else { 124 }

        Remove-Item $TempFile2, "$TempFile2.err" -ErrorAction SilentlyContinue

        Write-Host $Output2

        if ($ExitCode2 -ne 0) {
            Write-Host "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec."
        }
        return
    }

    # --- Unexpected error ---
    Write-Host "ERROR"
    Write-Host $Output
}
```

### 4. 프로필을 새로고침하세요.

```powershell
. $PROFILE
```

## Windows 관련 참고사항

- **Python 경로**: Windows에서 가상 환경 바이너리는 `.venv/bin/python3` 대신 `.venv\Scripts\python.exe`에 있습니다. 설정이 다른 경우 `$PY_EXEC`를 조정하세요.
- **`PROJECT_ROOT` 환경 변수**: 시스템 환경 변수에서 이를 설정하거나 프로필의 함수 위에 다음 줄을 추가합니다.
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: 이러한 Unix 도구는 기본적으로 사용할 수 없습니다. 위의 스크립트는 PowerShell 기본 항목(밀리초 시간 제한이 있는 'WaitForExit' 및 'GetTempFileName()')을 사용합니다.
- **`pgrep`**: `Get-Process -Name "streamlit"`로 대체되었습니다.
- **`start_service` / `update_github_ip`**: 이는 동일한 프로필 파일에서 `s` 함수 앞에 PowerShell 함수(`Start-Service-STT`, `Update-GithubIp`)로 정의되어야 합니다.
- **WSL Kiwix 스크립트**: `bash`를 사용할 수 있는 경우(WSL을 통해) `.sh` 도우미 스크립트는 그대로 실행됩니다. 그렇지 않으면 `.ps1` 또는 `.bat`에 해당하는 파일로 조정하세요.
- **여러 PowerShell 버전**: `$PROFILE`은 Windows PowerShell 5.1 및 PowerShell 7에 대한 서로 다른 파일을 가리킵니다. 어떤 프로필 파일이 활성화되어 있는지 확인하려면 각 버전에서 `$PROFILE`을 실행하세요.

## 특징

- **동적 경로**: `PROJECT_ROOT` 환경 변수를 통해 프로젝트 루트를 자동으로 찾습니다.
- **자동 재시작**: 백엔드가 다운되면 'Start-Service-STT' 및 로컬 Wikipedia 서비스 실행을 시도합니다.
- **스마트 타임아웃**: 먼저 빠른 2초 응답을 시도한 다음 70초 심층 처리 모드로 돌아갑니다.