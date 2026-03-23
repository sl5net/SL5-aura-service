# Aura unter Wayland (Manjaro / Arch / CachyOS)

Damit Aura Text in anderen Fenstern schreiben kann, wird unter Wayland `dotool` verwendet.

### Wichtige Voraussetzungen:
1. **Daemon:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch).
2. **Berechtigungen:** Dein Benutzer muss in der Gruppe „Eingabe“ sein.
3. **Uinput:** Die Datei `/dev/uinput` muss für die Gruppe `input` beschreibbar sein.

### Manuelle Reparatur:
Falls das Tippen nicht funktioniert, führen Sie folgende Befehle aus:
__CODE_BLOCK_0__