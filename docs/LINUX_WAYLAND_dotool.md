# dotool on Wayland — Setup & Troubleshooting

`dotool` is required for Aura to type text into other applications on Wayland.
Unlike `xdotool`, it communicates directly with the Linux kernel via `uinput`
and works on both **X11 and Wayland**.

On X11, `xdotool` is used by default. `dotool` is optional on X11 but
recommended for better layout stability (especially with Umlauts).

---

## 1. Install dotool

**Arch / Manjaro / CachyOS (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu / Debian (if available in repos):**
```bash
sudo apt install dotool
```

**If not in repos — build from source:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. Allow dotool to run without root (required)

`dotool` needs access to `/dev/uinput`. Without this, it will fail silently.

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

**Re-login required** after the group change for it to take effect.

---

## 3. Verify the installation

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

If `groups` does not show `input`, log out and back in (or reboot).

---

## 4. How Aura uses dotool

Aura's `type_watcher.sh` automatically:

- Detects Wayland via `$WAYLAND_DISPLAY` and selects `dotool`
- Starts `dotoold` daemon in the background if it exists and is not running
- Falls back to `xdotool` if `dotool` is not installed (X11 only)
- Sets the keyboard layout from your active Vosk model (e.g. `de` → `XKB_DEFAULT_LAYOUT=de`)

No manual daemon management is needed — Aura handles this on startup.

---

## 5. Troubleshooting

**Aura transcribes but no text appears:**
```bash
# Check if dotool is installed:
command -v dotool

# Check group membership:
groups | grep input

# Test manually (focus a text field first):
echo "type hello" | dotool

# Check the watcher log:
tail -30 log/type_watcher.log
```

**Missing or garbled characters (especially Umlauts):**

Increase the typing delay in `config/settings_local.py`:
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool works in terminal but not in Aura:**

Check that the `input` group is active in the desktop session (not just a new terminal).
A full re-login is required after `gpasswd`.

**Force dotool on X11** (optional, for better layout stability):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. Fallback if dotool cannot be installed

If `dotool` is unavailable on your system, Aura falls back to `xdotool` on X11.
On Wayland without `dotool`, typing is **not supported** — this is a Wayland
security restriction, not an Aura limitation.

Alternative tools that may work on specific compositors:

| Tool | Works on |
|---|---|
| `xdotool` | X11 only |
| `dotool` | X11 + Wayland (recommended) |
| `ydotool` | X11 + Wayland (alternative) |

To use `ydotool` as a manual workaround:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
Note: Aura does not integrate `ydotool` natively — manual configuration required.
