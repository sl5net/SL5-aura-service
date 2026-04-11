# FUZZY_MAP-Regelhandbuch

## Regelformat

```python
('replacement', r'regex_pattern', threshold, {'flags': re.IGNORECASE})
```

| Position | Name | Beschreibung |
|---|---|---|
| 1 | Ersatz | Der Ausgabetext nach der Regel stimmt mit | überein
| 2 | Muster | Regex oder Fuzzy-String zum Vergleich mit |
| 3 | Schwelle | Wird für Regex-Regeln ignoriert. Wird für Fuzzy-Matching verwendet (0–100) |
| 4 | Flaggen | `{'flags': re.IGNORECASE}` für Groß-/Kleinschreibung, `0` für Groß-/Kleinschreibung |

## Pipeline-Logik

- Regeln werden **top-down** verarbeitet
- **Alle** Matching-Regeln werden angewendet (kumulativ)
- Ein **fullmatch** (`^...$`) stoppt die Pipeline sofort
- Frühere Regeln haben Vorrang vor späteren Regeln

## Gemeinsame Muster

### Übereinstimmung mit einem einzelnen Wort (Wortgrenze)
```python
('Python', r'\bpython\b', 0, {'flags': re.IGNORECASE})
```

### Passen Sie mehrere Varianten an
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'flags': re.IGNORECASE})
```

### Fullmatch – stoppt die Pipeline
```python
('hello koan', r'^.*$', 0, {'flags': re.IGNORECASE})
```
⚠️ Das passt zu **allem**. Die Pipeline stoppt hier. Frühere Regeln haben weiterhin Vorrang.

### Beginn der Eingabe anpassen
```python
('Note: ', r'^notiz\b', 0, {'flags': re.IGNORECASE})
```

### Passt genau zu der Phrase
```python
('New York', r'\bnew york\b', 0, {'flags': re.IGNORECASE})
```

## Dateispeicherorte

| Datei | Phase | Beschreibung |
|---|---|---|
| `FUZZY_MAP_pre.py` | Pre-LanguageTool | Wird vor der Rechtschreibprüfung angewendet |
| `FUZZY_MAP.py` | Post-LanguageTool | Wird nach der Rechtschreibprüfung angewendet |
| `PUNCTUATION_MAP.py` | Pre-LanguageTool | Zeichensetzungsregeln |

## Tipps

- Stellen Sie **spezifische** Regeln vor **allgemeine** Regeln
- Verwenden Sie „^...$“ fullmatch nur, wenn Sie die gesamte weitere Verarbeitung stoppen möchten
- „FUZZY_MAP_pre.py“ ist ideal für Korrekturen vor der Rechtschreibprüfung
- Testregeln mit: „s your test input“ in der Aura-Konsole
- Backups werden automatisch als „.peter_backup“ erstellt

## Beispiele

```python
FUZZY_MAP_pre = [
    # Correct a common STT mistake
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'flags': re.IGNORECASE}),
]
```

## Ihre erste Regel – Schritt für Schritt

1. Öffnen Sie „config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py“.
2. Fügen Sie Ihre Regel in „FUZZY_MAP_pre = [...]“ hinzu
3. Speichern – Aura wird automatisch neu geladen, kein Neustart erforderlich
4. Diktieren Sie Ihre Auslösephrase und beobachten Sie, wie sie ausgelöst wird


## Empfohlene Dateistruktur

Platzieren Sie Ihre Regeln **vor** langen Kommentarblöcken:
```python
# config/maps/plugins/sandbox/de-DE/FUZZY_MAP_pre.py
import re  # noqa: F401
# too<-from
FUZZY_MAP_pre = [
    ('My Rule', r'my rule', 0, {'flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**Warum?** Auras Auto-Fix scannt nur die ersten ca. 1 KB einer Datei.
Wenn Ihre Regeln nach einer langen Kopfzeile angezeigt werden, kann Auto-Fix sie nicht finden oder reparieren.
Der Pfadkommentar in Zeile 1 wird ebenfalls empfohlen – er hilft Benutzern, die Datei schnell zu identifizieren.