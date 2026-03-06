# Regex-Kartenwartungstools

Zur Unterstützung der Schnellsuchfunktion („s“-Befehl / „search_rules.sh“) verwenden wir ein Hilfsskript, das Regex-Muster automatisch mit für Menschen lesbaren Beispielen annotiert.

## Warum brauchen wir das?
Unsere „FUZZY_MAP.py“-Dateien enthalten komplexe reguläre Ausdrücke. Um sie über Fuzzy-Finder (fzf) durchsuchbar zu machen, ohne den rohen regulären Ausdruck verstehen zu müssen, fügen wir „# EXAMPLE:“-Kommentare über den Mustern hinzu.

**Vor:**
```python
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

**Nachher (automatisch generiert):**
```python
# EXAMPLE: 1234-5678-9012-3456
('CreditCard', r'\b(?:\d[ -]*?){13,16}\b', ...)
```

## Das Tagger-Skript (`map_tagger.py`)

Wir stellen ein Python-Skript zur Verfügung, das alle Dateien „FUZZY_MAP.py“ und „FUZZY_MAP_pre.py“ scannt und diese Beispiele automatisch generiert.

### Installation
Das Skript benötigt die „exrex“-Bibliothek, um zufällige Übereinstimmungen für komplexe reguläre Ausdrücke zu generieren.

```bash
pip install exrex
```

### Nutzung
Führen Sie das Skript im Projektstammverzeichnis aus:

```bash
python3 tools/map_tagger.py
```

### Arbeitsablauf
1. **Erstellen oder bearbeiten** Sie eine Kartendatei (z. B. Hinzufügen neuer Regeln).
2. **Führen** Sie das Tagger-Skript aus.
3. **Interaktiver Modus:**
- Das Skript zeigt Ihnen einen generierten Vorschlag.
- Drücken Sie „ENTER“, um es zu akzeptieren.
- Geben Sie zum Überspringen „s“ ein.
- Geben Sie „sa“ (alle überspringen) ein, wenn Sie alle verbleibenden Muster überspringen möchten, deren Generierung fehlschlägt.
4. **Übernehmen** Sie die Änderungen.

> **Hinweis:** Das Skript ignoriert vorhandene „# EXAMPLE:“-Tags, sodass eine wiederholte Ausführung sicher ist.