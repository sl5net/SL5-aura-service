# フィッシュシェルの統合

STT (Speech-to-Text) CLI との対話を容易にするために、Fish 構成にショートカット機能を追加できます。これにより、ターミナルに「質問」と入力するだけで済みます。

## セットアップ手順

Fish Shell は関数を個別のファイルとして保存します。推奨されるアプローチは、専用の関数ファイルを作成することです。

1. 関数ファイルを作成します (ディレクトリが存在しない場合は自動的に作成されます)。
   ```fish
   mkdir -p ~/.config/fish/functions
   nano ~/.config/fish/functions/s.fish
   ```

2. 次のブロックをファイルに貼り付けます。

```fish


please newest updates in zsh - verson


# --- STT Project Path Resolution ---
function s --description "STT CLI shortcut"
    if test (count $argv) -eq 0
        echo "question <your question>"
        return 1
    end

    update_github_ip

    set TEMP_FILE (mktemp)
    set SHORT_TIMEOUT_SECONDS 2
    set LONG_TIMEOUT_SECONDS 70

    # Path shortcuts
    set PY_EXEC "$PROJECT_ROOT/.venv/bin/python3"
    set CLI_SCRIPT "$PROJECT_ROOT/scripts/py/cli_client.py"

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    set EXIT_CODE $status
    set OUTPUT (cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    if echo "$OUTPUT" | grep -q "Verbindungsfehler"; or not pgrep -f "streamlit-chat.py" > /dev/null
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        set KIWIX_SCRIPT "$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if test -f "$KIWIX_SCRIPT"
            bash "$KIWIX_SCRIPT"
        end
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $argv"
        return 1

    # 2. Timeout (124) OR success (0)
    else if test $EXIT_CODE -eq 124; or test $EXIT_CODE -eq 0
        if test $EXIT_CODE -eq 0
            echo "$OUTPUT"
            return 0
        end
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        set TEMP_FILE_2 (mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
            "$PY_EXEC" -u "$CLI_SCRIPT" $argv \
            --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        set EXIT_CODE_2 $status
        set OUTPUT_2 (cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if test $EXIT_CODE_2 -ne 0
            echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        end
        return 0

    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    end
end
```

3. この機能は、すべての新しい Fish セッションですぐに使用できます。新しいターミナルを開かずに現在のセッションにロードするには:
   ```fish
   source ~/.config/fish/functions/s.fish
   ```

## 魚特有の注意事項

- Fish は、変数の割り当てに「VAR=value」の代わりに「set VAR value」を使用します。
- 条件では、`[ ]` と `fi` の代わりに `test` と `end` ブロックを使用します。
- `$argv` は、引数を渡すための `$*` / `$@` を置き換えます。
- 終了コードの `$status` は `$?` を置き換えます。
- 条件式内の `||` / `&&` は `or` / `and` に置き換えられます。
- Fish は「ローカル」を使用しません**。関数内のすべての変数はデフォルトでローカルです。

＃＃ 特徴

- **動的パス**: `/tmp` マーカー ファイルを介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「start_service」とローカルの Wikipedia サービスを実行しようとします。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。