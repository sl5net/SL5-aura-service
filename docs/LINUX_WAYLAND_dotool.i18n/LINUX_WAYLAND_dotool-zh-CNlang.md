# Aura unter Wayland (Manjaro / Arch / CachyOS)

Damit Aura 文本位于 andere Fenster schreiben kann，在 Wayland `dotool` verwendet 下。

### Wichtige Voraussetzungen：
1. **守护进程：** `dotoold` muss im Hintergrund laufen (Aura startet diesen automatisch)。
2. **说明：** 用户在“输入”组中混乱。
3. **Uinput:** 将 `/dev/uinput` 设为 Gruppe `input` 的名称。

### 曼纽尔·雷帕拉图尔：
Falls das Tippen nicht funktioniert, führe folgende Befehle aus:
__代码_块_0__