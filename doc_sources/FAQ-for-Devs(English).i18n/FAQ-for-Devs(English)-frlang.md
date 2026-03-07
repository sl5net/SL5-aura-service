# règles d'expressions régulières

Important : veuillez appliquer les expressions régulières dans le bon ordre.

Vous devez d'abord utiliser l'expression régulière composite (plus générale), puis appliquer l'expression spécialisée.

La raison en est que si l'expression régulière la plus courte et spécialisée s'exécute en premier, elle peut correspondre à une partie de la chaîne essentielle pour l'expression régulière composite plus grande. Cela rendrait impossible pour l'expression régulière composite de trouver sa correspondance par la suite.
(S. 20.10.'25 18:37 lundi)

#Linux/Mac

si vous souhaitez démarrer automatiquement le service, vous pouvez ajouter :
~/projects/py/STT/scripts/restart_venv_and_run-server.sh
au démarrage automatique.

Démarrez le service uniquement lorsqu'il existe une connexion Internet :
puis défini dans settings_local.py :
SERVICE_START_OPTION = 1


## ajouter entrer
quand vous définissez
config/settings_local.py/AUTO_ENTER_AFTER_DICTATION_REGEX_APPS
à 1, il ajoute enter.

quand vous définissez
tmp/sl5_auto_enter.flag
à 1, il ajoute enter.

tmp/sl5_auto_enter.flag sera écrasé lorsque vous démarrerez le service.
tmp/sl5_auto_enter.flag est peut-être plus facile à analyser pour vous avec d'autres scripts et sa lecture est peut-être un peu plus rapide.

utiliser d'autres numéros pour désactiver
(S. 13.9.'25 16:12 samedi)