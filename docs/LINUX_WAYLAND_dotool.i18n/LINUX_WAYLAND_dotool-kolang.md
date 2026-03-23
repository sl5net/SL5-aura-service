# Aura unter Wayland(만자로/아치/CachyOS)

Aura 텍스트는 Wayland 'dotool' 버전에 포함된 Fenster schreiben kann의 텍스트입니다.

### Wichtige Voraussettzungen:
1. **데몬:** `dotoold` muss im Hintergrund laufen(Aura startet diesen automatisch).
2. **설정:** Dein User muss in der Gruppe `input` sein.
3. **입력:** Die Datei `/dev/uinput` muss für die Gruppe `input` beschreibbar sein.

### 마누엘 레파라튀르:
Falls das Tippen nicht funktioniert, führe folgende Befehle aus:
__CODE_BLOCK_0__