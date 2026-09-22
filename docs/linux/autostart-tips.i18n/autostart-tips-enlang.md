> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../autostart-tips.md).*


Create Autostart entry from your graphical user interface for:

restart venv and run-server.sh.desktop                          

aura engine.log.desktop  

Go to the folder: `~/.config/autostart/`

Open in Editor

restart venv and run-server.sh.desktop                          
aura engine.log.desktop  

Adjust the command manually

**Instead of:**
`Exec=/pfad/zu/deinem/script.sh`

**Examples Write:**

[Desktop Entry]
Comment[en GB] =
Comments =
Exec=console -e bash -c 'if [ -f /tmp/sl5 aura/sl5net aura project root ]; then echo "aura already runs."; otherwise touch /tmp/sl5 aura/sl5net aura project root; /home/......../projects/py/STT/scripts/restart venv and run-server.sh; fi; exec zsh'
GenericName[en GB] =
GenericName =
Icon=text-x-log
MimeType =
Name[en GB]=aura engine
Name=aura engine
Path=
StartupNotify=true
Terminal=false
Type=Application
X-KDE-AutostartScript=true
X-KDE substituteUID=false
X-KDE username =


### Why didn't the graphics setting work?

In Plasma 6 there are occasional problems with the assignment of the "Default Terminal" during the system startup phase. By writing `konsole` (the default terminal of KDE) directly into the `Exec` line, we bypass the automatic detection and force the startup.


26.3.'26 08:16 Thu
