Crochets Aura SL5 : ajoutés

HOOK_PLUGIN_LOAD = 'on_plugin_load'
HOOK_FILE_LOAD = 'on_file_load'
HOOK_RELOAD = 'on_reload'
HOOK_UPSTREAM = 'on_folder_change'

on_folder_change() et
on_reload() pour déclencher la logique après les rechargements à chaud. Utilisez-le pour « chaîner » l'exécution avec des scripts parents comme secure_packer.py pour les packages complexes.

# Guide du développeur : Hooks du cycle de vie des plugins

Aura SL5 permet aux plugins (Maps) de définir des "Hooks" spécifiques qui s'exécutent automatiquement lorsque l'état du module change. Ceci est essentiel pour les flux de travail avancés tels que le système **Secure Private Map**.

## Le crochet `on_folder_change`

Implémentation de la détection de hook `on_folder_change`. Le rechargeur analyse maintenant le répertoire

## Le hook `on_reload()`

La fonction `on_reload()` est une fonction facultative que vous pouvez définir dans n'importe quel module Map.

### Comportement
* **Trigger :** Exécuté immédiatement après le **rechargement à chaud** réussi d'un module (modification de fichier + déclencheur vocal).
* **Contexte :** S'exécute dans le thread principal de l'application.
* **Sécurité :** Enveloppé dans un bloc `try/sauf`. Les erreurs ici seront enregistrées mais ne feront **pas planter** l'application.

### Modèle d'utilisation : la « daisy chain »
Pour les packages complexes (comme Private Maps), vous avez souvent de nombreux sous-fichiers, mais un seul script central (`secure_packer.py`) doit gérer la logique.

Vous pouvez utiliser le hook pour déléguer la tâche vers le haut :

__CODE_BLOCK_0__