# コマンド プロンプト (CMD) の統合 (Windows)

Windows コマンド プロンプトから STT (Speech-to-Text) CLI を簡単に操作できるようにするには、「s.bat」バッチ ファイルを作成し、それを「PATH」に配置します。これにより、CMD ウィンドウに「質問」と入力するだけで済みます。

> **注:** CMD (cmd.exe) は従来の Windows シェルであり、PowerShell や Unix シェルと比較して重大な制限があります。より充実したエクスペリエンスを得るには、代わりに [PowerShell Integration](.././powershell-integration.i18n/powershell-integration-jalang.md) または [WSL Integration](.././wsl-integration.i18n/wsl-integration-jalang.md) の使用を検討してください。

## セットアップ手順

### 1. 個人用スクリプト用のディレクトリを作成します (まだ作成していない場合)。

```cmd
mkdir %USERPROFILE%\bin
```

### 2. そのディレクトリを PATH に追加します (1 回限りのセットアップ)

**システム プロパティ → 環境変数** を開き、ユーザーの `PATH` 変数に `%USERPROFILE%\bin` を追加します。

あるいは、管理者特権の CMD プロンプトでこれを実行します (CMD を再度開いた後に有効になります)。

```cmd
setx PATH "%USERPROFILE%\bin;%PATH%"
```

### 3. バッチファイルを作成する

メモ帳または任意のテキスト エディタを開き、以下を `%USERPROFILE%\bin\s.bat` として保存します。

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

### 4. テストしてみる

新しい CMD ウィンドウを開き (更新された PATH がロードされます)、次のように入力します。

```cmd
s your question here
```

## CMD 固有の注意事項

- **ネイティブ プロセス タイムアウトなし**: CMD には、Unix の「タイムアウト」に相当するものがありません。このスクリプトは、タイムアウト ロジックを PowerShell の `WaitForExit` にインラインで委任します。 PowerShell が利用可能である必要があります (最新のすべての Windows システムにあります)。
- **`PROJECT_ROOT`**: システム プロパティを介してこれを永続的なユーザー環境変数として設定するか、`.bat` ファイル内のパスをハードコードします。
- **ヘルパー スクリプト**: `update_github_ip.bat` と `start_service.bat` が `PATH` または `%USERPROFILE%\bin` に存在する必要があります。これらは、CMD の「update_github_ip」および「start_service」シェル関数に相当します。
- **Kiwix スクリプト用の `bash`**: WSL がインストールされている場合、CMD で `bash` が利用可能になり、`.sh` スクリプトが直接実行されます。それ以外の場合は、「kiwix-docker-start-if-not-running.sh」を同等の「.bat」に適応させます。
- **引用符の処理**: CMD には厳密かつ脆弱な引用規則があります。クエリに特殊文字 (`&`、`|`、`>`、`<`) が含まれている場合は、クエリ全体を二重引用符で囲みます: `s "your & question"`。
- **`set /p` の制限**: `set /p` はファイルの最初の行のみを読み取ります。複数行の出力の場合は、`type` を使用してファイルを直接出力します (ロングタイムアウト分岐で実行したように)。

＃＃ 特徴

- **動的パス**: `PROJECT_ROOT` 環境変数を介してパスを自動的に解決します。
- **自動再起動**: バックエンドがダウンしている場合、`start_service.bat` を呼び出し、ローカルの Wikipedia サービスの開始を試みます。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。