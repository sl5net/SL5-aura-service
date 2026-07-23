# FUZZY_MAP-Regelhandbuch

## Regelformat

```python
('replacement', r'regex_pattern', threshold, {'command_flags': re.IGNORECASE})
```

| Position | Name | Beschreibung |
|---|---|---|
| 1 | Ersatz | Der Ausgabetext nach der Regel stimmt mit | überein
| 2 | Muster | Regex oder Fuzzy-String zum Vergleich mit |
| 3 | Schwelle | Für Regex-Regeln: ignoriert. Für Fuzzy-Regeln: Mindestübereinstimmungspunktzahl (0–100) |
| 4 | Optionen | Optionales Wörterbuch (siehe „Optionsreferenz“ unten). Für Standardwerte | verwenden Sie „0“ oder lassen es weg
### Roher Ersatz
Standardmäßig („False“) werden Ersetzungszeichenfolgen von Pythons „re.sub()“ verarbeitet, das die Verwendung von Regex-Rückverweisen wie „\1“ oder „\2“ zum Einfügen erfasster Gruppen unterstützt (zum Beispiel: „(r'\1‘, r‘(\d)\s+(?=\d)‘, 95)‘).
Wenn Ihre Ersetzung eine mehrzeilige Zeichenfolge ist oder Backslashes ohne Escapezeichen enthält (z. B. Codevorlagen oder Pfade) und genau so beibehalten werden soll, wie sie ist, aktivieren Sie „raw_replacement“: True im Optionswörterbuch:
```python
(System_Instructions, r'^(system instructions)$', 10, {'command_flags': re.IGNORECASE, 'raw_replacement': True})
```

### Verfügbare vom Benutzer konfigurierbare Optionen:

* **`command_flags`** (Ganzzahl): Regex-Flags, die während der Musterkompilierung verwendet werden.
*Beispiel:* `{'command_flags': re.IGNORECASE}`
* **`raw_replacement`** (boolean): Bei „True“ wird der Ersetzungstext als reines String-Literal behandelt und durch Pythons „re.sub“-Backslash-Analyse umgangen. Entscheidend für mehrzeilige Eingabeaufforderungen oder Zeichenfolgen mit Backslashes ohne Escapezeichen (`\`).
*Beispiel:* `{'raw_replacement': True}`
* **`cache`** (boolean): Schaltet den AURA-Ergebniscache um. Für Regeln, die dynamische Ausgaben generieren (z. B. aktuelle Uhrzeit, zufällige Witze), auf „False“ setzen, um sicherzustellen, dass sie bei jedem Spiel neu ausgewertet werden.
*Beispiel:* `{'cache': False}`
* **`skip_list`** (Liste von Zeichenfolgen): Gibt Nachbearbeitungs-Pipeline-Module an, die übersprungen werden sollen, wenn diese Regel übereinstimmt.
*Beispiel:* `{'skip_list': ['LanguageTool']}` (überspringt die Grammatikprüfung)
* **`only_in_windows`** (Liste der Regex-Strings): Beschränkt die Regel so, dass sie nur dann ausgelöst wird, wenn der Titel des aktiven Fensters mit einem der angegebenen Muster übereinstimmt.
*Beispiel:* `{'only_in_windows': [r'^Mozilla Firefox$', r'Chrome']}`
* **`exclude_windows`** (Liste der Regex-Strings): Verhindert, dass die Regel ausgelöst wird, wenn der Titel des aktiven Fensters mit einem der angegebenen Muster übereinstimmt.
*Beispiel:* `{'exclude_windows': [r'Terminal', r'Claude']}`
* **`window_ignore_case`** (boolean): Steuert, ob der Fensterabgleich („only_in_windows“ / „exclude_windows“) ohne Berücksichtigung der Groß-/Kleinschreibung („True“) oder unter Berücksichtigung der Groß-/Kleinschreibung („False“) ausgewertet wird. Wenn es weggelassen wird, wird auf die globale Einstellung „LOWERCASE_WINDOW_TITLES“ in „config/settings.py“ zurückgegriffen.
*Beispiel:* `{'window_ignore_case': False}`
* **`on_match_exec`** (Liste von Pfad-/String-Objekten): Pfade zu Skripten/Plugins, die ausgeführt werden sollen, wenn diese Regel übereinstimmt (wird häufig von Catch-All- und Fallback-Regeln verwendet).
*Beispiel:* `{'on_match_exec': [PROJECT_ROOT / 'scripts' / 'custom_action.py']}`

## Pipeline-Logik
- Regeln werden **top-down** verarbeitet


## Pipeline-Logik

- Regeln werden **top-down** verarbeitet
- **Alle** Matching-Regeln werden angewendet (kumulativ)
- Ein **fullmatch** (`^...$`) stoppt die Pipeline sofort
- Frühere Regeln haben Vorrang vor späteren Regeln

## Gemeinsame Muster

### Übereinstimmung mit einem einzelnen Wort (Wortgrenze)
```python
('Python', r'\bpython\b', 0, {'command_flags': re.IGNORECASE})
```

### Passen Sie mehrere Varianten an
```python
('OpenAI', r'\bopen\s*ai\b', 0, {'command_flags': re.IGNORECASE})
```

### Fullmatch – stoppt die Pipeline
```python
('hello koan', r'^.*$', 0, {'command_flags': re.IGNORECASE})
```
⚠️ Das passt zu **allem**. Die Pipeline stoppt hier. Frühere Regeln haben weiterhin Vorrang.

### Beginn der Eingabe anpassen
```python
('Note: ', r'^notiz\b', 0, {'command_flags': re.IGNORECASE})
```

### Passt genau zu der Phrase
```python
('New York', r'\bnew york\b', 0, {'command_flags': re.IGNORECASE})
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
    ('Raspberry Pi', r'\braspberry\s*pie?\b', 0, {'command_flags': re.IGNORECASE}),

    # Expand abbreviation
    ('zum Beispiel', r'\bzb\b', 0, {'command_flags': re.IGNORECASE}),

    # Stop pipeline for testing
    # ('test koan', r'^.*$', 0, {'command_flags': re.IGNORECASE}),
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
    ('My Rule', r'my rule', 0, {'command_flags': re.IGNORECASE}),
]
# ============================================================
# Longer explanations, task descriptions, notes...
# can be as long as needed — they go AFTER the rules.
# ============================================================
```

**Warum?** Auras Auto-Fix scannt nur die ersten ca. 1 KB einer Datei.
Wenn Ihre Regeln nach einer langen Kopfzeile angezeigt werden, kann Auto-Fix sie nicht finden oder reparieren.
Der Pfadkommentar in Zeile 1 wird ebenfalls empfohlen – er hilft Benutzern, die Datei schnell zu identifizieren.