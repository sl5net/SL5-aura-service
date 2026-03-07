# dotool – 설치 및 구성 (Manjaro / Arch-basiert)

## is dotool이었나?

`dotool`은 Linux용 Werkzeug zum Simulieren von Tastatureingaben의 기능입니다.
X11에 대한 기능은 Wayland와 마찬가지로 `xdotool`로 표시되며 기능도 포함되어 있습니다.

---

## 설치 (만자로/아치)

### 1. 패키지 설치

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. 사용자 zur `input` - Gruppe Hinzufügen

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

Ohne Neu-Login grift die Gruppenzugehörigkeit nicht.

---

## 프로젝트 구성

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

## Wie das Skript dotool 버전

### Eingabe-Funktion

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

### 구성 auslesen(ohne Seiteneffekte)

설정은 다음과 같습니다. das `print()` -`settings.py`의 Ausgaben
den Wert nicht verfälschen:

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

## 힌바이제

- **Umlaute und Sonderzeichen:** `유형 지연 2`(도구 기본값 수행) ist empfohlen.
Bei `typedelay 0` können Zeichen wie ä, ö, ü, ß verloren gehen.
- **Zu schnell für die Zielanwendung?** Manche Apps(z. B. Electron, 브라우저 입력)
Verlieren Zeichen bei niedrigem 지연. 가을에는 `dotool_typedelay = 5` oder höher verwenden.
- **Wayland:** Wayland에서 dotool 기능을 사용하면 xdotool을 사용할 수 있습니다.
- **폴백:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.
---

## Wie das Skript dotool 버전

Das Skript startet einen persisten `dotool`-Prozess über ein FIFO,
um den Overhead eines neuen Prozeses bei jedem Tastendruck zu vermeiden.

### 관련 코드(`type_watcher.sh`)

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

### Eingabe-Funktion

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

### 구성 auslesen(ohne Seiteneffekte)

설정은 다음과 같습니다. das `print()` -`settings.py`의 Ausgaben
den Wert nicht verfälschen:

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

## 힌바이제

- **Zu schnell für die Zielanwendung?** Manche Apps(z. B. Electron, 브라우저 입력)
verlieren Zeichen bei 'typedelay 0'. 가을에는 'typedelay 5' 또는 'typedelay 10' 버전이 제공됩니다.
- **Wayland:** Wayland에서 dotool 기능을 사용하면 xdotool을 사용할 수 있습니다.
- **폴백:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.