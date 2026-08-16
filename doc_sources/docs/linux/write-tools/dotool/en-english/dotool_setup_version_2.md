# dotool – Installation & Configuration (Manjaro / Arch-based)

## Overview
`dotool` is a low-level input simulation utility. Unlike `xdotool`, it interacts directly with the Linux kernel via `uinput`, making it compatible with both **X11 and Wayland**.

---

## Installation (Manjaro / Arch)

### 1. Install the Package
```bash
pamac build dotool
# or via yay: yay -S dotool
```

### 2. Permissions & udev Rules
To allow `dotool` to simulate input without root privileges, your user must be part of the `input` group, and a udev rule must be active:

1. **Add user to group:** `sudo gpasswd -a $USER input`
2. **Create udev rule:** 
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
     | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
3. **Reload udev rules:**
   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

**Important:** You must **log out and log back in** for the group changes to take effect.

---

## Project Configuration (`config/settings.py`)

```python
# Override X11 default to use dotool (recommended for better layout stability)
x11_input_method_OVERRIDE = "dotool"

# Delay between keystrokes in milliseconds
# 2ms = Default, reliable for special characters and Umlauts
# 0ms = Maximum speed (Instant mode)
dotool_typedelay = 2
```

---

## Script Implementation

### Performance Optimization (FIFO)
Starting a new `dotool` instance for every word is slow (~100ms latency). To achieve "instant" typing, the script uses a persistent background process reading from a FIFO pipe.

```bash
# Setup in the main script
mkfifo /tmp/dotool_fifo 2>/dev/null
dotool < /tmp/dotool_fifo &
DOTOOL_PID=$!
```

### The Typing Function
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

## Troubleshooting & Notes
- **Missing Characters:** If special characters (like Umlauts) are skipped, increase `dotool_typedelay` to 5 or 10.
- **Application Compatibility:** Some apps (Electron, Browsers) may require a higher delay to register fast input correctly.
- **Wayland Support:** `dotool` is the required backend for Wayland, as `xdotool` does not support it.
- **Automatic Fallback:** The script automatically falls back to `xdotool` if `dotool` is not installed or configured correctly.
