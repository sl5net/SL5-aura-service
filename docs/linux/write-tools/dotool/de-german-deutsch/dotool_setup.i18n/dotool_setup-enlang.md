> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../dotool_setup.md).*

# dotool – Installation & Configuration (Manjaro / Arch-based)

## What is dotool?

`dotool` is a fast tool for simulating keyboard input on Linux.
It is significantly faster than `xdotool` and works on both X11 and Wayland.

---

## Installation (Manjaro / Arch)

### Install 1st package

```bash
pamac build dotool
# oder mit yay:
yay -S dotool
```

### Add users to the `input` group

```bash
sudo gpasswd -a $USER input
```

### Create the 3. udev rule

```bash
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
```

### 4. Reload udev

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 5. Log in again (important!)

Without logging in again, group membership does not apply.

---

## Configuration in the Project

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

## How the script uses dotool

### Input Function

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

### Read configuration (without side effects)

Settings are read in such a way that `print()` outputs in `settings.py`
do not falsify the value:

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

## Notes

- ** Umlaute & Sonderzeichen:** `typedelay 2` (dotool-Default) is recommended.
  In `typedelay 0`, characters such as ä, ö, ü, ß can be lost.
- **Too fast for the target application?** Some apps (e.g. Electron, browser inputs)
  lose signs at low delay. In this case, use `dotool_typedelay = 5` or higher.
- **Wayland:** dotool also works under Wayland, xdotool does not.
- **Fallback:** If dotool is not installed, the script automatically falls back to `xdotool`.
---

## How the script uses dotool

The script starts a persistent `dotool` process via a FIFO,
to avoid the overhead of a new process with each keystroke.

### Relevant code (`type_watcher.sh`)

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

### Input Function

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

### Read configuration (without side effects)

Settings are read in such a way that `print()` outputs in `settings.py`
do not falsify the value:

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

## Notes

- **Too fast for the target application?** Some apps (e.g., Electron, browser inputs)
  lose characters at `typedelay 0`. In this case, use `typedelay 5` or `typedelay 10`.
- **Wayland:** dotool also works under Wayland, whereas xdotool does not.
- **Fallback:** If dotool is not installed, the script automatically falls back to `xdotool`.
