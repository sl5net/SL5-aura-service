# Aura dla Waylanda (Manjaro / Arch / CachyOS)

Damit Aura Tekst w innym języku Fenster schreiben, wird dla Wayland `dotool` verwendet.

### Wichtige Voraussetzungen:
1. **Daemon:** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch).
2. **Berechtigungen:** Dein User muss in der Gruppe `input` sein.
3. **Uinput:** Die Datei `/dev/uinput` muss für die Gruppe `input` beschreibbar sein.

### Manuelle naprawczy:
Falls das Tippen nicht funktioniert, führe folgende Befehle aus:
__KOD_BLOKU_0__