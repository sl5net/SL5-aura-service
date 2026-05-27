Erstelle Autostart Eintrag über deine grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Gehe in den Ordner: `~/.config/autostart/`

öffne im Editor

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

[Desktop Entry]
Comment[en_GB]=
Comment=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; then echo "aura already runs."; else touch /tmp/sl5_aura/sl5net_aura_project_root; /home/......../projects/py/STT/scripts/restart_venv_and_run-server.sh; fi; exec zsh'
GenericName[en_GB]=
GenericName=
Icon=text-x-log
MimeType=
Name[en_GB]=aura_engine
Name=aura_engine
Path=
StartupNotify=true
Terminal=false
Type=Application
X-KDE-AutostartScript=true
X-KDE-SubstituteUID=false
X-KDE-Username=


### Warum hat die grafische Einstellung nicht funktioniert?

In Plasma 6 gibt es gelegentlich Probleme mit der Zuweisung des „Default Terminals“ in der Startphase des Systems. Indem wir die „Konsole“ (das Standard-Terminal von KDE) direkt in die „Exec“-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Do
