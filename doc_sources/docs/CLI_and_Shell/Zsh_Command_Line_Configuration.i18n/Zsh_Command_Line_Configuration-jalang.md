このドキュメントでは、コマンド ラインを介して Python サービスと対話するための最終的な検証済みの Zsh 構成を要約します。

この構成では、安全な出力から即時実行まで、サービスにアクセスするための 3 つの異なる方法が提供されます。

## Zsh コマンドライン構成の概要

### 1. 設定ファイル

以下のコードはすべて **`~/.zshrc`** ファイルに貼り付ける必要があります。 **`source ~/.zshrc`** を忘れずに行うか、変更を加えた後に新しいターミナル セッションを開きます。

### 2. 最終的なコードブロック

このブロックは 3 つの必要な関数を定義します。これには、以前に発生した競合エラーを防ぐために必要な `unalias` コマンドが含まれています。

```bash
# ===================================================================
# == 1. sl: Output Only (Safe Mode - Just prints the result)
# ===================================================================

# Unalias 'sl' in case it was previously defined as a simple alias
unalias sl 2>/dev/null
sl() {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    /home/seeh/projects/py/STT/.venv/bin/python3 /home/seeh/projects/py/STT/scripts/py/cli_client.py "$*" --lang "de-DE"
}
# source ~/.zshrc


# ===================================================================
# == 2. slz: Zsh Line Insertion (Safe Prep Mode - Paste output to prompt)
# ===================================================================

# Unalias 'slz' in case it was previously defined as an alias
unalias slz 2>/dev/null
slz() {
    if [ $# -eq 0 ]; then
        echo "Usage: slz <your question whose result should be pasted to the line>"
        return 1
    fi

    # 1. Execute the client and capture the output (the command string)
    # "$*" ensures all arguments are passed as a single string to the CLI client.
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" --lang "de-DE")

    # 2. Use 'print -z' to paste the captured command into the current prompt line.
    print -z "$COMMAND"
}
# source ~/.zshrc

# ===================================================================
# == 3. slxXsoidfuasdzof: Immediate Execution (DANGEROUS MODE)
# ===================================================================

# Unalias the long name in case it was previously defined
unalias slxXsoidfuasdzof 2>/dev/null
slxXsoidfuasdzof() {
    if [ $# -eq 0 ]; then
        echo "Usage: slx <your question whose result will be executed immediately>"
        return 1
    fi

    # Führt den CLI-Client aus und speichert die Ausgabe in der Variable 'COMMAND'
    COMMAND=$(/home/seeh/projects/py/STT/.venv/bin/python3 \
        /home/seeh/projects/py/STT/scripts/py/cli_client.py \
        "$*" \
        --lang "de-DE")

    # Check if any output was received
    if [ -n "$COMMAND" ]; then
        echo "--> Ausführen des Befehls: $COMMAND"
        echo "--> Executing command: $COMMAND"
        # DANGER: 'eval' executes the command string immediately
        eval "$COMMAND"
    else
        echo "No command output received from the service."
    fi
}
# source ~/.zshrc

```

---

### 3. 3 つのコマンドの使用法

|コマンド |機能 |安全レベル |例 |
| :--- | :--- | :--- | :--- |
| **`sl`** | **標準出力:** サービスを実行し、出力全体をコンソールに直接出力します。 | **安全** | `sl 家とは何か` (プリント:「家とは...」) |
| **`slz`** | **安全な実行の準備:** サービスを実行し、出力 (シェル コマンドなど) を Zsh 入力行に貼り付けて、レビューまたは実行の準備を整えます。 | **安全/準備** | `slz git` (貼り付け: `git add . && git commit...` **ただし、実行されません**。)
| **`slxXsoidfuasdzof`** | **即時実行:** サービスを実行し、出力をシェル コマンドとして直ちに実行します。セキュリティ対策として暗号名を使用します。 | **危険** | `slxXsoidfuasdzof git` (`git add...` コマンドをすぐに実行します。)