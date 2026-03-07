# dotool – 安装和配置 (Manjaro / Arch-basiert)

## 是 dotool 吗？

`dotool` 是 Linux 下的模拟工具。
这是 X11 中的“xdotool”和功能的德语 schneller 和 Wayland。

---

## 安装（Manjaro / Arch）

### 1. 包安装

__代码_块_0__

### 2. 用户 zur `input`-Gruppe hinzufügen

__代码_块_1__

### 3.udev-Regel erstellen

__代码_块_2__

### 4.udev 新拉登

__代码_块_3__

### 5. Neu einloggen（wichtig！）

Ohne Neu-Login 不支持 Gruppenzugehörigkeit。

---

## 项目配置

### `config/settings.py`

__代码_块_4__

---

## Wie das Skript dotool verwendet

### Eingabe-Funktion

__代码_块_5__

### 配置 auslesen (ohne Seiteneffekte)

设置 werden so ausgelesen，dass `print()`-Ausgaben in `settings.py`
den Wert nicht verfälschen:

__代码_块_6__

---

## 说明

- **变音和特殊设置：** `类型延迟 2`（执行工具默认） ist empfohlen。
Bei `typedelay 0` können Zeichen wie ä, ö, ü, ß verloren gehen。
- **Zu schnell für die Zielanwendung？** Manche Apps（z. B. Electron，浏览器输入）
Verlieren Zeichen bei niedrigem 延迟。在 diesem Fall `dotool_typedelay = 5` 或 höher verwenden 中。
- **Wayland：** 在 Wayland 上执行 dotool 功能，xdotool 不可用。
- **后备：** Wenn dotool nicht installiert ist，fällt das Skript automatisch auf `xdotool` zurück。
---

## Wie das Skript dotool verwendet

Das Skript startet einen permanenten `dotool`-Prozess über ein FIFO,
um den Overhead eines neuen Prozesses bei jedem Tastendruck zu vermeiden。

### 相关代码(`type_watcher.sh`)

__代码_块_7__

### Eingabe-Funktion

__代码_块_8__

### 配置 auslesen (ohne Seiteneffekte)

设置 werden so ausgelesen，dass `print()`-Ausgaben in `settings.py`
den Wert nicht verfälschen:

__代码_块_9__

---

## 说明

- **Zu schnell für die Zielanwendung？** Manche Apps（z. B. Electron，浏览器输入）
verlieren Zeichen bei `typedelay 0`。在秋季`typedelay 5`或`typedelay 10`版本中。
- **Wayland：** 在 Wayland 上执行 dotool 功能，xdotool 不可用。
- **后备：** Wenn dotool nicht installiert ist，fällt das Skript automatisch auf `xdotool` zurück。