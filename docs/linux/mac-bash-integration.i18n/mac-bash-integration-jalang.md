# macOS Bash シェルの統合

> **macOS Catalina (10.15) より前のデフォルト シェル。** Catalina 以降、macOS にはデフォルト シェルとして Zsh が同梱されています。最新の Mac を使用していて、シェルを変更していない場合は、代わりに [macOS Zsh Integration](.././mac-zsh-integration.i18n/mac-zsh-integration-jalang.md) ガイドを参照してください。
>
> 現在のシェルは次のようにして確認できます。
>「バッシュ」
> $SHELLをエコーする
>「」

STT (Speech-to-Text) CLI との対話を容易にするために、`~/.bash_profile` にショートカット関数を追加できます。これにより、ターミナルに「質問」と入力するだけで済みます。

## セットアップ手順

1. 好みのエディターで Bash 構成を開きます。
   ```bash
   nano ~/.bash_profile
   open -e ~/.bash_profile   # opens in TextEdit
   ```

2. ファイルの最後に次のブロックを貼り付けます。

```bash
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
    local TEMP_FILE=$(mktemp)
    local SHORT_TIMEOUT_SECONDS=2
    local LONG_TIMEOUT_SECONDS=70
    # Path shortcuts
    local PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    local CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"
    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    local EXIT_CODE=$?
    local OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        local KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        local TEMP_FILE_2=$(mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        local EXIT_CODE_2=$?
        local OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ $EXIT_CODE_2 -ne 0 ]; then
             echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        fi
        return 0
    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
```

3. 設定をリロードします。
   ```bash
   source ~/.bash_profile
   ```

## macOS 固有の注意事項

- **「timeout」は macOS に組み込まれていません。** この機能を使用する前に、Homebrew 経由でインストールしてください。
  ```bash
  brew install coreutils
  ```
インストール後、`timeout`は`gtimeout`として利用可能になります。エイリアスを追加するか、上記の関数の `timeout` を `gtimeout` に置き換えます。
  ```bash
  alias timeout=gtimeout
  ```
`~/.bash_profile` の `s()` 関数の上にエイリアスを追加します。

- **macOS はログイン シェルに `~/.bash_profile` を使用します** (ターミナル.app はデフォルトでログイン シェルを開きます)、Linux は通常 `~/.bashrc` を使用します。すべてのコンテキストで関数を使用できるようにしたい場合は、一方からもう一方を取得できます。
  ```bash
  # Add to ~/.bash_profile:
  [ -f ~/.bashrc ] && source ~/.bashrc
  ```

- **macOS には Bash 3.2** が同梱されています (GPLv3 ライセンスのため)。この関数は Bash 3.2 以降と完全な互換性があります。 Bash 5 が必要な場合は、Homebrew 経由でインストールします。
  ```bash
  brew install bash
  ```

- **Python パス**: 仮想環境が `$PROJECT_ROOT/.venv` に設定されていることを確認してください。 `pyenv` または `conda` を使用して Python を管理する場合は、それに応じて `PY_EXEC` を調整してください。

＃＃ 特徴

- **動的パス**: `/tmp` マーカー ファイルを介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「start_service」とローカルの Wikipedia サービスを実行しようとします。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。