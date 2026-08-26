#Linux menta

## con ventana de terminal

```bash

mkdir -p ~/.config/autostart
cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Startet den SL5 Aura Service
Exec=x-terminal-emulator -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura läuft bereits."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
Icon=text-x-script
Terminal=false
StartupNotify=true
X-GNOME-Autostart-enabled=true
EOF
chmod +x ~/.config/autostart/aura_engine.desktop

```

## sin ventana de terminal

```bash

cat > ~/.config/autostart/aura_engine.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=aura_engine
Comment=Startet den SL5 Aura Service im Hintergrund
Exec=bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then exit 0; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh >> /home/linus/SL5-aura-service/aura_engine.log 2>&1; fi'
Icon=text-x-script
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

```