# Hooks du cycle de vie des plugins

Aura SL5 prend en charge les hooks de cycle de vie qui permettent aux plugins (Maps) d'exécuter automatiquement une logique spécifique lorsque leur état change.

## Le crochet `on_reload()`

La fonction `on_reload()` est une fonction facultative spéciale que vous pouvez définir dans n'importe quelle Plugin Map (`.py`).

### Comportement
* **Déclencheur :** Cette fonction est exécutée **immédiatement après** le rechargement à chaud réussi du module (changement de fichier détecté + déclencheur vocal).
* **Contexte :** Il s'exécute dans le flux d'application principal.
* **Portée :** Il n'est **PAS** exécuté lors du démarrage initial du système (démarrage à froid). C'est strictement pour les scénarios de *re*-chargement.

### Cas d'utilisation
* **Sécurité :** Rechiffrez ou recompressez automatiquement les fichiers sensibles après l'édition.
* **Gestion de l'état :** Réinitialisation des compteurs globaux ou effacement des caches spécifiques.
* **Notification :** Enregistrement des informations de débogage spécifiques pour vérifier qu'une modification a été appliquée.

### Détails techniques et sécurité
* **Gestion des erreurs :** L'exécution est enveloppée dans un bloc `try/sauf`. Si votre fonction `on_reload` plante (par exemple, `DivisionByZero`), elle enregistrera une erreur (`❌ Erreur d'exécution de on_reload...`) mais **ne fera pas planter Aura**.
* **Performance :** La fonction s'exécute de manière synchrone. Évitez les tâches de longue durée (comme les téléchargements volumineux) directement dans cette fonction, car elles bloqueraient brièvement le traitement des commandes vocales. Pour les tâches lourdes, créez un fil de discussion.

### Exemple de code

__CODE_BLOCK_0__