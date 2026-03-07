# dotool – Instalación y configuración (Manjaro / Arch-basiert)

## ¿Era dotool?

`dotool` es una herramienta de simulación de tareas rápidas en Linux.
Es un software alemán como `xdotool` y funcional también en X11 y Wayland.

---

##Instalación (Manjaro/Arco)

### 1. Instalación del paquete

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### 2. Usuario en `input`-Gruppe hinzufügen

```bash
sudo gpasswd -a $USER input
```

### 3. udev-Regel erstellen

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

### 4. udev nuevo cargado

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 5. Nuevo registro (¡qué!)

Ohne Neu-Login greift die Gruppenzugehörigkeit no.

---

## Configuración en el proyecto

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

## Cómo usar la herramienta Skript

### Función Eingabe

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

### Configuración auslesen (ohne Seiteneffekte)

Las configuraciones se configuran de esta manera, ingresando `print()` en `settings.py`
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

- **Umlaute und Sonderzeichen:** `type delay 2` (hacer herramienta-predeterminado) está activado.
Bei `typedelay 0` puede verloren gehen ä, ö, ü, ß verloren gehen.
- **¿Zu schnell für die Zielanwendung?** Manche Apps (por ejemplo, B. Electron, Browser-Inputs)
verlieren Zeichen bei niedrigem Delay. En este caso Fall `dotool_typedelay = 5` o más alto.
- **Wayland:** Dotool funciona también en Wayland, pero no se incluye xdotool.
- **Reserva:** Si no se instala dotool, el script se activa automáticamente en `xdotool`.
---

## Cómo usar la herramienta Skript

El script inicia un proceso persistente `dotool` sobre un FIFO,
um den Overhead eines nuevos procesos bei jedem Tastendruck zu vermeiden.

### Código relevante (`type_watcher.sh`)

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

### Función Eingabe

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

### Configuración auslesen (ohne Seiteneffekte)

Las configuraciones se configuran de esta manera, ingresando `print()` en `settings.py`
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

- **¿Zu schnell für die Zielanwendung?** Manche Apps (por ejemplo, B. Electron, Browser-Inputs)
Verlieren Zeichen bei `typedelay 0`. En este caso, se utilizan `typedelay 5` o `typedelay 10`.
- **Wayland:** Dotool funciona también en Wayland, pero no se incluye xdotool.
- **Reserva:** Si no se instala dotool, el script se activa automáticamente en `xdotool`.