# POSIX sh / Dash の統合

STT (Speech-to-Text) CLI との対話を容易にするために、シェル プロファイルにショートカット関数を追加できます。これにより、ターミナルに「質問」と入力するだけで済みます。

> **注意:** Dash およびその他の厳密な POSIX シェル (Debian/Ubuntu の `/bin/sh` はデフォルトで Dash) は、すべてのコンテキスト、プロセス置換、または配列で `local` キーワードをサポートしません**。以下の関数は、完全に POSIX 互換になるように作成されています。

## セットアップ手順

1. 好みのエディタでシェル プロファイルを開きます。
   ```sh
   nano ~/.profile
   # or, if your system uses ~/.shrc for interactive shells:
   nano ~/.shrc
   ```

2. ファイルの最後に次のブロックを貼り付けます。

```sh

please read newest updates in zsh - verson


# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
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
    timeout "$SHORT_TIMEOUT_SECONDS" \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
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
            sh "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ "$EXIT_CODE" -eq 124 ] || [ "$EXIT_CODE" -eq 0 ]; then
        if [ "$EXIT_CODE" -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout "$LONG_TIMEOUT_SECONDS" \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$@" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ "$EXIT_CODE_2" -ne 0 ]; then
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
   ```sh
   . ~/.profile
   ```

## POSIX / ダッシュ固有の注意事項

- 互換性を最大限に高めるために、「local」はここでは使用されません**。すべての変数は、規則によってのみ関数スコープに設定されます。これらは厳密な POSIX sh では技術的にグローバルです。
- コマンドに引数を渡すときは、引用符で囲まれた引数による適切な単語の分割を維持するために、「$*」よりも「$@」が優先されます。
- Kiwix ヘルパー スクリプトを実行するときに、「bash」は「sh」に置き換えられ、POSIX ツールチェーン内に留まります。
- この設定ファイルは、ログイン シェルによって取得される `~/.profile` に配置するのが最適です。インタラクティブな非ログイン シェルの場合、ディストリビューションで `~/.shrc` が使用される場合があります。システムのドキュメントを確認してください。

＃＃ 特徴

- **動的パス**: `/tmp` マーカー ファイルを介してプロジェクト ルートを自動的に検索します。
- **自動再起動**: バックエンドがダウンしている場合、「start_service」とローカルの Wikipedia サービスを実行しようとします。
- **スマート タイムアウト**: 最初に 2 秒の素早い応答を試み、その後 70 秒の詳細な処理モードに戻ります。