# Unmatched Training Plugin (`a_collect_unmatched_training`)

## Zweck

Dieses Plugin sammelt automatisch unerkannte Spracheingaben und fügt diese hinzu
als neue Varianten des Fuzzy-Map-Regex. Dadurch kann sich das System „selbst trainieren“
im Laufe der Zeit durch Lernen aus unübertroffenen Erkennungsergebnissen.

## Wie es funktioniert

1. Die Catch-All-Regel „COLLECT_UNMATCHED“ in „FUZZY_MAP_pre.py“ wird ausgelöst, wenn
Keine andere Regel passte zur Spracheingabe.
2. „collect_unmatched.py“ wird über „on_match_exec“ mit dem passenden Text aufgerufen.
3. Der Text wird zu „unmatched_list.txt“ hinzugefügt (durch Pipes getrennt).
4. Der Regex in „FUZZY_MAP_pre.py“ wird automatisch um die neue Variante erweitert.

## Deaktivieren des Plugins

Wenn Sie genügend Trainingsdaten gesammelt haben, deaktivieren Sie dieses Plugin, indem Sie entweder:

- Deaktivieren in den Aura-Einstellungen
- Entfernen des Plugin-Ordners aus dem Verzeichnis „maps“.
– Den Ordner mit einem ungültigen Namen umbenennen (z. B. ein Leerzeichen hinzufügen: „a_collect unmatched_training“)

## Dateistruktur
```
a_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## Notiz

Das Plugin ändert „FUZZY_MAP_pre.py“ zur Laufzeit. Stellen Sie sicher, dass Sie sich verpflichten
Aktualisieren Sie die Datei regelmäßig, um die gesammelten Trainingsdaten zu bewahren.