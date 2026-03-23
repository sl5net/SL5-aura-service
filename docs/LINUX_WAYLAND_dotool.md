# Aura unter Wayland (Manjaro / Arch / CachyOS)

Damit Aura Text in andere Fenster schreiben kann, wird unter Wayland `dotool` verwendet.

### Wichtige Voraussetzungen:
1. **Daemon:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch).
2. **Berechtigungen:** Dein User muss in der Gruppe `input` sein.
3. **Uinput:** Die Datei `/dev/uinput` muss für die Gruppe `input` beschreibbar sein.

### Manuelle Reparatur:
Falls das Tippen nicht funktioniert, führe folgende Befehle aus:
```bash
sudo usermod -aG input $USER
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
# Danach: REBOOT
