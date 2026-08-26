# openSUSE el inicio automático de XDG

En openSUSE, el mecanismo de inicio automático de XDG es el mismo que en Mint: `~/.config/autostart/`, por lo que aquí no se necesita ningún concepto separado como LaunchAgents de macOS.

## entorno de escritorio

La diferencia es el entorno de escritorio: el escritorio insignia/predeterminado de openSUSE es en realidad **KDE Plasma** (a diferencia de Mint), por lo que es mucho más probable que el enfoque basado en `konsole` de su documentación original funcione tal como está. openSUSE también ofrece una edición de GNOME, por lo que le brindaré ambas variantes más una opción sin terminal que funciona independientemente del escritorio.

**Primero, confirme la ruta del script** (ajuste `linus` si la máquina SUSE usa un nombre de usuario diferente):

### encontrar

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### Plasma KDE

**Opción A — KDE Plasma** (escritorio predeterminado de openSUSE):

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

### Edición GNOME de openSUSE

**Opción B — Edición GNOME de openSUSE:** simplemente intercambie la línea `Exec`, ya que `konsole` generalmente no está instalado en GNOME:

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### sin terminal visible

**Opción C: recomendada: sin terminal visible, fondo + registro** (funciona de manera idéntica en Plasma, GNOME, Xfce, lo que sea; evita por completo la pregunta de "qué terminal está instalado", igual que la variante robusta que le di para Mint):

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

## Verifique el registro

Consulte el registro más tarde con:

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**Prueba sin cerrar sesión:** primero ejecute la parte `bash -c '...'` manualmente en una terminal para confirmar que realmente inicia el servicio, luego cierre/inicie sesión para verificar el disparador de inicio automático real. La configuración del sistema de openSUSE (Plasma: *Autostart*; GNOME: *Startup Applications* vía `gnome-tweaks`) también incluirá esta entrada después si desea alternarla desde la GUI.