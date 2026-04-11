# dotool on Wayland — セットアップとトラブルシューティング

Aura が Wayland 上の他のアプリケーションにテキストを入力するには、`dotool` が必要です。
「xdotool」とは異なり、「uinput」を介してLinuxカーネルと直接通信します。
**X11 と Wayland** の両方で動作します。

X11 では、デフォルトで `xdotool` が使用されます。 `dotool` は X11 ではオプションですが、
レイアウトの安定性を高めるために推奨されます (特にウムラウトの場合)。

---

## 1. dotool をインストールします

**Arch / Manjaro / CachyOS (AUR):**
```bash
yay -S dotool
# or:
pamac build dotool
```

**Ubuntu / Debian (リポジトリで利用可能な場合):**
```bash
sudo apt install dotool
```

**リポジトリにない場合は、ソースからビルドします:**
```bash
sudo pacman -S go        # or: sudo apt install golang
git clone https://git.sr.ht/~geb/dotool
cd dotool
make
sudo make install
```

---

## 2. root なしで dotool を実行できるようにします (必須)

`dotool` は `/dev/uinput` にアクセスする必要があります。これがないと、静かに失敗します。

```bash
# Add your user to the input group:
sudo gpasswd -a $USER input

# Create the udev rule:
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules

# Reload rules:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

グループの変更を有効にするには、**再ログインが必要です**。

---

## 3. インストールを確認します

```bash
# Test that dotool can type (focus a text field first):
echo "type hello" | dotool

# Check that the input group is active in your session:
groups | grep input
```

「groups」に「input」が表示されない場合は、ログアウトして再度ログイン (または再起動) してください。

---

## 4. Aura が dotool を使用する方法

Aura の `type_watcher.sh` は自動的に次のようになります。

- `$WAYLAND_DISPLAY` 経由で Wayland を検出し、`dotool` を選択します
- `dotoold` デーモンが存在していて実行されていない場合は、バックグラウンドで起動します。
- `dotool` がインストールされていない場合は `xdotool` にフォールバックします (X11 のみ)
- アクティブな Vosk モデルからキーボード レイアウトを設定します (例: `de` → `XKB_DEFAULT_LAYOUT=de`)

手動のデーモン管理は必要ありません。Aura が起動時にこれを処理します。

---

## 5. トラブルシューティング

**Aura は文字化しますが、テキストは表示されません:**
```bash
# Check if dotool is installed:
command -v dotool

# Check group membership:
groups | grep input

# Test manually (focus a text field first):
echo "type hello" | dotool

# Check the watcher log:
tail -30 log/type_watcher.log
```

**文字の欠落または文字化け (特にウムラウト文字):**

`config/settings_local.py` の入力遅延を増やします。
```python
dotool_typedelay = 5   # default is 2, try 5 or 10
```

**dotool はターミナルでは動作しますが、Aura では動作しません:**

「input」グループがデスクトップ セッション (新しい端末だけでなく) でアクティブであることを確認します。
「gpasswd」の後に完全な再ログインが必要です。

**X11 で dotool を強制します** (レイアウトの安定性を向上させるためのオプション):
```python
# config/settings_local.py
x11_input_method_OVERRIDE = "dotool"
```

---

## 6. dotool をインストールできない場合のフォールバック

システムで「dotool」が使用できない場合、Aura は X11 の「xdotool」にフォールバックします。
「dotool」のない Wayland では、入力は **サポートされていません** - これは Wayland です
Aura の制限ではなく、セキュリティの制限です。

特定のコンポジターで動作する可能性のある代替ツール:

|ツール |作品 |
|---|---|
| `xdotool` | X11のみ |
| `dotool` | X11 + Wayland (推奨) |
| `ydotool` | X11 + Wayland (代替) |

手動の回避策として「ydotool」を使用するには:
```bash
sudo pacman -S ydotool    # or: sudo apt install ydotool
sudo systemctl enable --now ydotool
```
注: Aura は「ydotool」をネイティブに統合しません。手動設定が必要です。