# XDG 자동 시작을 openSUSE합니다.

openSUSE에서 XDG 자동 시작 메커니즘은 Mint(`~/.config/autostart/`)와 동일하므로 여기서는 macOS의 LaunchAgents와 같은 별도의 개념이 필요하지 않습니다.

## 데스크탑 환경

차이점은 데스크톱 환경입니다. openSUSE의 기본/플래그십 데스크톱은 실제로 **KDE Plasma**(Mint와는 다름)이므로 원본 문서의 `konsole` 기반 접근 방식이 있는 그대로 작동할 가능성이 훨씬 더 높습니다. openSUSE는 GNOME 에디션도 제공하므로 두 가지 변형과 데스크톱에 관계없이 작동하는 터미널 없는 옵션을 제공하겠습니다.

**먼저 스크립트 경로를 확인하세요**(SUSE 시스템이 다른 사용자 이름을 사용하는 경우 `linus`를 조정하세요):

### 찾다

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### KDE 플라즈마

**옵션 A — KDE 플라즈마**(openSUSE의 기본 데스크탑):

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

### openSUSE의 그놈 에디션

**옵션 B — openSUSE의 GNOME 버전:** `konsole`은 일반적으로 GNOME에 설치되지 않으므로 `Exec` 줄을 바꾸세요.

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### 보이는 터미널이 없습니다

**옵션 C — 권장 사항: 눈에 보이는 터미널 없음, 배경 + 로그** (Plasma, GNOME, Xfce 등에서 동일하게 작동합니다. "어떤 터미널이 설치되어 있는지"라는 질문을 완전히 피합니다. Mint에 대해 제공한 강력한 변형과 동일합니다):

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

## 로그를 확인하세요

나중에 다음을 사용하여 로그를 확인하세요.

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**로그아웃하지 않고 테스트:** 먼저 터미널에서 `bash -c '...'` 부분을 수동으로 실행하여 실제로 서비스가 시작되는지 확인한 다음 로그아웃/로그인하여 실제 자동 시작 트리거를 확인합니다. GUI에서 전환하려는 경우 openSUSE의 시스템 설정(플라즈마: *Autostart*; GNOME: `gnome-tweaks`를 통한 *시작 응용 프로그램*)에도 이 항목이 나열됩니다.