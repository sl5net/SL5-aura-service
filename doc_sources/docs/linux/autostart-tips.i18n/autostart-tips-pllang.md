Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Wpisz polecenie: `~/.config/autostart/`

öffne w edytorze

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl Manuell Anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

[Wpis na pulpicie]
Komentarz[en_GB]=
Komentarz=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; następnie powtórz „aura już działa.”; w przeciwnym razie dotknij /tmp/sl5_aura/sl5net_aura_project_root; /home/....../projects/py/STT/scripts/restart_venv_and_run-server.sh; fi; wykonanie zsh'
Nazwa ogólna[en_GB]=
Nazwa ogólna=
Ikona=tekst-x-log
Typ MIME=
Nazwa[en_GB]=aura_engine
Nazwa=aura_engine
Ścieżka=
StartupNotify=true
Terminal=fałsz
Typ=Zastosowanie
X-KDE-AutostartScript=true
X-KDE-SubstituteUID=false
Nazwa użytkownika X-KDE=


### Warum hat die grafische Einstellung nicht funktioniert?

W Plazmie 6 gibt es gelegentlich Probleme mit der Zuweisung des „Default Terminals” w Startphase des Systems. Użyj `konsole` (das Standard-Terminal von KDE) bezpośrednio w `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Czw