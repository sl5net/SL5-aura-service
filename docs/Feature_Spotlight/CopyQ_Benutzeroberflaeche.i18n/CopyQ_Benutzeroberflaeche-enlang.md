> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../CopyQ_Benutzeroberflaeche.md).*

# CopyQ – User Interface & Integration in SL5 Aura

## What is CopyQ?

CopyQ is an extensible clipboard manager with a scriptable interface.
It saves a history of all copied content and allows access via command line,
Python script or keyboard shortcut.

For SL5 Aura, CopyQ is the primary tool for speech-to-text results
to the clipboard and manage it there.

## Relevant files in the repo

| File | Purpose |
|---|---|
| `tools/export_to_copyq.py` | Exports FUZZY_MAP rules to CopyQ |
| `scripts/py/func/process_text_in_background.py` | Processes text and sends it to CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Numbers clipboard text by |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Test script for clipboard access |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan exercises on the topic |


## export_to_copyq.py

The script `tools/export_to_copyq.py` reads the map files of the repo (read-only)
and sends the rules as structured items to CopyQ.

**Important:** The script does not change any files in the repo – it only sends commands
to the external CopyQ process.

### Platforms

- **Linux:** `copyq` is directly available in the PATH
- **Windows:** Typical paths are automatically searched, e.g., `C:\Program Files\CopyQ\copyq.exe`

### Usage

```bash
python tools/export_to_copyq.py
```

## Controlling CopyQ via command line

CopyQ has a built-in CLI:

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

## Koan 11 – CopyQ User Interface

The Koan `11_copyq_benutzeroberflaeche` contains rules that the word "koans"
recover from typical STT recognition errors.

### FUZZY_MAP_pre.py (before LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

This rule applies in the case of full match (`^...$`) – thus stopping the further pipeline.

### FUZZY_MAP.py (according to LanguageTool)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

This rule also applies within a longer sentence (no full match).

## Typical STT Errors with "CopyQ"

Vosk often recognizes "CopyQ" as:
- `copy cue`
- `kopie ku`
- `copy queue`
- `kopi q`

Possible correction rule for `FUZZY_MAP_pre.py`:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'command_flags': re.IGNORECASE}),
```

## pyperclip as a Python alternative

If CopyQ is not available, Aura `pyperclip` is used as a fallback:

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` is installed in `.venv` (`site-packages/pyperclip/`).

## Notes

- CopyQ must run as a background process for the CLI to work
- On Linux: `copyq &` at system startup
- On Windows: CopyQ starts automatically in the tray when installed
- For tests: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`
