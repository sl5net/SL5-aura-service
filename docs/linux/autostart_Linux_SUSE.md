# openSUSE the XDG autostart

On openSUSE the XDG autostart mechanism is the same as on Mint — `~/.config/autostart/` — so no separate concept like macOS's LaunchAgents is needed here.

## desktop environment

The difference is the desktop environment: openSUSE's default/flagship desktop is actually **KDE Plasma** (unlike Mint), so the `konsole`-based approach from your original documentation is much more likely to work as-is. openSUSE also offers a GNOME edition, so I'll give you both variants plus a terminal-free option that works regardless of desktop.

**First, confirm the script path** (adjust `linus` if the SUSE machine uses a different username):

### find

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### KDE Plasma

**Option A — KDE Plasma** (openSUSE's default desktop):

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

### GNOME edition of openSUSE

**Option B — GNOME edition of openSUSE:** just swap the `Exec` line, since `konsole` usually isn't installed on GNOME:

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### no visible terminal

**Option C — Recommended: no visible terminal, background + log** (works identically on Plasma, GNOME, Xfce, whatever — avoids the whole "which terminal is installed" question entirely, same as the robust variant I gave you for Mint):

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

## Check the log

Check the log later with:

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**Test without logging out:** run the `bash -c '...'` part manually in a terminal first to confirm it actually starts the service, then log out/in to verify the real autostart trigger. openSUSE's system settings (Plasma: *Autostart*; GNOME: *Startup Applications* via `gnome-tweaks`) will also list this entry afterward if you want to toggle it from the GUI.

