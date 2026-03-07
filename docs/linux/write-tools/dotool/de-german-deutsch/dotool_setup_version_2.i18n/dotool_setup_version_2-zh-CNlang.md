### Teil 1：德国文献

# dotool – 安装和配置 (Manjaro / Arch-basiert)

## 是 dotool 吗？
`dotool` 是 Tastatureingaben 的 Werkzeug zur 模拟。我通过“uinput”和“xdotool”命令直接与内核进行交互，并在 **X11 和 Wayland** 下进行操作。

---

## 安装（Manjaro / Arch）

### 1. 包安装
__代码_块_0__

### 2. 准备就绪
Damit `dotool` ohne Root-Rechte titpen darf，muss dein User in die Gruppe `input` 和 eine udev-Regel aktiv sein：

1. **用户 zur Gruppe:** `sudo gpasswd -a $USER input`
2. **udev-Regel：**
__代码_块_1__
3. **重新加载：**
__代码_块_2__

**维希蒂格：** Danach einmal **aus- und neu einloggen**，damit die Gruppenrechte aktiv werden。

---

## 项目配置 (`config/settings.py`)

__代码_块_3__

---

## 在 Skript 中实现

### 持久化进程（先进先出）
Um den Overhead durch ständiges Neuerstellen des beautyllen zu vermeiden，nutzt das Skript eine Pipe (FIFO)。 Dadurch reagiert `dotool` verzögerungsfrei。

__代码_块_4__

### Die Eingabe-Funktion
__代码_块_5__

---

## 说明和说明
- **Fehlende Zeichen：** Wenn Umlaute verschluckt werden，erhöhe `dotool_typedelay` auf 5 oder 10。
- **后备：** ist `dotool` nicht korrekt konfiguriert，weicht das System automatisch auf `xdotool` aus。
- **Wayland 支持：** 在 Wayland 中，“dotool”自动运行，“xdotool”不具有任何功能。