Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche para:



aura_engine.log.desktop  

Gehe in den Ordner: `~/.config/autostart/`

desligado no Editor

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl Manuel Anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

[Entrada na área de trabalho]
Comentário[pt_GB]=
Comentário =
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; então echo "aura já está em execução."; senão toque em /tmp/sl5_aura/sl5net_aura_project_root; /home/......../projects/py/STT/scripts/restart_venv_and_run-server.sh; fi; executivo zsh'
Nome genérico[en_GB]=
Nome genérico =
Ícone = texto-x-log
MimeType =
Nome[pt_BR]=aura_engine
Nome=aura_engine
Caminho=
StartupNotify = verdadeiro
Terminal=falso
Tipo=Aplicativo
X-KDE-AutostartScript=true
X-KDE-SubstituteUID=falso
X-KDE-Nome de usuário=


### Warum hat die grafische Einstellung nicht funktioniert?

No Plasma 6, o problema é resolvido com o ajuste dos "terminais padrão" na fase inicial do sistema. Indem wir `konsole` (das Standard-Terminal von KDE) direkt in die `Exec`-Zeile schreiben, umgehen wir die automatische Erkennung und erzwingen den Start.


26.3.'26 08:16 Qui