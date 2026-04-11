# Plugin de formation inégalé (`1_collect_unmatched_training`)

## But

Ce plugin collecte automatiquement les entrées vocales non reconnues et les ajoute
comme nouvelles variantes de la regex de carte floue. Cela permet au système de « s'auto-entraîner »
au fil du temps en apprenant de résultats de reconnaissance inégalés.

## Comment ça marche

1. La règle fourre-tout `COLLECT_UNMATCHED` se déclenche lorsqu'aucune autre règle ne correspond.
2. `collect_unmatched.py` est appelé via `on_match_exec` avec le texte correspondant.
3. L'expression régulière dans l'appelant `FUZZY_MAP_pre.py` est automatiquement étendue.

## Utilisation

Ajoutez cette règle fourre-tout à la fin de tout `FUZZY_MAP_pre.py` que vous souhaitez entraîner :
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

L'étiquette `f'{str(__file__)}'` indique à `collect_unmatched.py` exactement lequel
`FUZZY_MAP_pre.py` à mettre à jour — la règle est donc portable sur n'importe quel plugin.

## Désactiver le plugin

Lorsque vous avez collecté suffisamment de données d'entraînement, désactivez-le en :

- Commenter la règle fourre-tout
- Renommer le dossier avec un nom invalide (par exemple ajouter un espace)
- Suppression du dossier plugin du répertoire `maps`

## Structure du fichier
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## Note

Le plugin modifie `FUZZY_MAP_pre.py` au moment de l'exécution. Valider la mise à jour
fichier régulièrement pour conserver les données de formation collectées.