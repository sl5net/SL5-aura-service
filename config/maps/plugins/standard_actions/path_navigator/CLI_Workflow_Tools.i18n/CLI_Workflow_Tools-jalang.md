# CLI ワークフロー ツール インストール ガイド

パス ナビゲーター プラグインの一部のアクションは、外部コマンド ライン ユーティリティに依存して、あいまい検索の実行、ファイルのリスト表示、およびクリップボードの操作を行います。これらのツールがない場合は、システム コンソールに警告が表示されます。

以下は、サポートされている各オペレーティング システムのインストール手順です。

## 必要なユーティリティ

* **`fzf`**: 汎用コマンドラインファジーファインダー。
* **`find`** (または `fd`): 標準のファイル検索ユーティリティ。
* **クリップボード ツール**: 出力をシステムのクリップボードに直接パイプするために使用されます。
* **Linux:** `xclip` (X11 環境が必要)。
* **macOS:** `pbcopy` (プリインストール)。
* **Windows:** `clip` (プリインストール)。
* **`file`**: 完全な端末プレビューのファイル タイプを決定します。

---

## インストール手順

### 1. Linux (Arch / Manjaro)
システムは Manjaro 上で実行されるため、「pacman」を使用して必要なパッケージをインストールできます。

```bash
sudo pacman -S fzf findutils xclip file
```



## 1. 高速ファイル選択 (Aura コマンド)

「path_navigator」アクションは、次の Git 対応の「fzf」コマンドを使用します。その目的は、ファイル パスをシステム クリップボードに直接出力することです。

**コマンドロジック:**
- Git リポジトリ内で `git ls-files` を使用します (無視されたファイルは除外します)。
- `find にフォールバックします。 Git リポジトリの外で -type f` を入力します。
- `xclip -selection Clipboard`を使用して、選択したパスをクリップボードに出力します。

## 2. ファイルの高速実行 (「k」関数)

ループを完了するには、カスタム シェル関数 `k` が使用されます。この関数はクリップボードからパスを取得し、即座に `kate` でファイルを開きます。

＃＃＃ 実装

次の関数をシェルの設定ファイル (例: `~/.bashrc`、`~/.zshrc`) に追加します。

```bash
# Function to open a file path from the system clipboard in Kate
function k {
    # Check if xclip is available
    if ! command -v xclip &> /dev/null; then
        echo "Error: xclip is required but not installed."
        return 1
    fi
    
    # 1. Get clipboard content
    CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
    
    # Check if clipboard is empty
    if [ -z "${CLIPBOARD_CONTENT}" ]; then
        echo "Error: Clipboard is empty. Nothing to open."
        return 1
    fi

    # 2. Check for multiline content (ensures only a single file path is used)
    LINE_COUNT=$(echo "${CLIPBOARD_CONTENT}" | wc -l)
    
    if [ "${LINE_COUNT}" -gt 1 ]; then
        echo "Error: Clipboard contains ${LINE_COUNT} lines. Only single-line file paths are supported."
        return 1
    fi
    
    # 3. Print the command before execution (User Feedback)
    echo "kate \"${CLIPBOARD_CONTENT}\""
    
    # 4. Final Execution
    # The double quotes around the content handle filenames with spaces correctly.
    # The '&' runs the command in the background, freeing the terminal.
    kate "${CLIPBOARD_CONTENT}" &
}
```

＃＃＃ 使用法

1. 「path_navigator」コマンドを使用します（たとえば、トリガーツールに「search file」と入力します）。
2. 目的のファイル (例: `src/main/config.py`) を見つけて選択します。
3. 端末で「k」と入力し、**ENTER** を押します。
4. ファイルは Kate で即座に開きます。
__CODE_BLOCK_2__