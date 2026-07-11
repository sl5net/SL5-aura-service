## Création de nouveaux modules de plugin ( docs/CreatingNewPluginModules.md )

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

(Facultatif) Pour Vrai/Faux, vous pouvez également utiliser 1/0. Cependant, cela est rare et peut réduire la lisibilité.

**Exemple (`config/settings.py`) :**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True. Not False means True.
    # "wannweil": False,

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
  
(Facultatif) Pour Vrai/Faux, vous pouvez également utiliser 1/0. Cependant, cela est rare et peut réduire la lisibilité.

* **Désactivation des modules parents :** Le comportement prévu est que la désactivation d'un module parent devrait   
désactiver automatiquement tous ses modules enfants et sous-dossiers de langue. Par exemple, définir `"standard_actions": False` devrait empêcher le chargement de `de-DE` et `en-US`. (27.10.'25 lundi)
  
*   **but**
L’objectif est d’améliorer encore ce système. Par exemple, fournir un moyen de respecter les paramètres du module enfant même si le parent est désactivé, ou introduire des règles d'héritage plus complexes. (27.10.'25 lundi)


  
  
  
t1- Es ist in der Tat wesentlich benutzerfreundlicher and komfortabler, die Steuerung über die Sprachbefehle direct in diesem Dokumentationsabschnitt hervorzuheben [1].

t2- Wir erweitern den Entwurf um eine klare Beschreibung der Tasten- bzw. Sprachsteuerungsbefehle (comme « Aura, Lernmodus einschalten / ausschalten ») et les détails, comme « toggle_learning.py » das Aus- et Einkommentieren automatisiert [2].


### Activation du mode d'apprentissage (formation inégalée)

Pour permettre à votre module personnalisé d'apprendre automatiquement des phrases non reconnues lorsque le "Lernmodus" (Mode d'apprentissage) est actif, vous pouvez ajouter une règle fourre-tout au **tout en bas** de votre liste `FUZZY_MAP_pre`.

Cette règle appelle le plugin d'entraînement sans correspondance lorsqu'aucune autre règle spécifique de votre fichier ne correspond :

```python
    # --- Training-Plugin (dynamically toggled by the learning mode) ---
    (f'{str(__file__)}', r'^(.*)$', 10, {
        'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']
    }),
```

Le plugin de formation utilise `f'{str(__file__)}'` pour localiser votre fichier et ajouter automatiquement la phrase non reconnue au premier groupe de règles disponible (comme votre groupe de commandes principal).

#### Basculer le mode d'apprentissage via les commandes vocales

Au lieu de modifier les fichiers manuellement, le moyen le plus confortable de gérer cette fonctionnalité consiste à utiliser les commandes vocales intégrées :

* **Pour activer :** Dites *"Aura, mode d'apprentissage activé"* ou *"Aura, Lernmodus starten"*.
* **Pour désactiver :** Dites *"Aura, mode d'apprentissage désactivé"* ou *"Aura, Lernmodus stoppen"*.

Ces commandes déclenchent `toggle_learning.py` en arrière-plan, qui commente ou décommente automatiquement les lignes fourre-tout dans vos fichiers de carte actifs.
  
  
  
  
*Conseil : après avoir défini vos modèles d'expression régulière, exécutez « python3 tools/map_tagger.py » pour générer automatiquement des exemples consultables pour les outils CLI. Voir [Map Maintenance Tools](../../Developer_Guide/Map_Maintenance_Tools-frlang.md) pour plus de détails.*