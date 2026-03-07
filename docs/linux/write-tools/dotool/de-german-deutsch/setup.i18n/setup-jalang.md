## テキスト入力メソッドの構成

### Voraussetzungen für `dotool` (schneller als xdotool)

1. インストール: `pamac build dotool` または `yay -S dotool`
2. ユーザー入力グループ: `sudo gpasswd -a $USER input`
3. udev-Regel erstellen:
   ```bash
   echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' | sudo tee /etc/udev/rules.d/80-dotool.rules
   ```
4. 詳しい説明: `sudo udevadm control --reload-rules && sudo udevadm Trigger`
5. **ノイ アインロッゲン**

### 設定

`config/settings.py` 内:
```python
x11_input_method_OVERRIDE = "dotool"  # oder "xdotool"
```

### ヒンヴァイゼ

- `dotool` ist deutlich Schneller als `xdotool` – bei sehr Schhneller Ausgabe kann es sein, dass die Zielanwendung Zeichen verliert
- 輸入品を印刷するための設定を表示する – das ist gewollt
- dotool-Listener は、FIFO (`/tmp/dotool_fifo`) mit `typelay 0` を使用して Hintergrundprozess を実行します

---