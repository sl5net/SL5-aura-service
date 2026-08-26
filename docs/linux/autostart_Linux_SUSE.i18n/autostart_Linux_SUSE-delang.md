# openSUSE den XDG-Autostart

Unter openSUSE ist der XDG-Autostart-Mechanismus derselbe wie unter Mint – „~/.config/autostart/“ – daher ist hier kein separates Konzept wie die LaunchAgents von macOS erforderlich.

## Desktop-Umgebung

Der Unterschied liegt in der Desktop-Umgebung: Der Standard-/Flaggschiff-Desktop von openSUSE ist tatsächlich **KDE Plasma** (im Gegensatz zu Mint), daher ist es viel wahrscheinlicher, dass der „konsole“-basierte Ansatz aus Ihrer Originaldokumentation so funktioniert, wie er ist. openSUSE bietet auch eine GNOME-Edition an, daher gebe ich Ihnen beide Varianten plus eine terminalfreie Option, die unabhängig vom Desktop funktioniert.

**Bestätigen Sie zunächst den Skriptpfad** (passen Sie „linus“ an, wenn die SUSE-Maschine einen anderen Benutzernamen verwendet):

### finden

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### KDE-Plasma

**Option A – KDE Plasma** (Standard-Desktop von openSUSE):

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

### GNOME-Edition von openSUSE

**Option B – GNOME-Edition von openSUSE:** Tauschen Sie einfach die Zeile „Exec“ aus, da „konsole“ normalerweise nicht auf GNOME installiert ist:

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### kein sichtbares Terminal

**Option C – Empfohlen: kein sichtbares Terminal, Hintergrund + Protokoll** (funktioniert identisch auf Plasma, GNOME,

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

## Überprüfen Sie das Protokoll

Überprüfen Sie das Protokoll später mit:

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**Test ohne Abmelden:** Führen Sie den Teil „bash -c '...'“ zuerst manuell in einem Terminal aus, um zu bestätigen, dass der Dienst tatsächlich gestartet wird, und melden Sie sich dann ab/an, um den tatsächlichen Autostart-Auslöser zu überprüfen. In den Systemeinstellungen von openSUSE (Plasma: *Autostart*; GNOME: *Startanwendungen* über „gnome-tweaks“) wird dieser Eintrag anschließend ebenfalls aufgeführt, wenn Sie ihn über die GUI umschalten möchten.