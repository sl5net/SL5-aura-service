# PowerShell-Integration (Windows)

Um die Interaktion mit der STT-CLI (Speech-to-Text) zu vereinfachen, können Sie Ihrem PowerShell-Profil eine Verknüpfungsfunktion hinzufügen. Dadurch können Sie einfach „Ihre Frage“ in ein beliebiges PowerShell-Fenster eingeben.

> **Gilt für:** Windows PowerShell 5.1 und PowerShell 7+ (empfohlen). PowerShell 7 kann über [Microsoft Store](https://aka.ms/powershell) oder über „winget install Microsoft.PowerShell“ installiert werden.

## Einrichtungsanweisungen

### 1. Skriptausführung zulassen (einmalige Einrichtung)

PowerShell blockiert standardmäßig Skripte. Öffnen Sie PowerShell **als Administrator** und führen Sie Folgendes aus:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Öffnen Sie Ihr PowerShell-Profil

```powershell
notepad $PROFILE
```

Wenn die Datei noch nicht existiert, erstellen Sie sie zuerst:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. Fügen Sie den folgenden Block am Ende der Datei ein

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

### 4. Laden Sie Ihr Profil neu

```powershell
. $PROFILE
```

## Windows-spezifische Hinweise

- **Python-Pfad**: Unter Windows befindet sich die Binärdatei der virtuellen Umgebung unter „.venv\Scripts\python.exe“ statt unter „.venv/bin/python3“. Passen Sie „$PY_EXEC“ an, wenn Ihr Setup davon abweicht.
- **Umgebungsvariable „PROJECT_ROOT“**: Legen Sie dies in Ihren Systemumgebungsvariablen fest oder fügen Sie die folgende Zeile über der Funktion in Ihrem Profil hinzu:
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: Diese Unix-Tools sind nicht nativ verfügbar. Das obige Skript verwendet PowerShell-native Äquivalente („WaitForExit“ mit einem Millisekunden-Timeout und „GetTempFileName()“).
- **`pgrep`**: Ersetzt durch `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`**: Diese müssen als PowerShell-Funktionen („Start-Service-STT“, „Update-GithubIp“) in derselben Profildatei vor der Funktion „s“ definiert werden.
- **WSL-Kiwix-Skript**: Wenn „bash“ verfügbar ist (über WSL), wird das „.sh“-Hilfsskript unverändert ausgeführt. Andernfalls passen Sie es an ein „.ps1“- oder „.bat“-Äquivalent an.
- **Mehrere PowerShell-Versionen**: „$PROFILE“ verweist auf unterschiedliche Dateien für Windows PowerShell 5.1 und PowerShell 7. Um zu überprüfen, welche Profildatei aktiv ist, führen Sie „$PROFILE“ in jeder Version aus.

## Merkmale

- **Dynamische Pfade**: Findet automatisch das Projektstammverzeichnis über die Umgebungsvariable „PROJECT_ROOT“.
- **Automatischer Neustart**: Wenn das Backend ausgefallen ist, versucht es, „Start-Service-STT“ und lokale Wikipedia-Dienste auszuführen.
- **Intelligente Zeitüberschreitungen**: Versucht zunächst eine schnelle 2-Sekunden-Reaktion und fällt dann auf einen 70-Sekunden-Tiefverarbeitungsmodus zurück.