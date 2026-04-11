# Unmatched Training Plugin (`1_collect_unmatched_training`)

## Zweck

Dieses Plugin sammelt automatisch unerkannte Spracheingaben und fügt diese hinzu
als neue Varianten des Fuzzy-Map-Regex. Dadurch kann sich das System „selbst trainieren“
im Laufe der Zeit durch Lernen aus unübertroffenen Erkennungsergebnissen.

## Wie es funktioniert

1. Die Catch-All-Regel „COLLECT_UNMATCHED“ wird ausgelöst, wenn keine andere Regel übereinstimmt.
2. „collect_unmatched.py“ wird über „on_match_exec“ mit dem passenden Text aufgerufen.
3. Der reguläre Ausdruck im aufrufenden „FUZZY_MAP_pre.py“ wird automatisch erweitert.

## Nutzung

Fügen Sie diese Sammelregel am Ende jeder „FUZZY_MAP_pre.py“ hinzu, die Sie trainieren möchten:
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

Die Bezeichnung „f'{str(__file__)}“ sagt „collect_unmatched.py“ genau, welche
„FUZZY_MAP_pre.py“ zum Aktualisieren – damit die Regel auf jedes Plugin übertragbar ist.

## Deaktivieren des Plugins

Wenn Sie genügend Trainingsdaten gesammelt haben, deaktivieren Sie sie folgendermaßen:

- Auskommentieren der Catch-All-Regel
- Den Ordner mit einem ungültigen Namen umbenennen (z. B. ein Leerzeichen hinzufügen)
- Entfernen des Plugin-Ordners aus dem Verzeichnis „maps“.

## Dateistruktur
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## Notiz

Das Plugin ändert „FUZZY_MAP_pre.py“ zur Laufzeit. Übernehmen Sie die Aktualisierung
Führen Sie regelmäßig eine Datei durch, um die gesammelten Trainingsdaten aufzubewahren.