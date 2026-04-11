# PowerShell の統合 (Windows)

STT (Speech-to-Text) CLI との対話を容易にするために、PowerShell プロファイルにショートカット関数を追加できます。これにより、任意の PowerShell ウィンドウに「質問」と入力するだけで済みます。

> **適用対象:** Windows PowerShell 5.1 および PowerShell 7 以降 (推奨)。 PowerShell 7 は、[Microsoft Store](https://aka.ms/powershell) から、または「winget install Microsoft.PowerShell」経由でインストールできます。

## セットアップ手順

### 1. スクリプトの実行を許可します (1 回限りのセットアップ)

PowerShell はデフォルトでスクリプトをブロックします。 **管理者として** PowerShell を開き、以下を実行します。

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. PowerShell プロファイルを開きます

```powershell
notepad $PROFILE
```

ファイルがまだ存在しない場合は、まずファイルを作成します。

```powershell
New-Item -ItemType File -Path $PROFILE -Force
notepad $PROFILE
```

### 3. ファイルの最後に次のブロックを貼り付けます。

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

### 4. プロフィールをリロードします

```powershell
. $PROFILE
```

## Windows 固有の注意事項

- **Python パス**: Windows では、仮想環境バイナリは `.venv/bin/python3` ではなく `.venv\Scripts\python.exe` にあります。設定が異なる場合は、`$PY_EXEC` を調整してください。
- **`PROJECT_ROOT` 環境変数**: これをシステム環境変数に設定するか、プロファイル内の関数の上に次の行を追加します。
  ```powershell
  $env:PROJECT_ROOT = "C:\path\to\your\project"
  ```
- **`timeout` / `mktemp`**: これらの Unix ツールはネイティブでは使用できません。上記のスクリプトは、PowerShell ネイティブの同等のもの (ミリ秒のタイムアウトを備えた `WaitForExit` と `GetTempFileName()`) を使用しています。
- **`pgrep`**: `Get-Process -Name "streamlit"` に置き換えられました。
- **`start_service` / `update_github_ip`**: これらは、同じプロファイル ファイル内の `s` 関数の前に PowerShell 関数 (`Start-Service-STT`、`Update-GithubIp`) として定義する必要があります。
- **WSL Kiwix スクリプト**: `bash` が (WSL 経由で) 利用可能な場合、`.sh` ヘルパー スクリプトはそのまま実行されます。それ以外の場合は、それを `.ps1` または `.bat` に相当するものに適応させます。
- **複数の PowerShell バージョン**: `$PROFILE` は、Windows PowerShell 5.1 と PowerShell 7 の異なるファイルを指します。どのプロファイル ファイルがアクティブであるかを確認するには、各バージョンで `$PROFILE` を実行します。

＃＃ 特徴

- **動的パス**: `PROJECT_ROOT` 環境変数を介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「Start-Service-STT」およびローカルの Wikipedia サービスを実行しようとします。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。