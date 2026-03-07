# CopyQ – Benutzeroberfläche 및 SL5 Aura의 통합

## CopyQ가 아니었나요?

CopyQ는 Benutzeroberfläche에 대한 클립보드 관리자와 같은 erweiterbarer 클립보드 관리자입니다.
Er speichert eine History aller kopierten Inhalte und erlaubt Zugriff per Kommandozeile,
Python-Script 또는 Tastenkürzel.

Für SL5 Aura ist CopyQ das primäre Werkzeug um Sprach-zu-Text Ergebnisse
in die Zwischenablage zu Bringen und dort zu verwalten.

## 관련 Dateien im Repo

| 다테이 | 즈베크 |
|---|---|
| `도구/export_to_copyq.py` | 수출 FUZZY_MAP-등록 없음 CopyQ |
| `scripts/py/func/process_text_in_Background.py` | CopyQ에 대한 텍스트 및 전송 내용 확인 |
| `config/maps/plugins/standard_actions/de-DE/renumber_clipboard_text.py` | Nummeriert 클립보드-텍스트 음 |
| `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py` | 클립보드-Zugriff에 대한 테스트 스크립트 |
| `config/maps/koans_deutsch/11_copyq_benutzeroberflaeche/` | Koan-Übungen zum 테마 |

## import_to_copyq.py

Das Script `tools/export_to_copyq.py` liest die Map-Dateien des Repos(읽기 전용)
und sendet die Regeln als strukturierte Items an CopyQ.

**위치:** Das Script verändert keine Dateien im Repo – es sendet nur Kommandos
외부 CopyQ-Prozess.

### 플랫폼

- **Linux:** `copyq` ist direct im PATH verfügbar
- **Windows:** Typische Pfade werden automatisch gesucht, z.B. `C:\Program Files\CopyQ\copyq.exe`

### 누정

```bash
python tools/export_to_copyq.py
```

## Kommandozeile steuern에 따른 CopyQ

CopyQ는 CLI를 사용합니다:

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

### FUZZY_MAP_pre.py(LanguageTool)

```python
FUZZY_MAP_pre = [
    ('koans', '^(korn|korns|koons|cohens|kreuz|kohl|kurz|chor ins|cuarn|twain|kurt)$'),
]
```

Diese Regel greift bei Fullmatch(`^...$`) – 파이프라인도 중지합니다.

### FUZZY_MAP.py(LanguageTool 없음)

```python
FUZZY_MAP = [
    ('koans', '(korn|korns|chor|chor ins|kohlen)'),
]
```

Diese Regel greift auch innerhalb eines längeren Satzes(완전 일치).

## Typische STT-Fehler bei "CopyQ"

Vosk erkennt "CopyQ"는 종종 다음과 같습니다:
- '큐 복사'
- `코피 쿠`
-`복사 대기열`
- `코피 q'

`FUZZY_MAP_pre.py`에 대한 Mögliche Korrektur-Regel:

```python
('CopyQ', r'\b(copy\s*q(ue|ue?ue)?|kopi\s*q)\b', 0, {'flags': re.IGNORECASE}),
```

## pyperclip은 Python-Alternative 역할을 합니다.

Wenn CopyQ nicht verfügbar ist, nutzt Aura `pyperclip` as Fallback:

```python
import pyperclip
pyperclip.copy("Text in Clipboard")
text = pyperclip.paste()
```

`pyperclip`은 `.venv` 설치 프로그램(`site-packages/pyperclip/`)입니다.

## 힌바이제

- CopyQ는 Hintergrundprozess laufen damit die CLI 기능을 비난합니다.
- Linux용: `copyq &` beim Systemstart
- Windows용: CopyQ startet automatisch im Tray wenn installiert
- 추가 테스트: `config/maps/plugins/z_fallback_llm/de-DE/test_clipboard.py`