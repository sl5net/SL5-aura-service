> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../setup.md).*

## Text Input Method Configuration

### Requirements for `dotool` (faster than xdotool)

1. Install: `pamac build dotool` or `yay -S dotool`
2. Add user to the input group: `sudo gpasswd -a $USER input`
3. Create udev rule:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Reload rules: `sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **Log in again**

### Configuration

In `config/settings.py`:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### Notes

- `dotool` is significantly faster than `xdotool` – with very fast output, the target application may lose characters
- Reading out the settings deliberately suppresses all print outputs from `settings.py` during import – this is intentional
- The dotool listener runs as a background process via a FIFO (`/tmp/dotool_fifo`) with `typedelay 0`

---
