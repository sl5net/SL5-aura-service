## Configuración del método de entrada de texto

### Voraussetzungen für `dotool` (schneller como xdotool)

1. Instalar: `pamac build dotool` o `yay -S dotool`
2. Usuario en el grupo de entrada: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Nueva carga: `sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **Nuevo registro**

### Configuración

En `config/settings.py`:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### Hinweise

- `dotool` ist deutlich schneller als `xdotool` – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- Das Auslesen der Settings unterdrückt bewusst alle Print-Auslesen aus `settings.py` während des Imports – das ist gewollt
- El oyente de dotool funciona como proceso de fondo sobre un FIFO (`/tmp/dotool_fifo`) con `typedelay 0`

---