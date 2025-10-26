## Pleins feux sur les fonctionnalités : implémentation d'un mode de traduction en direct commutable

Notre framework d'assistant vocal plug-in est conçu pour une flexibilité maximale. Ce guide présente une fonctionnalité puissante : un mode de traduction en direct qui peut être activé et désactivé avec une simple commande vocale. Imaginez parler à votre assistant en allemand et entendre le résultat en portugais, puis revenir instantanément à un comportement normal.

Ceci n'est pas réalisé en modifiant le moteur principal, mais en manipulant intelligemment le fichier de configuration des règles lui-même.

### Comment l'utiliser

Cette configuration implique d'ajouter deux règles à votre fichier `FUZZY_MAP_pre.py` et de créer les scripts correspondants.

**1. La règle Toggle :** Cette règle écoute la commande pour activer ou désactiver le mode de traduction.

```python
# Rule to turn the translation mode on or off
    ('', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|einschalten|deaktivieren|ausschalten|toggle|Dogge|doppelt)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
```
Lorsque vous dites « Übersetzung einschalten » (Activer la traduction), le script `toggle_translation_mode.py` est exécuté.

**2. La règle de traduction :** Il s'agit d'une règle « fourre-tout » qui, lorsqu'elle est active, correspond à n'importe quel texte et l'envoie au script de traduction.

```python
    # ANCHOR: The following line is controlled by the toggle script.
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_german_to_portuguese.py']}),
```
La clé ici est le commentaire `# TRANSLATION_RULE`. Cela agit comme une « ancre » que le script à bascule utilise pour rechercher et modifier la règle en dessous.

### Comment ça marche : la magie derrière le rideau

Au lieu d'utiliser un état interne, cette méthode modifie directement la mappe de règles sur le système de fichiers. Le script `toggle_translation_mode.py` fait office de gestionnaire de configuration.

1. **Trouver la règle :** Lorsqu'il est déclenché, le script lit le contenu de `FUZZY_MAP_pre.py`. Il recherche le commentaire d'ancrage unique `# TRANSLATION_RULE`.

2. **Basculer l'état :**
* **Pour désactiver :** Si la ligne de règle située sous l'ancre est active, le script ajoute un « # » au début de la ligne, la commentant et la désactivant efficacement.
* **Pour activer :** Si la ligne de règle est déjà commentée, le script supprime soigneusement le « # » initial, réactivant ainsi la règle.

3. **Enregistrer et recharger :** Le script enregistre le contenu modifié dans `FUZZY_MAP_pre.py`. Il crée ensuite un fichier de déclenchement spécial (par exemple, `RELOAD_RULES.trigger`). Le service principal surveille constamment ce fichier déclencheur. Lorsqu'il apparaît, le service sait que sa configuration a changé et recharge l'intégralité de la carte de règles à partir du disque, appliquant ainsi la modification instantanément.

### Philosophie de conception : avantages et considérations

Cette approche consistant à modifier directement le fichier de configuration a été choisie pour sa clarté et sa simplicité pour l'utilisateur final.

#### Avantages :

* **Haute transparence :** L'état actuel du système est toujours visible. Un rapide coup d'œil au fichier `FUZZY_MAP_pre.py` révèle immédiatement si la règle de traduction est active ou commentée.
* **Aucune modification du moteur principal :** Cette fonctionnalité puissante a été implémentée sans modifier une seule ligne du moteur principal de traitement des règles. Cela démontre la flexibilité du système de plugins.
* **Intuitif pour les développeurs :** Le concept d'activation ou de désactivation d'un élément de configuration en le commentant est un modèle familier, simple et fiable pour quiconque a travaillé avec du code ou des fichiers de configuration.

#### Considérations :

* **Autorisations du système de fichiers :** Pour que cette méthode fonctionne, le processus de l'assistant doit disposer d'autorisations en écriture sur ses propres fichiers de configuration. Dans certains environnements de haute sécurité, cela peut être une considération.