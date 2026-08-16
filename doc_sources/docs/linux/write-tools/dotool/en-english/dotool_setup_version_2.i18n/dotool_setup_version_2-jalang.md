# dotool – インストールと設定 (Manjaro / Arch ベース)

＃＃ 概要
`dotool` は、低レベルの入力シミュレーション ユーティリティです。 「xdotool」とは異なり、「uinput」を介して Linux カーネルと直接対話するため、**X11 と Wayland** の両方と互換性があります。

---

## インスタレーション (マンジャロ / アーチ)

### 1. パッケージをインストールする
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. 権限と udev ルール
`dotool` が root 権限なしで入力をシミュレートできるようにするには、ユーザーが `input` グループの一部である必要があり、udev ルールがアクティブである必要があります。

1. **ユーザーをグループに追加します:** `sudo gpasswd -a $USER input`
2. **udev ルールを作成します:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **udev ルールをリロードします:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**重要:** グループの変更を有効にするには、**ログアウトしてから再度ログイン**する必要があります。

---

## プロジェクト設定 (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## スクリプトの実装

### パフォーマンスの最適化 (FIFO)
すべての単語に対して新しい `dotool` インスタンスを開始すると時間がかかります (最大 100 ミリ秒の遅延)。 「瞬時」の入力を実現するために、スクリプトは FIFO パイプから読み取る永続的なバックグラウンド プロセスを使用します。

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### タイピング機能
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Pipe commands directly into the running background process
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

---

## トラブルシューティングと注意事項
- **文字の欠落:** 特殊文字 (ウムラウトなど) がスキップされる場合は、`dotool_typelay` を 5 または 10 に増やします。
- **アプリケーションの互換性:** 一部のアプリ (Electron、ブラウザ) では、高速入力を正しく登録するために、より長い遅延が必要な場合があります。
- **Wayland サポート:** `xdotool` はサポートしていないため、`dotool` は Wayland に必要なバックエンドです。
- **自動フォールバック:** `dotool` がインストールまたは正しく構成されていない場合、スクリプトは自動的に `xdotool` にフォールバックします。