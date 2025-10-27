## Création de nouveaux modules de plugin

Notre framework utilise un puissant système de découverte automatique pour charger les modules de règles. Cela rend l'ajout de nouveaux ensembles de commandes simple et propre, sans avoir besoin d'enregistrer manuellement chaque nouveau composant. Ce guide explique comment créer, structurer et gérer vos propres modules personnalisés.

### Le concept de base : les modules basés sur des dossiers

Un module est simplement un dossier dans le répertoire `config/maps/`. Le système analyse automatiquement ce répertoire et traite chaque sous-dossier comme un module chargeable.

### Guide étape par étape pour créer un module

Suivez ces étapes pour créer un nouveau module, par exemple pour contenir les macros d'un jeu spécifique.

**1. Accédez au répertoire Maps**
Tous les modules de règles résident dans le dossier `config/maps/` du projet.

**2. Créez votre dossier de module**
Créez un nouveau dossier. Le nom doit être descriptif et utiliser des traits de soulignement au lieu d'espaces (par exemple, `my_game_macros`, `custom_home_automation`).

**3. Ajouter des sous-dossiers de langue (étape critique)**
Dans votre nouveau dossier de module, vous devez créer des sous-dossiers pour chaque langue que vous souhaitez prendre en charge.

* **Convention de dénomination :** Les noms de ces sous-dossiers **doivent être des codes de langue et de paramètres régionaux valides**. Le système utilise ces noms pour charger les règles correctes pour la langue active.
* **Exemples corrects :** `de-DE`, `en-US`, `en-GB`, `pt-BR`
* **Avertissement :** Si vous utilisez un nom non standard comme « german » ou « english_rules », le système ignorera le dossier ou le traitera comme un module distinct, non spécifique à une langue.

**4. Ajoutez vos fichiers de règles**
Placez vos fichiers de règles (par exemple, `FUZZY_MAP_pre.py`) dans le sous-dossier de langue approprié. Le moyen le plus simple de commencer consiste à copier le contenu d’un dossier de module de langue existant pour l’utiliser comme modèle.

### Exemple de structure de répertoire

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### Gestion des modules dans la configuration

Le système est conçu pour nécessiter une configuration minimale.

#### Activation des modules (valeur par défaut)

Les modules sont **activés par défaut**. Tant qu'un dossier de module existe dans `config/maps/`, le système le trouvera et chargera ses règles. **Vous n'avez pas besoin d'ajouter une entrée à votre fichier de paramètres pour activer un nouveau module.**

#### Désactivation des modules

Pour désactiver un module, vous devez ajouter une entrée pour celui-ci dans le dictionnaire `PLUGINS_ENABLED` dans votre fichier de paramètres et définir sa valeur sur `False`.

**Exemple (`config/settings.py`) :**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True
    "wannweil",

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### Notes de conception importantes

* **Comportement par défaut : Aucune entrée équivaut à « Vrai »**
Si un module n'est pas répertorié dans le dictionnaire `PLUGINS_ENABLED`, il est considéré comme **actif** par défaut. Cette conception maintient le fichier de configuration propre, car il vous suffit de répertorier les exceptions.

* **Raccourci pour activer**
Votre système de configuration comprend également que lister une clé de module sans valeur implique qu'elle est activée. Par exemple, ajouter « wannweil » au dictionnaire revient à ajouter « wannweil : True ». Cela fournit un raccourci pratique pour activer les modules.

* **Désactivation des modules parents (amélioration future) :** Le comportement prévu est que la désactivation d'un module parent devrait   
désactiver automatiquement tous ses modules enfants et sous-dossiers de langue. Par exemple, définir `"standard_actions": False` devrait empêcher le chargement de `de-DE` et `en-US`. *Veuillez noter que la mise en œuvre de cette désactivation récursive est toujours prévue.* (27.10.'25 lundi)
  
* **Amélioration future**
*(Remarque : il s'agit d'une fonctionnalité prévue)*
L’objectif est d’améliorer encore ce système. Par exemple, fournir un moyen de respecter les paramètres du module enfant même si le parent est désactivé, ou introduire des règles d'héritage plus complexes. (27.10.'25 lundi)