# CopyQ – Benutzeroberfläche & Integration in SL5 Aura

## Was ist CopyQ?

CopyQ ist ein erweiterbarer Clipboard-Manager mit einer skriptbaren Benutzeroberfläche.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python-Script oder Tastenkürzel.

Für SL5 Aura ist CopyQ das primäre Werkzeug um Sprach-zu-Text Ergebnisse
in die Zwischenablage zu bringen und dort zu verwalten.

## Relevante Dateien im Repo

| Datei | Zweck |
|---|---|
| `tools/export_to_copyq.py` | Exportiert FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` | Verarbeitet Text und sendet ihn an CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Nummeriert Clipboard-Text um |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Test-Script für Clipboard-Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

## export_to_copyq.py

Das Script `tools/export_to_copyq.py` liest die Map-Dateien des Repos (read-only)
und sendet die Regeln als strukturierte Items an CopyQ.

**Wichtig:** Das Script verändert keine Dateien im Repo – es sendet nur Kommandos
an den externen CopyQ-Prozess.

### Plattformen

- **Linux:** `copyq` ist direkt im PATH verfügbar
- **Windows:** Typische Pfade werden automatisch gesucht, z.B. `C:\Program Files\CopyQ\copyq.exe`

### Nutzung

```bash
python tools/export_to_copyq.py
```

## CopyQ per Kommandozeile steuern

CopyQ hat eine eingebaute CLI:

```bash
# Aktuellen Clipboard-Inhalt zeigen
copyq read 0

# Text in Clipboard schreiben
copyq add "Mein Text"

# Item aus History holen (Index 0 = aktuell)
copyq read 0

# CopyQ-Fenster öffnen
copyq show

# Script ausführen
copyq eval "popup('Hallo von Aura!')"
```

## Koan 11 – CopyQ Benutzeroberfläche

Der Koan `11_copyq_benutzeroberflaeche` enthält Regeln die das Wort "koans"
aus typischen STT-Erkennungsfehlern wiederherstellen.

### FUZZY_MAP_pre.py (vor LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Diese Regel greift bei Fullmatch (`^...$`) – stoppt also die weitere Pipeline.

### FUZZY_MAP.py (nach LanguageTool)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

Diese Regel greift auch innerhalb eines längeren Satzes (kein Fullmatch).

## Typische STT-Fehler bei "CopyQ"

Vosk erkennt "CopyQ" oft als:
- `copy cue`
- `kopie ku`
- `copy queue`
- `kopi q`

Mögliche Korrektur-Regel für `FUZZY_MAP_pre.py`:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

## pyperclip als Python-Alternative

Wenn CopyQ nicht verfügbar ist, nutzt Aura `pyperclip` als Fallback:

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` ist im `.venv` installiert (`site-packages/pyperclip/`).

## Hinweise

- CopyQ muss als Hintergrundprozess laufen damit die CLI funktioniert
- Unter Linux: `copyq &` beim Systemstart
- Unter Windows: CopyQ startet automatisch im Tray wenn installiert
- Für Tests: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`
