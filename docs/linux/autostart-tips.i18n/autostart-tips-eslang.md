Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

Aquí en el orden: `~/.config/autostart/`

öffne en el editor

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Schreibe:**
`Exec=konsole --noclose -e /pfad/zu/deinem/script.sh`

bez.

`Exec=kate /pfad/zu/deinem/script.sh`


### ¿Por qué la instalación gráfica no funciona?

En Plasma 6 hay un problema grave con el cambio de "Terminales predeterminados" en la fase de inicio de los sistemas. También tenemos `console` (el terminal estándar de KDE) directamente en el `Exec`-Zeile schreiben, para activar y desactivar automáticamente el inicio.


26.3.'26 08:16 Jue