Erstelle Autostart Eintrag über dein grafische Benutzeroberfläche für:

reiniciar_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Aquí en el orden: `~/.config/autostart/`

öffne en el editor

reiniciar_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstatt:**
`Exec=/pfad/zu/deinem/script.sh`

**Beispiele Schreibe:**

[Entrada de escritorio]
Comentario[en_GB]=
Comentario=
Exec=konsole -e bash -c 'if [ -f /tmp/sl5_aura/sl5net_aura_project_root ]; luego repite "el aura ya corre."; de lo contrario, toque /tmp/sl5_aura/sl5net_aura_project_root; /home/......./projects/py/STT/scripts/restart_venv_and_run-server.sh; fi; ejecutivo zsh'
NombreGenérico[en_GB]=
Nombre genérico=
Icono=texto-x-log
Tipo Mime=
Nombre[en_GB]=aura_engine
Nombre=aura_motor
Ruta =
Notificación de inicio = verdadero
Terminal=falso
Tipo=Aplicación
X-KDE-AutostartScript=verdadero
X-KDE-SubstituteUID=falso
X-KDE-nombre de usuario=


### ¿Por qué la instalación gráfica no funciona?

En Plasma 6 hay un problema grave con el cambio de "Terminales predeterminados" en la fase de inicio de los sistemas. También tenemos `console` (el terminal estándar de KDE) directamente en el `Exec`-Zeile schreiben, para activar y desactivar automáticamente el inicio.


26.3.'26 08:16 Jue