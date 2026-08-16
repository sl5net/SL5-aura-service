## Text Input Method Konfiguration

### Voraussetzungen für `dotool` (schneller als xdotool)

1. Installieren: `pamac build dotool` oder `yay -S dotool`
2. User zur input-Gruppe hinzufügen: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Regeln neu laden: `sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **Neu einloggen**

### Konfiguration

In `config/settings.py`:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### Hinweise

- `dotool` ist deutlich schneller als `xdotool` – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- Das Auslesen der Settings unterdrückt bewusst alle Print-Ausgaben aus `settings.py` während des Imports – das ist gewollt
- Der dotool-Listener läuft als Hintergrundprozess über ein FIFO (`/tmp/dotool_fifo`) mit `typedelay 0`

---
