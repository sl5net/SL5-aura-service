# CopyQ – Benutzeroberfläche e integración en SL5 Aura

## ¿Era CopyQ?

CopyQ es un administrador de portapapeles diferente con una lista de archivos de escritura.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python-Script o Tastenkürzel.

Para SL5 Aura es CopyQ el primer trabajo con texto escrito
in die Zwischenablage zu Bringen und dort zu verwalten.

## Fechas relevantes en el repositorio

| Fechai | Zweck |
|---|---|
| `herramientas/export_to_copyq.py` | Exportar FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` | Verificar texto y enviar en CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Portapapeles numérico-Texto um |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Script de prueba para el portapapeles |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

## export_to_copyq.py

El script `tools/export_to_copyq.py` se encuentra en la fecha del mapa de repositorios (solo lectura)
y envía el Regeln als strukturierte Items an CopyQ.

**Wichtig:** Das Script verändert keine Dateien im Repo – es sendet nur Kommandos
un proceso externo CopyQ.

### Plataformas

- **Linux:** `copyq` está directamente disponible en PATH
- **Windows:** Typische Pfade werden automatisch gesucht, z.B. `C:\Archivos de programa\CopyQ\copyq.exe`

### nuezung

```bash
python tools/export_to_copyq.py
```

## CopyQ por Kommandozeile steuern

CopyQ tiene una CLI propia:

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

### FUZZY_MAP_pre.py (para LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Este reglamento aparece en Fullmatch (`^...$`): también detuvo el otro canal.

### FUZZY_MAP.py (después de LanguageTool)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

Este reglamento incluye también una parte interior de una bolsa larga (no Fullmatch).

## Typische STT-Fehler en "CopyQ"

Vosk erkennt "CopyQ" a menudo también:
- `copiar señal`
- `kopie ku`
- `copiar cola`
- `kopi q`

Reglas de corrección modificadas para `FUZZY_MAP_pre.py`:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

## pyperclip y alternativa a Python

Si CopyQ no está disponible, no usará Aura `pyperclip` como Fallback:

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` está instalado en `.venv` (`site-packages/pyperclip/`).

## Hinweise

- CopyQ no debe funcionar en el proceso de fondo si no funciona la CLI
- En Linux: `copyq &` en Systemstart
- En Windows: CopyQ se inicia automáticamente en la bandeja cuando se instala
- Para pruebas: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`