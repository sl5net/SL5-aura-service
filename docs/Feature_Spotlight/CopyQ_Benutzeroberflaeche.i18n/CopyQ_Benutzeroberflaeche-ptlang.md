# CopyQ – Benutzeroberfläche e integração no SL5 Aura

## Era CopyQ?

CopyQ é um gerenciador de área de transferência integrado com uma barra de script padrão.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python-Script ou Tastenkürzel.

Para SL5 Aura é CopyQ das primeiras ferramentas de trabalho para criação de texto
in die Zwischenablage zu trazen und dort zu verwalten.

## Dados relevantes no repositório

| Data | Zweck |
|---|---|
| `ferramentas/export_to_copyq.py` | Exportado FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` | Escrever texto e enviá-lo para um CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Número de texto da área de transferência um |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Script de teste para Clipboard-Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

## export_to_copyq.py

O script `tools/export_to_copyq.py` é o mapa de dados dos repositórios (somente leitura)
e envie o regulamento para itens estruturados e CopyQ.

**Observação:** O script não contém nenhuma data no repositório – é enviado apenas comandos
e o processo CopyQ externo.

### Plataformas

- **Linux:** `copyq` está diretamente no PATH verificado
- **Windows:** Typische Pfade werden automatisch gesucht, z.B. `C:\Arquivos de Programas\CopyQ\copyq.exe`

### Nutzung

```bash
python tools/export_to_copyq.py
```

## CopyQ para Kommandozeile Steuern

CopyQ com uma CLI completa:

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
como típico STT-Erkennungsfehlern wiederherstellen.

### FUZZY_MAP_pre.py (para LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Este Reggel é bom para Fullmatch (`^...$`) – interrompe também o nosso Pipeline.

### FUZZY_MAP.py (nach LanguageTool)

__CODE_BLOCO_3__

Este Regel também é um grande número de Satzes (sem Fullmatch).

## Typische STT-Fehler bei "CopyQ"

Você usa "CopyQ" frequentemente como:
- `copiar sugestão`
- `copiar ku`
- `copiar fila`
- `kopi q`

Regras de correção padrão para `FUZZY_MAP_pre.py`:

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

## pyperclip como Python-Alternative

Se o CopyQ não for verificado, deixe Aura `pyperclip` como substituto:

__CODE_BLOCO_5__

`pyperclip` está instalado em `.venv` (`site-packages/pyperclip/`).

##Hinweise

- CopyQ deve ser usado no processo de base devido à funcionalidade CLI
- No Linux: `copyq &` beim Systemstart
- No Windows: o CopyQ inicia automaticamente na bandeja durante a instalação
- Para testes: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`