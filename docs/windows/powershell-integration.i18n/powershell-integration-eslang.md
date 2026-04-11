# Integración de PowerShell (Windows)

Para facilitar la interacción con la CLI STT (Voz a Texto), puede agregar una función de acceso directo a su perfil de PowerShell. Esto le permite simplemente escribir "su pregunta" en cualquier ventana de PowerShell.

> **Se aplica a:** Windows PowerShell 5.1 y PowerShell 7+ (recomendado). PowerShell 7 se puede instalar desde [Microsoft Store](https://aka.ms/powershell) o mediante `winget install Microsoft.PowerShell`.

## Instrucciones de configuración

### 1. Permitir la ejecución del script (configuración única)

PowerShell bloquea los scripts de forma predeterminada. Abra PowerShell **como administrador** y ejecute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Abra su perfil de PowerShell

```powershell
notepad $PROFILE
```

Si el archivo aún no existe, créelo primero:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. Pega el siguiente bloque al final del archivo.

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

### 4. Recarga tu perfil

```powershell
. $PROFILE
```

## Notas específicas de Windows

- **Ruta de Python**: en Windows, el binario del entorno virtual está en `.venv\Scripts\python.exe` en lugar de `.venv/bin/python3`. Ajuste `$PY_EXEC` si su configuración es diferente.
- **Variable de entorno `PROJECT_ROOT`**: establezca esto en las variables de entorno de su sistema o agregue la siguiente línea encima de la función en su perfil:
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: Estas herramientas de Unix no están disponibles de forma nativa. El script anterior utiliza equivalentes nativos de PowerShell (`WaitForExit` con un tiempo de espera de milisegundos y `GetTempFileName()`).
- **`pgrep`**: Reemplazado con `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`**: Deben definirse como funciones de PowerShell (`Start-Service-STT`, `Update-GithubIp`) en el mismo archivo de perfil, antes de la función `s`.
- **Script WSL Kiwix**: si `bash` está disponible (a través de WSL), el script auxiliar `.sh` se ejecutará tal cual. De lo contrario, adáptelo a un equivalente `.ps1` o `.bat`.
- **Múltiples versiones de PowerShell**: `$PROFILE` apunta a diferentes archivos para Windows PowerShell 5.1 y PowerShell 7. Para verificar qué archivo de perfil está activo, ejecute `$PROFILE` en cada versión.

## Características

- **Rutas dinámicas**: encuentra automáticamente la raíz del proyecto a través de la variable de entorno `PROJECT_ROOT`.
- **Reinicio automático**: si el backend no funciona, intenta ejecutar `Start-Service-STT` y los servicios locales de Wikipedia.
- **Tiempos de espera inteligentes**: primero intenta una respuesta rápida de 2 segundos y luego vuelve a un modo de procesamiento profundo de 70 segundos.