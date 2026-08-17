### 条件 1: ドイツ語の文書化

# dotool – インストールと設定 (Manjaro / Arch-basiert)

## dotool でしたか?
`dotool` は、シミュレーションによるシミュレーションの作業に使用されます。私は、**X11 と Wayland** を使用して、`uinput` と関数を使用してカーネルを直接制御する `xdotool` コミュニティを開発しています。

---

## インスタレーション (マンジャロ / アーチ)

### 1. パケットのインストール
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. ベレヒティグンゲン セットツェン
Damit `dotool` ohne Root-Rechte ティッペン ダーフ、muss dein ユーザーはグループ `input` および eine udev-Regel aktiv sein:

1. **ユーザーグループ:** `sudo gpasswd -a $USER input`
2. **udev-Regel:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **ノイラーデンの評価:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Wichtig:** Danach einmal **aus- und neu einloggen**、damit die Gruppenrechte aktiv werden。

---

## Project による構成 (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## スクリプトを実装する

### 永続化プロセス (FIFO)
キーボードのオーバーヘッドは、パイプ (FIFO) のスクリプトを表示するために使用されます。 Dadurch reagiert `dotool` verzögerungsfrei。

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### Die Eingabe-Funktion
```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        # Sendet Befehle direkt an den wartenden Prozess
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" > /tmp/dotool_fifo
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

---

## ヒンヴァイゼ & フェーラーベヘブン
- **Fehlende Zeichen:** Wenn Umlaute verschluckt werden、erhöhe `dotool_typelay` auf 5 or 10.
- **フォールバック:** `dotool` は設定を変更し、`xdotool` を使用してシステムを自動化します。
- **Wayland サポート:** Wayland の `dotool` 自動機能、および `xdotool` の機能をサポートします。