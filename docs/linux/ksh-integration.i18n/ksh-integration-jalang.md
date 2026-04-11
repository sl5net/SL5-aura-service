# Ksh (Korn シェル) の統合

STT (Speech-to-Text) CLI との対話を容易にするために、`~/.kshrc` にショートカット関数を追加できます。これにより、ターミナルに「質問」と入力するだけで済みます。

## セットアップ手順

1. 好みのエディターで Ksh 構成を開きます。
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. ファイルの最後に次のブロックを貼り付けます。

```ksh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
function s {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
    TEMP_FILE=$(mktemp)
    SHORT_TIMEOUT_SECONDS=2
    LONG_TIMEOUT_SECONDS=70
    # Path shortcuts
    PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"
    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    EXIT_CODE=$?
    OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
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
        TEMP_FILE_2=$(mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
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

3. Ksh が構成ファイルをロードしていることを確認します。これを `~/.profile` に追加または確認します。
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. 設定をリロードします。
   ```ksh
   . ~/.kshrc
   ```

## Ksh 固有の注意事項

- Ksh は、`function name { }` と `name() { }` 構文の両方をサポートします。ここではわかりやすくするために「function」キーワードを使用しています。
- `local` は、すべての Ksh バリアント (例: `ksh88`) でサポートされません**。したがって、上記の関数内の変数は「local」なしで宣言されます。 `mksh` または `ksh93` を使用している場合は、代わりに `typeset` を使用できます: `typeset TEMP_FILE=$(mktemp)`。
- `ENV` 変数は、`.bashrc` と同様に、対話型セッションのどのファイル Ksh ソースを制御します。

＃＃ 特徴

- **動的パス**: `/tmp` マーカー ファイルを介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「start_service」とローカルの Wikipedia サービスを実行しようとします。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。