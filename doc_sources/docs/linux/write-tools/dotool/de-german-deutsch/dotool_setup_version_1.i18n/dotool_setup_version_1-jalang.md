# dotool – インストールと設定 (Manjaro / Arch-basiert)

## dotool でしたか?

`dotool` は、Linux 上でのシミュレーションを行うためのシュネルです。
ドイツ語のシュネラーは「xdotool」であり、X11 の機能は Wayland と同じです。

---

## インスタレーション (マンジャロ / アーチ)

### 1. パケットのインストール

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. ユーザー zur `input`-Gruppe hinzufügen

```bash
sudo gpasswd -a $USER input
```

### 3. udev-Regel erstellen

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

### 4. udev neu laden

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 5. Neu einloggen (wichtig!)

Ohne Neu-Login は Gruppenzugehörigkeit nicht にログインします。

---

## プロジェクトによる構成

### `config/settings.py`

```python
# Eingabemethode für X11: "dotool" (schnell) oder "xdotool" (Fallback)
x11_input_method_OVERRIDE = "dotool"

# Delay zwischen Tastenanschlägen in Millisekunden
# 2ms = dotool-Default, zuverlässig auch für Umlaute (ä, ö, ü, ß)
# 0ms = maximal schnell, kann Sonderzeichen verschlucken
dotool_typedelay = 2
```

---

## Wie das Skript dotool verwendet

### アインガベファンクション

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay %s\ntype %s\n' "$DOTOOL_TYPEDELAY" "$text" | dotool
    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

### Konfiguration auslesen (ohne Seitenefekte)

設定は非常に重要なので、`settings.py` の `print()`-Ausgaben を実行します。
デン・ヴェルト・ニヒト・フェルシェン:

```bash
OVERRIDE=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.x11_input_method_OVERRIDE)
")
[[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"

DOTOOL_TYPEDELAY=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.dotool_typedelay)
")
```

---

## ヒンヴァイセ

- **Umlaute und Sonderzeichen:** `type late 2` (do tools-Default) は empfohlen です。
`typelay 0` は、ä、ö、ü、ß の状況を理解するための Zeichen です。
- **Zielanwendung をどうするか?** Manche Apps (z.B. Electron、ブラウザ入力)
Verlieren Zeichen bei niedrigem 遅延。秋には `dotool_typelay = 5` が更新されます。
- **Wayland:** Wayland の dotool 機能、xdotool ヒンジ機能。
- **フォールバック:** dotool をインストールするには、`xdotool` を使用してスクリプトを自動実行します。
---

## Wie das Skript dotool verwendet

Das Skript startet einenpersisten `dotool`-Prozess über ein FIFO,
ウム デン オーバーヘッド エイネス ノイエン プロゼス ベイ ジェデム タステンドルック ツー ヴァーメイデン。

### 関連コード (`type_watcher.sh`)

```bash
export DOTOOL_DELAY=0

# Alten Listener beenden falls noch läuft
pkill -f "dotool < /tmp/dotool_fifo" 2>/dev/null

DOTOOL_PID=$!

# typedelay direkt nach Start setzen
sleep 0.1
echo "typedelay 0" > /tmp/dotool_fifo

# Cleanup beim Beenden
trap "kill $DOTOOL_PID 2>/dev/null; rm -f /tmp/dotool_fifo" EXIT
```

### アインガベファンクション

```bash
do_type() {
    local text="$1"
    if [[ "$INPUT_METHOD" == "dotool" ]]; then
        printf 'typedelay 0\ntype %s\n' "$text" | dotool
        # printf 'typedelay 0\ntype %s\n' "$text" > /tmp/dotool_fifo
        # printf 'type %s\n' "$text" | dotool

    else
        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 12 "$text"
    fi
}
```

### Konfiguration auslesen (ohne Seitenefekte)

設定は非常に重要なので、`settings.py` の `print()`-Ausgaben を実行します。
デン・ヴェルト・ニヒト・フェルシェン:

```bash
OVERRIDE=$(python3 -c "
import importlib.util, sys, io
spec = importlib.util.spec_from_file_location('settings', '$(pwd)/config/settings.py')
old_stdout = sys.stdout
sys.stdout = io.StringIO()
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sys.stdout = old_stdout
print(mod.x11_input_method_OVERRIDE)
")
[[ "$OVERRIDE" == "dotool" ]] && INPUT_METHOD="dotool"
```

---

## ヒンヴァイセ

- **Zielanwendung をどうするか?** Manche Apps (z.B. Electron、ブラウザ入力)
Zeichen は「typelay 0」を検証します。秋には `typelay 5` または `typelay 10` が更新されます。
- **Wayland:** Wayland の dotool 機能、xdotool ヒンジ機能。
- **フォールバック:** dotool をインストールするには、`xdotool` を使用してスクリプトを自動実行します。