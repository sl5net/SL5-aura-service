## 텍스트 입력 방법 구성

### Voraussetzungen für `dotool`(schneller als xdotool)

1. 설치 방법: `pamac build dotool` 또는 `yay -S dotool`
2. 사용자 zur input-Gruppe Hinzufügen: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. Regeln neu laden: `sudo udevadm control --reload-rules && sudo udevadm Trigger`
5. **뉴 아인로그겐**

### 구성

`config/settings.py`에서:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### 힌와이즈

- `dotool`은 `xdotool`과 같은 deutlich schneller입니다 – bei sehr schneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- Das Auslesen der Settings unterdrückt bewusst alle Print-Ausgaben aus `settings.py` während des Imports – das ist gewollt
- Der dotool-Listener läuft als Hintergrundprozess über ein FIFO(`/tmp/dotool_fifo`) mit `typedelay 0`

---