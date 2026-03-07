# CopyQ – Benutzeroberfläche & Intégration dans SL5 Aura

## Était-ce CopyQ ?

CopyQ est un gestionnaire de presse-papiers plus facile à utiliser avec une seule copie de script.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python-Script ou Goûter.

Pour SL5 Aura, CopyQ est le premier outil de travail avec texte intégré
in die Zwischenablage zu bringen und dort zu verwalten.

## Dates pertinentes dans le dépôt

| Datei | Zweck |
|---|---|
| `tools/export_to_copyq.py` | Exporter les paramètres FUZZY_MAP vers CopyQ |
| `scripts/py/func/process_text_in_background.py` | Réaliser le texte et l'envoyer dans un CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Numéroté Presse-papiers-Texte à |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Test-Script pour Clipboard-Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

## export_to_copyq.py

Le script `tools/export_to_copyq.py` est le Map-Dateien des Repos (lecture seule)
et envoyez le Regeln als strukturierte Items an CopyQ.

**Quelque chose :** Le script vous envoie des données dans le dépôt – il est envoyé à vos commandos
un CopyQ-Prozess externe.

### Plateformes

- **Linux :** `copyq` est directement dans la barre PATH
- **Windows :** Typische Pfade werden automatisch gesucht, par exemple. `C:\Program Files\CopyQ\copyq.exe`

### Nutzung

```bash
python tools/export_to_copyq.py
```

## CopyQ pour le Kommandozeile Steuern

CopyQ a une CLI unique :

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

## Koan 11 – Copier les flûtes à beignets CopyQ

Le Koan `11_copyq_benutzeroberflaeche` enthält Regeln die das Wort "koans"
aus typischen STT-Erkennungsfehlern wiederherstellen.

### FUZZY_MAP_pre.py (pour LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Ce règlement est accepté par Fullmatch (`^...$`) – il s'arrête également pour d'autres pipelines.

### FUZZY_MAP.py (selon LanguageTool)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

Ce règlement prend en charge une partie intérieure plus longue (comme Fullmatch).

## Typische STT-Fehler bei "CopyQ"

Vous pouvez également utiliser "CopyQ" :
- `copier le signal`
- `copier ku`
- `copier la file d'attente`
- `kopi q`

Plusieurs modèles de textures pour `FUZZY_MAP_pre.py` :

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

## pyperclip comme Python-Alternative

Si CopyQ n'est pas disponible, utilisez Aura `pyperclip` comme solution de repli :

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` est installé dans `.venv` (`site-packages/pyperclip/`).

## Notes

- CopyQ doit également utiliser le processus de fond pour utiliser la fonction CLI
- Sous Linux : `copyq &` depuis Systemstart
- Sous Windows : CopyQ démarre automatiquement dans le bac lors de l'installation
- Pour les tests : `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`