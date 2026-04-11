# PowerShell Integration (Windows)

To make interacting with the STT (Speech-to-Text) CLI easier, you can add a shortcut function to your PowerShell profile. This allows you to simply type `s "your question"` in any PowerShell window.

> **Applies to:** Windows PowerShell 5.1 and PowerShell 7+ (recommended). PowerShell 7 can be installed from the [Microsoft Store](https://aka.ms/powershell) or via `winget install Microsoft.PowerShell`.

## Setup Instructions

### 1. Allow script execution (one-time setup)

PowerShell blocks scripts by default. Open PowerShell **as Administrator** and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Open your PowerShell profile

```powershell
notepad $PROFILE
```

If the file does not exist yet, create it first:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. Paste the following block at the end of the file

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

### 4. Reload your profile

```powershell
. $PROFILE
```

## Windows-Specific Notes

- **Python path**: On Windows, the virtual environment binary is at `.venv\Scripts\python.exe` instead of `.venv/bin/python3`. Adjust `$PY_EXEC` if your setup differs.
- **`PROJECT_ROOT` environment variable**: Set this in your system environment variables, or add the following line above the function in your profile:
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: These Unix tools are not available natively. The script above uses PowerShell-native equivalents (`WaitForExit` with a millisecond timeout and `GetTempFileName()`).
- **`pgrep`**: Replaced with `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`**: These must be defined as PowerShell functions (`Start-Service-STT`, `Update-GithubIp`) in the same profile file, before the `s` function.
- **WSL Kiwix script**: If `bash` is available (via WSL), the `.sh` helper script will run as-is. Otherwise, adapt it to a `.ps1` or `.bat` equivalent.
- **Multiple PowerShell versions**: `$PROFILE` points to different files for Windows PowerShell 5.1 and PowerShell 7. To check which profile file is active, run `$PROFILE` in each version.

## Features

- **Dynamic Paths**: Automatically finds the project root via the `PROJECT_ROOT` environment variable.
- **Auto-Restart**: If the backend is down, it attempts to run `Start-Service-STT` and local Wikipedia services.
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.
