## 文本输入法配置

### Voraussetzungen für `dotool` (schneller als xdotool)

1. 安装：`pamac build dotool` 或 `yay -S dotool`
2.用户zur输入-Gruppe hinzufügen：`sudo gpasswd -a $USER input`
3. udev-Regel erstellen：
__代码_块_0__
4.重新启动：`sudo udevadm control --reload-rules && sudo udevadm trigger`
5. **新einloggen**

### 配置

在`config/settings.py`中：
__代码_块_1__

### 警告

- `dotool` ist deutlich schneller als `xdotool` – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- 在导入时使用“settings.py”打印所有设置 – das ist gewollt
- Der dotool-Listener läuft als Hintergrundprozess über ein FIFO (`/tmp/dotool_fifo`) mit `typedelay 0`

---