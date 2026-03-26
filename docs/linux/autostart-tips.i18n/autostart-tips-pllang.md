Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

Wpisz polecenie: `~/.config/autostart/`

öffne w edytorze

restart_venv_and_run-server.sh.desktop  ✔
aura_engine.log.desktop  

Den Befehl Manuell Anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Schemat:**
`Exec=konsole --noclose -e /pfad/zu/deinem/script.sh`

bez.

`Exec=kate /pfad/zu/deinem/script.sh`


### Warum hat die grafische Einstellung nicht funktioniert?

W Plazmie 6 gibt es gelegentlich Probleme mit der Zuweisung des „Default Terminals” w Startphase des Systems. Użyj `konsole` (das Standard-Terminal von KDE) bezpośrednio w `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Czw