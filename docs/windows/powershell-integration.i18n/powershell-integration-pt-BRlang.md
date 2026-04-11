#Integração com PowerShell (Windows)

Para facilitar a interação com a CLI STT (Speech-to-Text), você pode adicionar uma função de atalho ao seu perfil do PowerShell. Isso permite que você simplesmente digite `s "sua pergunta"` em qualquer janela do PowerShell.

> **Aplica-se a:** Windows PowerShell 5.1 e PowerShell 7+ (recomendado). O PowerShell 7 pode ser instalado a partir do [Microsoft Store](https://aka.ms/powershell) ou via `winget install Microsoft.PowerShell`.

## Instruções de configuração

### 1. Permitir execução de script (configuração única)

O PowerShell bloqueia scripts por padrão. Abra o PowerShell **como administrador** e execute:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Abra seu perfil do PowerShell

```powershell
notepad $PROFILE
```

Se o arquivo ainda não existir, crie-o primeiro:

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. Cole o seguinte bloco no final do arquivo

__CODE_BLOCO_3__

### 4. Recarregue seu perfil

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

## Notas específicas do Windows

- **Caminho Python**: No Windows, o binário do ambiente virtual está em `.venv\Scripts\python.exe` em vez de `.venv/bin/python3`. Ajuste `$PY_EXEC` se sua configuração for diferente.
- **Variável de ambiente `PROJECT_ROOT`**: Defina isso nas variáveis de ambiente do seu sistema ou adicione a seguinte linha acima da função em seu perfil:
__CODE_BLOCO_5__
- **`timeout` / `mktemp`**: Essas ferramentas Unix não estão disponíveis nativamente. O script acima usa equivalentes nativos do PowerShell (`WaitForExit` com tempo limite de milissegundos e `GetTempFileName()`).
- **`pgrep`**: Substituído por `Get-Process -Name "streamlit"`.
- **`start_service` / `update_github_ip`**: Devem ser definidas como funções do PowerShell (`Start-Service-STT`, `Update-GithubIp`) no mesmo arquivo de perfil, antes da função `s`.
- **Script WSL Kiwix**: Se `bash` estiver disponível (via WSL), o script auxiliar `.sh` será executado como está. Caso contrário, adapte-o para um equivalente `.ps1` ou `.bat`.
- **Várias versões do PowerShell**: `$PROFILE` aponta para arquivos diferentes para Windows PowerShell 5.1 e PowerShell 7. Para verificar qual arquivo de perfil está ativo, execute `$PROFILE` em cada versão.

## Características

- **Caminhos Dinâmicos**: Encontra automaticamente a raiz do projeto através da variável de ambiente `PROJECT_ROOT`.
- **Auto-Restart**: Se o backend estiver inativo, ele tenta executar o `Start-Service-STT` e os serviços locais da Wikipedia.
- **Tempos limite inteligentes**: primeiro tenta uma resposta rápida de 2 segundos e depois volta para um modo de processamento profundo de 70 segundos.