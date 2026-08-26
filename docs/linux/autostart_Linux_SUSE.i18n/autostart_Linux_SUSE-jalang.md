# openSUSE XDG 自動起動

openSUSE では、XDG 自動起動メカニズムは Mint と同じ (`~/.config/autostart/`) なので、ここでは macOS の LaunchAgents のような別の概念は必要ありません。

## デスクトップ環境

違いはデスクトップ環境です。openSUSE のデフォルト/フラッグシップ デスクトップは実際には **KDE Plasma** (Mint とは異なります) なので、元のドキュメントの「konsole」ベースのアプローチがそのまま機能する可能性が高くなります。 openSUSE は GNOME エディションも提供しているので、両方のバージョンに加えて、デスクトップに関係なく動作するターミナルフリーのオプションを提供します。

**最初に、スクリプト パスを確認します** (SUSE マシンが別のユーザー名を使用している場合は、`linus` を調整します)。

＃＃＃ 探す

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### KDE プラズマ

**オプション A — KDE Plasma** (openSUSE のデフォルトのデスクトップ):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Starts the SL5 Aura Service
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
Icon=text-x-script
Terminal=false
StartupNotify=true
EOF
chmod +x ~/.config/autostart/aura_engine.desktop
```

### openSUSE の GNOME エディション

**オプション B — openSUSE の GNOME 版:** 通常、「konsole」は GNOME にインストールされていないため、「Exec」行を置き換えるだけです。

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### 端子が表示されない

**オプション C — 推奨: 表示されないターミナル、バックグラウンド + ログ** (Plasma、GNOME、Xfce など何でも同様に動作します。Mint 用に提供した堅牢なバリアントと同じように、「どのターミナルがインストールされているか」という質問全体を完全に回避します):

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Starts the SL5 Aura Service in the background
Exec=bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi'
Icon=text-x-script
Terminal=false
StartupNotify=false
EOF
chmod +x ~/.config/autostart/aura_engine.desktop
```

## ログを確認してください

後で次のようにしてログを確認します。

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**ログアウトせずにテストします:** まずターミナルで `bash -c '...'` 部分を手動で実行して実際にサービスが開始されることを確認し、次にログアウト/ログインして実際の自動開始トリガーを確認します。 GUI から切り替える場合は、openSUSE のシステム設定 (Plasma: *Autostart*、GNOME: `gnome-tweaks` 経由の *Startup Applications*) にもこのエントリがリストされます。