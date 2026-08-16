# dotool – Installation & Konfiguration (Manjaro / Arch-basiert)

## Was ist dotool?

`dotool` ist ein schnelles Werkzeug zum Simulieren von Tastatureingaben unter Linux.
Es ist deutlich schneller als `xdotool` und funktioniert sowohl unter X11 als auch Wayland.

---

## Installation (Manjaro / Arch)

### 1. Paket installieren

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. User zur `input`-Gruppe hinzufügen

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

Ohne Neu-Login greift die Gruppenzugehörigkeit nicht.

---

## Konfiguration im Projekt

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

### Konfiguration auslesen (ohne Seiteneffekte)

Settings werden so ausgelesen, dass `print()`-Ausgaben in `settings.py`
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

## Hinweise

- **Umlaute & Sonderzeichen:** `typedelay 2` (dotool-Default) ist empfohlen.
  Bei `typedelay 0` können Zeichen wie ä, ö, ü, ß verloren gehen.
- **Zu schnell für die Zielanwendung?** Manche Apps (z. B. Electron, Browser-Inputs)
  verlieren Zeichen bei niedrigem Delay. In diesem Fall `dotool_typedelay = 5` oder höher verwenden.
- **Wayland:** dotool funktioniert auch unter Wayland, xdotool hingegen nicht.
- **Fallback:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.
---

## Wie das Skript dotool verwendet

Das Skript startet einen persistenten `dotool`-Prozess über ein FIFO,
um den Overhead eines neuen Prozesses bei jedem Tastendruck zu vermeiden.

### Relevanter Code (`type_watcher.sh`)

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

### Konfiguration auslesen (ohne Seiteneffekte)

Settings werden so ausgelesen, dass `print()`-Ausgaben in `settings.py`
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

## Hinweise

- **Zu schnell für die Zielanwendung?** Manche Apps (z. B. Electron, Browser-Inputs)
  verlieren Zeichen bei `typedelay 0`. In diesem Fall `typedelay 5` oder `typedelay 10` verwenden.
- **Wayland:** dotool funktioniert auch unter Wayland, xdotool hingegen nicht.
- **Fallback:** Wenn dotool nicht installiert ist, fällt das Skript automatisch auf `xdotool` zurück.
