> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../dotool_setup_version_2.md).*

### Part 1: German Documentation

# dotool – Installation & Configuration (Manjaro / Arch-based)

## What is dotool?
`dotool` is a tool for simulating keyboard input. Unlike `xdotool`, it communicates directly with the kernel via `uinput` and therefore works universally under **X11 and Wayland**.

---

## Installation (Manjaro / Arch)

### 1. Install package
```bash
pamac build dotool
# oder: yay -S dotool
```

### 2. Set Permissions
In order for `dotool` to type without root rights, your user must be in the `input` group and a udev rule must be active:

1. **User to the group:** `sudo gpasswd -a $USER input`
2. **udev rule:**
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Reload rules:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Important:** After that, **log out and log in again**, so that the group permissions become active.

---

## Configuration in the project (`config/settings.py`)

```python
# Erzwingt dotool unter X11 (empfohlen für bessere Layout-Stabilität)
x11_input_method_OVERRIDE = "dotool"

# Verzögerung zwischen Anschlägen (in ms)
# 2ms = Standard, sicher für Umlaute (ä, ö, ü, ß)
# 0ms = Maximal schnell (Blitz-Modus)
dotool_typedelay = 2
```

---

## Implementation in the script

### Persistent Process (FIFO)
To avoid the overhead of constantly recreating the virtual keyboard, the script uses a pipe (FIFO). This allows `dotool` to respond without delay.

```bash
# Vorbereitung im Hauptskript
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### The Input Function
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

## Notes & Troubleshooting
- **Missing characters:** If umlauts are being dropped, increase `dotool_typedelay` to 5 or 10.
- **Fallback:** If `dotool` is not configured correctly, the system automatically falls back to `xdotool`.
- **Wayland Support:** Under Wayland, `dotool` is automatically preferred because `xdotool` does not work there.

