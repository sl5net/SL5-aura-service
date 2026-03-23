# Aura bajo Wayland (Manjaro / Arch / CachyOS)

Damit Aura Text in other Fenster schreiben kann, wird unter Wayland `dotool` verwendet.

### Wichtige Voraussetzungen:
1. **Daemon:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch).
2. **Berechtigungen:** El usuario debe ingresar al grupo `input` sein.
3. **Uinput:** La fecha `/dev/uinput` debe ser escrita para el grupo `input`.

### Manuelle Reparatur:
Falls das Tippen no funciona, führe folgende Befehle aus:
__CODE_BLOCK_0__