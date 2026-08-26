# openSUSE le démarrage automatique de XDG

Sur openSUSE, le mécanisme de démarrage automatique XDG est le même que sur Mint — `~/.config/autostart/` — donc aucun concept distinct comme les LaunchAgents de macOS n'est nécessaire ici.

## environnement de bureau

La différence réside dans l'environnement de bureau : le bureau par défaut/phare d'openSUSE est en fait **KDE Plasma** (contrairement à Mint), donc l'approche basée sur la « konsole » de votre documentation d'origine est beaucoup plus susceptible de fonctionner telle quelle. openSUSE propose également une édition GNOME, je vais donc vous proposer les deux variantes ainsi qu'une option sans terminal qui fonctionne quel que soit le bureau.

**Tout d'abord, confirmez le chemin du script** (ajustez `linus` si la machine SUSE utilise un nom d'utilisateur différent) :

### trouver

```bash
find /home/*/SL5-aura-service -iname "restart_venv_and_run-server.sh"
```

### Plasma KDE

**Option A — KDE Plasma** (bureau par défaut d'openSUSE) :

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

### Édition GNOME d'openSUSE

**Option B — Édition GNOME d'openSUSE :** échangez simplement la ligne `Exec`, car `konsole` n'est généralement pas installé sur GNOME :

```bash
Exec=gnome-terminal -- bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "Aura is already running."; else mkdir -p /tmp/sl5_aura && touch /tmp/sl5_aura/sl5net_aura_project_root; /home/linus/SL5-aura-service/scripts/restart_venv_and_run-server.sh; fi; exec bash'
```

### aucun terminal visible

**Option C — Recommandée : aucun terminal visible, arrière-plan + journal** (fonctionne de manière identique sur Plasma, GNOME, Xfce, peu importe — évite toute la question "quel terminal est installé", identique à la variante robuste que je vous ai donnée pour Mint) :

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

## Vérifiez le journal

Vérifiez le journal plus tard avec :

```bash
tail -f /home/linus/SL5-aura-service/aura_engine.log
```

**Testez sans vous déconnecter :** exécutez d'abord la partie `bash -c '...'` manuellement dans un terminal pour confirmer qu'il démarre réellement le service, puis déconnectez-vous/connectez-vous pour vérifier le véritable déclencheur de démarrage automatique. Les paramètres système d'openSUSE (Plasma : *Autostart* ; GNOME : *Startup Applications* via `gnome-tweaks`) répertorieront également cette entrée par la suite si vous souhaitez la basculer depuis l'interface graphique.