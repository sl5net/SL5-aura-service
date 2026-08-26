# openSUSE a inicialização automática do XDG

No openSUSE, o mecanismo de inicialização automática do XDG é o mesmo do Mint — `~/.config/autostart/` — portanto, nenhum conceito separado como o LaunchAgents do macOS é necessário aqui.

## ambiente de área de trabalho

A diferença é o ambiente de desktop: o desktop padrão/principal do openSUSE é na verdade o **KDE Plasma** (ao contrário do Mint), então a abordagem baseada no `konsole` da sua documentação original tem muito mais probabilidade de funcionar como está. O openSUSE também oferece uma edição GNOME, então darei a você ambas as variantes, além de uma opção sem terminal que funciona independentemente do desktop.

**Primeiro, confirme o caminho do script** (ajuste `linus` se a máquina SUSE usar um nome de usuário diferente):

### encontrar

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### Plasma KDE

**Opção A — KDE Plasma** (área de trabalho padrão do openSUSE):

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

### Edição GNOME do openSUSE

**Opção B — Edição GNOME do openSUSE:** apenas troque a linha `Exec`, já que o `konsole` normalmente não é instalado no GNOME:

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### nenhum terminal visível

**Opção C - Recomendado: nenhum terminal visível, plano de fundo + log ** (funciona de forma idêntica no Plasma, GNOME, Xfce, qualquer que seja - evita toda a questão "qual terminal está instalado", igual à variante robusta que dei a você para o Mint):

__CODE_BLOCO_3__

## Verifique o registro

Verifique o log mais tarde com:

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

**Teste sem efetuar logout:** execute a parte `bash -c '...'` manualmente em um terminal primeiro para confirmar se ele realmente inicia o serviço e, em seguida, efetue logout/in para verificar o verdadeiro gatilho de inicialização automática. As configurações do sistema do openSUSE (Plasma: *Autostart*; GNOME: *Startup Applications* via `gnome-tweaks`) também listarão esta entrada posteriormente se você quiser alterná-la na GUI.