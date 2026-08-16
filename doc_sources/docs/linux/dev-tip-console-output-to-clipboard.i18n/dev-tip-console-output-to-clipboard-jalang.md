# 開発ヒント: コンソール出力をクリップボードに自動的にコピーする

**カテゴリ:** Linux / シェルの生産性  
**プラットフォーム:** Linux (zsh + Konsole/KDE)

---

＃＃ 問題

AI アシスタントを使用する場合、多くの場合、ターミナル出力をコピーしてチャットに貼り付ける必要があります。これは通常、次のことを意味します。
1. コマンドを実行する
2. マウスで出力を選択します
3. コピー
4. ブラウザに切り替える
5.貼り付け

それは手順が多すぎます。

---

## 解決策: `preexec` / `precmd` による自動キャプチャ

これを `~/.zshrc` に追加します。

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}


precmd() {
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        cleaned=$(cat ~/t.txt \
            | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | sed "s|$HOME|~|g" \
            | sed 's/[^[:print:]]//g' \
            | grep -v '^$')
        if [ -n "$cleaned" ]; then
            echo "$cleaned" | xclip -selection clipboard
            echo "[📋 In Zwischenablage kopiert]"
        fi
    fi
}

```

次にリロードします。
```bash
source ~/.zshrc
```

＃＃＃ 結果

すべてのコマンドの後、出力は自動的にクリップボードに保存され、**Ctrl+V** を使用して AI チャットに貼り付けることができます。

出力は常に参照用に `~/t.txt` に保存されます。

---

## 仕組み

|パート |何をするのか |
|------|---------------|
| `preexec()` |各コマンドの前に実行され、出力が `~/t.txt` にリダイレクトされます。
| `precmd()` |各コマンドの後に実行され、標準出力が復元され、クリップボードにコピーされます。
| `tee ~/t.txt` |出力をターミナルに表示しながらファイルに保存します。
| `sed '...'` | KDE Konsole タイトルのエスケープ シーケンス (`]2;...` `]1;`) を削除します。
| `xクリップ` |クリーンアップされた出力をクリップボードにコピーします。

---

＃＃ 要件

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️してはいけないこと

`fc -ln -1 | 'は **使用しないでください** bash` を実行して最後のコマンドを再実行します。

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

これにより、すべてのコマンドが終了後に再実行され、ファイルの上書き、`git commit` の再実行、`sed -i` の再実行など、破壊的な副作用が発生する可能性があります。

上記の「preexec」/「precmd」アプローチは、**実行中**、安全かつ信頼性の高い出力をキャプチャします。