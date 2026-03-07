# Erste Schritte mit SL5 Aura

## Was ist SL5 Aura?

SL5 Aura ist ein Offline-Sprachassistent, der Sprache in Text (STT) umwandelt und konfigurierbare Regeln anwendet, um die Ausgabe zu bereinigen, zu korrigieren und umzuwandeln.

Es funktioniert ohne GUI – alles läuft über CLI oder Konsole.

## Wie es funktioniert

```
Microphone → Vosk (STT) → Maps (Pre) → LanguageTool → Maps (Post) → Output
```

1. **Vosk** wandelt Ihre Sprache in Rohtext um
2. **Pre-Maps** bereinigen und korrigieren Sie den Text vor der Rechtschreibprüfung
3. **LanguageTool** korrigiert Grammatik und Rechtschreibung
4. **Post-Maps** wenden endgültige Transformationen an
5. **Ausgabe** ist der endgültige saubere Text (und optional TTS)

## Deine ersten Schritte

### 1. Starten Sie Aura
```bash
python main.py
```

### 2. Test mit Konsoleneingabe
Geben Sie „s“ gefolgt von Ihrem Text ein:
```
s hello world
```

### 3. Sehen Sie eine Regel in Aktion
Öffnen Sie „config/maps/koans_deutsch/01_koan_erste_schritte/de-DE/FUZZY_MAP_pre.py“.

Kommentieren Sie die darin enthaltene Regel aus und testen Sie sie erneut. Was geschieht?

## Regeln verstehen

Regeln befinden sich in „config/maps/“ in Python-Dateien namens „FUZZY_MAP_pre.py“ oder „FUZZY_MAP.py“.

Eine Regel sieht so aus:
```python
('Hello World', r'\bhello world\b', 0, {'flags': re.IGNORECASE})
#   ^output        ^pattern          ^threshold  ^case-insensitive
```

Die **Ausgabe** steht an erster Stelle – Sie sehen sofort, was die Regel hervorbringt.

Regeln werden **von oben nach unten** verarbeitet. Der erste vollständige Treffer (`^...$`) stoppt alles.

## Koans – Learning by Doing

Koans sind kleine Übungen in `config/maps/koans_deutsch/` und `config/maps/koans_english/`.

Jedes Koan lehrt ein Konzept:

| Koan | Thema |
|---|---|
| 01_koan_erste_schritte | Erste Regel, vollständige Übereinstimmung, Pipeline-Stopp |
| 02_koan_listen | Listen, mehrere Regeln |
| 03_koan_schwierige_namen | Schwierige Namen, phonetische Zuordnung |

Beginnen Sie mit Koan 01 und arbeiten Sie sich nach oben.

## Tipps

- Regeln in „FUZZY_MAP_pre.py“ werden **vor** der Rechtschreibprüfung ausgeführt – gut zum Beheben von STT-Fehlern
- Regeln in „FUZZY_MAP.py“ werden **nach** der Rechtschreibprüfung ausgeführt – gut für die Formatierung
- Sicherungsdateien („.peter_backup“) werden vor jeder Änderung automatisch erstellt
- Verwenden Sie „peter.py“, um eine KI die Koans automatisch bearbeiten zu lassen