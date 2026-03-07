### マークダウン ドキュメント: `STT/settings/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md`

```markdown
CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# CLI Workflow Tools: FZF to Kate Integration

This document describes a high-efficiency command-line workflow that leverages the fuzzy file search implemented in the `path_navigator` plugin to quickly open files in the Kate editor.

## 1. Fast File Selection (Aura Command)

The `path_navigator` action uses the following Git-aware `fzf` command. Its purpose is to output a file path directly into the system clipboard.

**Command Logic:**
- Uses `git ls-files` inside a Git repository (excludes ignored files).
- Falls back to `find . -type f` outside a Git repository.
- Outputs the selected path to the clipboard using `xclip -selection clipboard`.

## 2. Fast File Execution (The 'k' Function)

To complete the loop, the custom shell function `k` is used. This function takes the path from the clipboard and instantly opens the file in `kate`.

### Implementation

Add the following function to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
# Kate のシステムクリップボードからファイルパスを開く関数
関数 k {
# xclip が利用可能かどうかを確認する
もし ！コマンド -v xclip &> /dev/null;それから
echo "エラー: xclip が必要ですが、インストールされていません。"
1を返す
フィ
  
#1. クリップボードの内容を取得する
CLIPBOARD_CONTENT=$(xclip -選択クリップボード -o 2>/dev/null)
  
# クリップボードが空かどうかを確認する
if [ -z "${CLIPBOARD_CONTENT}" ];それから
echo "エラー: クリップボードが空です。開くものはありません。"
1を返す
フィ

# 2. 複数行のコンテンツをチェックします (単一のファイル パスのみが使用されていることを確認します)
LINE_COUNT=$(エコー "${CLIPBOARD_CONTENT}" | wc -l)
  
if [ "${LINE_COUNT}" -gt 1 ];それから
echo "エラー: クリップボードには ${LINE_COUNT} 行が含まれています。単一行のファイル パスのみがサポートされています。"
1を返す
フィ
  
# 3. 実行前にコマンドを出力する (ユーザーフィードバック)
echo "ケイト \"${CLIPBOARD_CONTENT}\""
  
#4. 最終実行
# コンテンツを囲む二重引用符は、スペースを含むファイル名を正しく処理します。
# 「&」はコマンドをバックグラウンドで実行し、ターミナルを解放します。
ケイト「${CLIPBOARD_CONTENT}」&
}
```

### Usage

1.  Use the `path_navigator` command (e.g., type `search file` in your trigger tool).
2.  Find and select the desired file (e.g., `src/main/config.py`).
3.  In your terminal, type `k` and press **ENTER**.
4.  The file opens instantly in Kate.
```