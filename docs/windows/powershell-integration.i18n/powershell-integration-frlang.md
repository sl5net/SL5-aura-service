# Intégration PowerShell (Windows)

Pour faciliter l'interaction avec la CLI STT (Speech-to-Text), vous pouvez ajouter une fonction de raccourci à votre profil PowerShell. Cela vous permet de taper simplement « votre question » dans n'importe quelle fenêtre PowerShell.

> **S'applique à :** Windows PowerShell 5.1 et PowerShell 7+ (recommandé). PowerShell 7 peut être installé à partir du [Microsoft Store](https://aka.ms/powershell) ou via `winget install Microsoft.PowerShell`.

## Instructions de configuration

### 1. Autoriser l'exécution du script (configuration unique)

PowerShell bloque les scripts par défaut. Ouvrez PowerShell **en tant qu'administrateur** et exécutez :

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Ouvrez votre profil PowerShell

```powershell
notepad $PROFILE
```

Si le fichier n'existe pas encore, créez-le d'abord :

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. Collez le bloc suivant à la fin du fichier

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

### 4. Rechargez votre profil

```powershell
. $PROFILE
```

## Notes spécifiques à Windows

- **Chemin Python** : sous Windows, le binaire de l'environnement virtuel se trouve dans `.venv\Scripts\python.exe` au lieu de `.venv/bin/python3`. Ajustez `$PY_EXEC` si votre configuration diffère.
- **Variable d'environnement `PROJECT_ROOT`** : définissez-la dans les variables d'environnement de votre système ou ajoutez la ligne suivante au-dessus de la fonction dans votre profil :
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`** : Ces outils Unix ne sont pas disponibles nativement. Le script ci-dessus utilise des équivalents natifs PowerShell (`WaitForExit` avec un délai d'attente d'une milliseconde et `GetTempFileName()`).
- **`pgrep`** : remplacé par `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`** : Celles-ci doivent être définies comme fonctions PowerShell (`Start-Service-STT`, `Update-GithubIp`) dans le même fichier de profil, avant la fonction `s`.
- **Script WSL Kiwix** : Si `bash` est disponible (via WSL), le script d'assistance `.sh` s'exécutera tel quel. Sinon, adaptez-le à un équivalent `.ps1` ou `.bat`.
- **Plusieurs versions de PowerShell** : `$PROFILE` pointe vers différents fichiers pour Windows PowerShell 5.1 et PowerShell 7. Pour vérifier quel fichier de profil est actif, exécutez `$PROFILE` dans chaque version.

## Caractéristiques

- **Chemins dynamiques** : trouve automatiquement la racine du projet via la variable d'environnement `PROJECT_ROOT`.
- **Auto-Restart** : si le backend est en panne, il tente d'exécuter `Start-Service-STT` et les services Wikipédia locaux.
- **Smart Timeouts** : essaie d'abord une réponse rapide de 2 secondes, puis revient à un mode de traitement approfondi de 70 secondes.