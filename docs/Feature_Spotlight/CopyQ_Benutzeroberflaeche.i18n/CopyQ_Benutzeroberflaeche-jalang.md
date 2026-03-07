# CopyQ – Benutzeroberfläche と SL5 Aura への統合

## CopyQ でしたか?

CopyQ is erweiterbarer Clipboard-Manager mit einer skriptbaren Benutzeroberfläche.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Commandozeile、
Python スクリプトまたは Tastenkurzel。

SL5 Aura ist CopyQ das primäre Werkzeug um Sprach-zu-Text Ergebnisse
さまざまなイベントが開催されます。

## 関連する日付に関するレポ

|ダテイ |ツベック |
|---|---|
| `tools/export_to_copyq.py` | Exportiert FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` |テキストを確認し、CopyQ を送信します。
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Nummeriert クリップボード テキスト うーん |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | Clipboard-Zugriff のテスト スクリプト |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum テーマ |

## export_to_copyq.py

Das Script `tools/export_to_copyq.py` 最も古い Map-Dateien des Repos (読み取り専用)
アイテムをコピー Q に送信します。

**Wichtig:** Das Script verändert keine Dateien im Repo – es sendet nur Commandos
外部の CopyQ-Prozess です。

### プラットフォーメン

- **Linux:** `copyq` は PATH を直接指定します
- **Windows:** Typische Pfade werden automatisch geucht、z.B. `C:\Program Files\CopyQ\copyq.exe`

### ヌツング

```bash
python tools/export_to_copyq.py
```

## CopyQ per Kommandozeile steuern

CopyQ Hat eine eingebaute CLI:

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

## 公案 11 – CopyQ Benutzeroberfläche

Der Koan `11_copyq_benutzeroberflaeche` enthält Regeln die das Wort "koans"
aus typischen STT-Erkennungsfehlern wiederherstellen。

### FUZZY_MAP_pre.py (言語ツール)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

フルマッチ (`^...$`) – パイプラインも停止します。

### FUZZY_MAP.py (言語ツールなし)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

Diese Regel grift auch innerhalb eines längeren Satzes (kein Fullmatch)。

## Typische STT-Fehler bei "CopyQ"

Vosk erkennt "CopyQ" は次のとおりです。
- `コピーキュー`
- `コピーク`
- `コピーキュー`
- 「コピQ」

`FUZZY_MAP_pre.py` のコレクトゥル レーゲルの例:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

## pyperclip als Python 代替



```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip` は `.venv` をインストールします (`site-packages/pyperclip/`)。

## ヒンヴァイセ

- CopyQ muss als Hintergrundprozess laufen damit die CLI funktioniert
- Linux の場合: `copyq &` beim Systemstart
- Windows の場合: CopyQ はトレイのインストール時に自動的に起動します
- 最後のテスト: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`