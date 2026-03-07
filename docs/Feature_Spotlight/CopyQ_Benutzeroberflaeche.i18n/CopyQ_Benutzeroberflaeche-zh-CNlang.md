# CopyQ – Benutzeroberfläche 与 SL5 Aura 中的集成

## 这是 CopyQ 吗？

CopyQ ist ein erweiterbarer Clipboard-Manager mit einer skriptbaren Benutzeroberfläche。
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python 脚本或 Tastenkürzel。

Für SL5 Aura ist CopyQ das primäre Werkzeug um Sprach-zu-Text Ergebnisse
in die Zwischenablage zu Bringen und dort zu verwalten。

## 回购协议中的相关日期

|达泰|兹韦克 |
|---|---|
| `工具/export_to_copyq.py` |导出 FUZZY_MAP-Regeln nach CopyQ |
| `scripts/py/func/process_text_in_background.py` |通过 CopyQ 发送文本和发送 |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Nummeriert 剪贴板文本 um |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` |剪贴板测试脚本-Zugriff |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` |主题 | Koan-Übungen zum Thema |

## 导出到copyq.py

Das 脚本 `tools/export_to_copyq.py` 位于 Map-Dateien des Repos（只读）


**内容：** Das Script verändert keine Dateien im Repo – es sendet nur Kommandos
一个外部 CopyQ-Prozess。

### 平台

- **Linux:** `copyq` ist direkt im PATH verfügbar
- **Windows：** Typische Pfade werden automatisch gesucht，z.B. `C:\Program Files\CopyQ\copyq.exe`

### 疯狂

__代码_块_0__

## CopyQ 根据 Kommandozeile steuern

CopyQ hat eine eingebaute CLI：

__代码_块_1__

## 公案 11 – CopyQ Benutzeroberfläche

Der Koan `11_copyq_benutzeroberflaeche` enthält Regeln die das Wort “koans”
aus type STT-Erkennungsfehlern wiederherstellen。

### FUZZY_MAP_pre.py（或 LanguageTool）

__代码_块_2__

Diese Regel greift bei Fullmatch (`^...$`) – 也停止了管道。

### FUZZY_MAP.py（nach LanguageTool）

__代码_块_3__

Diese Regel greift auch insidehalb eines längeren Satzes (kein Fullmatch)。

## 典型的 STT-Fehler bei“CopyQ”

Vosk erkennt“CopyQ”经常是：
- `复制提示`
- `kopie ku`
- `复制队列`
- `kopi q`

Mögliche Korrektur-Regel für `FUZZY_MAP_pre.py`：

__代码_块_4__

## pyperclip 作为 Python-Alternative

Wenn CopyQ nicht verfügbar ist, nutzt Aura `pyperclip` als 后备：

__代码_块_5__

`pyperclip` 是 `.venv` 安装程序 (`site-packages/pyperclip/`)。

## 说明

- CopyQ muss als Hintergrundprozess laufen damit die CLI 功能
- 在 Linux 下：`copyq &` beim Systemstart
- 在 Windows 下：CopyQ 在安装时在托盘中自动启动
- 用于测试：`config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`