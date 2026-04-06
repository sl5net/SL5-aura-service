# Premiers pas sous Windows

## Étape 1 : Exécutez le programme d'installation
Double-cliquez sur `setup/windows11_setup_with_ahk_copyq.bat`.
- Faites un clic droit → "Exécuter en tant qu'administrateur" si vous y êtes invité.
- Le script installe Python, AutoHotkey v2, CopyQ et télécharge les modèles vocaux (~ 4 Go).
- Cela prend environ 8 à 10 minutes.

## Étape 2 : Démarrer Aura
Double-cliquez sur `start_aura.bat` dans le dossier du projet.
Vous devriez entendre un son de démarrage : Aura est prête.

**Rien ne s'est passé ?** Vérifiez le journal :
log\aura_engine.log

## Étape 3 : Configurez votre raccourci clavier
Le programme d'installation installe CopyQ automatiquement. Pour déclencher une dictée :
1. Ouvrez CopyQ → Commandes → Ajouter une commande
2. Définissez la commande sur :
cmd /c écho. > C:\tmp\sl5_record.trigger
3. Attribuez un raccourci global (par exemple « F9 »)

## Étape 4 : Première dictée
1. Cliquez dans n'importe quel champ de texte
2. Appuyez sur votre touche de raccourci - attendez la notification "Écoute..."
3. Dites « Bonjour tout le monde »
4. Appuyez à nouveau sur la touche de raccourci - le texte apparaît

## Étape 5 : Rechercher des commandes vocales
Dites : **"Aura Search"** — une fenêtre s'ouvre avec toutes les règles disponibles.

## Dépannage
| Symptôme | Corriger |
|---|---|
| Aucun son de démarrage | Vérifiez `log\aura_engine.log` |
| Le raccourci clavier ne fait rien | Vérifiez si `C:\tmp\sl5_record.trigger` est créé |
| Texte non saisi | Vérifiez si `type_watcher.ahk` est en cours d'exécution dans le Gestionnaire des tâches |
| Crash au démarrage | Exécutez à nouveau l'installation en tant qu'administrateur |

> Dépannage complet : [TROUBLESHOOTING.md](../../TROUBLESHOOTING.i18n/TROUBLESHOOTING-frlang.md)