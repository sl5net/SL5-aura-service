# Plugin de formation inégalé (`a_collect_unmatched_training`)

## But

Ce plugin collecte automatiquement les entrées vocales non reconnues et les ajoute
comme nouvelles variantes de la regex de carte floue. Cela permet au système de « s'auto-entraîner »
au fil du temps en apprenant de résultats de reconnaissance inégalés.

## Comment ça marche

1. La règle fourre-tout `COLLECT_UNMATCHED` dans `FUZZY_MAP_pre.py` se déclenche lorsque
aucune autre règle ne correspondait à la saisie vocale.
2. `collect_unmatched.py` est appelé via `on_match_exec` avec le texte correspondant.
3. Le texte est ajouté à « unmatched_list.txt » (séparé par des tuyaux).
4. L'expression régulière dans `FUZZY_MAP_pre.py` est automatiquement étendue avec la nouvelle variante.

## Désactiver le plugin

Lorsque vous avez collecté suffisamment de données d'entraînement, désactivez ce plugin en :

- Le désactiver dans les paramètres Aura
- Suppression du dossier plugin du répertoire `maps`
- Renommer le dossier avec un nom invalide (par exemple ajouter un espace : `a_collect unmatched_training`)

## Structure du fichier
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## Note

Le plugin modifie `FUZZY_MAP_pre.py` au moment de l'exécution. Assurez-vous de vous engager
le fichier mis à jour régulièrement pour préserver les données de formation collectées.