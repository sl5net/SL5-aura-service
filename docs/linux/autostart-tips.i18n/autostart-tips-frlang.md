Première introduction de démarrage automatique à partir des indications graphiques pour :

restart_venv_and_run-server.sh.desktop   

aura_engine.log.desktop  

Voir dans l'ordre : `~/.config/autostart/`

öffne dans l'éditeur

restart_venv_and_run-server.sh.desktop   
aura_engine.log.desktop  

Den Befehl manuell anpassen

**Anstat:**
`Exec=/pfad/zu/deinem/script.sh`

**Voir les exemples :**

Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'

`Exec=xfce4-terminal -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'`

Exec=konsole -e 'bash -c "/home/seeh/projects/py/STT/scripts/restart_venv_and_run-server.sh && bash"'   

Exec=Exec=kate /home/me/projects/py/STT/log/aura_engine.log

Exec=kate /home/me/projects/py/STT/config/filters/settings_local_log_filter.py





### Pourquoi l'installation graphique n'est-elle pas fonctionnelle ?

Dans Plasma 6, il existe un problème récurrent avec la configuration des "terminaux par défaut" lors de la phase de démarrage des systèmes. Nous avons une « console » (du terminal standard de KDE) directement dans la zone « Exec », puis la configuration et le démarrage automatiques du démarrage.


26.3.'26 08:16 jeu.