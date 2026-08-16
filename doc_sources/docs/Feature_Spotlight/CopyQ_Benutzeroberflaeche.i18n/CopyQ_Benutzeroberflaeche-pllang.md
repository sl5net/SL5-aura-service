# CopyQ – Benutzeroberfläche i integracja w SL5 Aura

## Czy to jest CopyQ?

CopyQ jest erweiterbarer Clipboard-Manager mit einer skriptbaren Benutzeroberfläche.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Skrypt Pythona lub Tastenkürzel.

Für SL5 Aura ist CopyQ das primäre Werkzeug um Sprach-zu-Text Ergebnisse
in die Zwischenablage zu Bringen und Dort zu Verwalten.

## Odpowiednie daty w repozytorium

| Data | Zweck |
|---|---|
| `narzędzia/eksport_do_kopiiq.py` | Eksport FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` | Wyślij tekst i wyślij do CopyQ |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Numeryczny tekst schowka um |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Skrypt testowy dla schowka Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum Thema |

## eksport_do_kopiiq.py

Das Script `tools/export_to_copyq.py` to najstarsza mapa-Dateien des Repos (tylko do odczytu)
und sendet die Regeln als strukturierte Items and CopyQ.

**Wichtig:** Das Script verändert keine Dateien im Repo – es sendet nur Kommandos
w zewnętrznym programie CopyQ-Prozess.

### Platformy

- **Linux:** `copyq` jest bezpośrednio na pasku PATH verfügbar
- **Windows:** Typische Pfade werden automatisch gesucht, z.B. `C:\Program Files\CopyQ\copyq.exe`

### Nutzung

__KOD_BLOKU_0__

## CopyQ dla steru Kommandozeile

CopyQ ma eine eingebaute CLI:

__KOD_BLOKU_1__

## Koan 11 – CopyQ Benutzeroberfläche

Der Koan `11_copyq_benutzeroberflaeche` enthält Regeln die das Wort "koans"
aus typischen STT-Erkennungsfehlern wiederherstellen.

### FUZZY_MAP_pre.py (dla LanguageTool)

__KOD_BLOKU_2__

Diese Regel greift bei Fullmatch (`^...$`) – zatrzymaj także inne Pipeline.

### FUZZY_MAP.py (nach LanguageTool)

__KOD_BLOKU_3__

Diese Regel greift auch internalhalb eines längeren Satzes (kein Fullmatch).

## Typische STT-Fehler bei „CopyQ”

Vosk erkennt „CopyQ” często używa również:
- `skopiuj wskazówkę`
- `kopiuj ku`
- `kopiuj kolejkę`
- `kopi q`

Mögliche Korrektur-Regel dla `FUZZY_MAP_pre.py`:

__KOD_BLOKU_4__

## pyperclip jako alternatywa dla Pythona

Wenn CopyQ nicht verfügbar ist, nutzt Aura `pyperclip` a także Fallback:

__KOD_BLOKU_5__

`pyperclip` to plik instalacyjny `.venv` (`site-packages/pyperclip/`).

## Hinweise

- CopyQ musi działać jako Hintergrundprozess laufen damit die CLI funktioniert
- Pod Linuksem: `copyq &` przy Systemstart
- W systemie Windows: CopyQ uruchamia się automatycznie w Tray podczas instalacji
- Dalsze testy: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`