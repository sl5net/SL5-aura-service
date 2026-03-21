# Übergabe-Bericht v2: CachyOS デバッグ – Aura STT 後処理

**日付:** 21. メルツ 2026 (セッション: 3 月 20 日 14:00 – 3 月 21 日 07:00 時間)  
**プロジェクト:** `~/projects/py/stt` (Aura STT – オフライン音声テキスト変換システム)  
**ステータス:** Großer Fortschritt — 4+ erfolgreiche Diktate möglich、aber noch instabil  

---

## 1. オースガング状況 (セッションの開始)

**CachyOS** 機能に関する詳細:
- Keine Rechtschreibkorrektur (LanguageTool 経由)
- Keine Regex-Regeln griffen
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%、Lüfter auf Vollgas

**Manjaro と Windows** のすべての機能がコードを識別します。

---

## 2. Gelöste 問題 (Reihenfolge der Entdeckung 内)

### ✅ 問題 1: Falsches venv beim Start
**日付:** `scripts/activate-venv_and_run-server.sh`  
**原因:** `python3 -m venv .env` が `python3 -m venv .venv` を実行する → falsches venv, fehlende Pakete  
**修正:** Zeile `python3 -m venv .env` entfernt

---

### ✅ 問題 2: Vosk Double-Free (glibc 2.43)
**原因:** Vosk 0.3.45 ハット潜在ダブルフリー バグ。 glibc 2.43 auf CachyOS erkennt および terminiert den Prozess。 Manjaro/ältere glibc ignorierte es Still.  
**修正:** mimalloc als alternator アロケーター:
```bash
sudo pacman -S mimalloc
```
スタートスクリプトの実装は、`/usr/lib/libmimalloc.so` などを自動化するものです。

**検証:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ 問題 3: plugins.zip Endlos-Repack-Loop (CPU 100%)
**Ursache:** `secure_packer_lib.py` のタイムスタンプをスキャンして、Quellverzeichnis の日付をすべてチェックしてください — 含まれる `aura_secure.blob` (2,4 GB)。 Jeder Zugriff auf `.blob` aktualisierte dessen atime → Timestamp neuer als ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff auf `.blob` → Endlosschleife.  
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.  
**修正:** `scripts/py/func/secure_packer_lib.py`、Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ 問題 4: e2e-Tests beim Start (89 並列プロゼス)
**Ursache:** `run_e2e_live_reload_func_test_v2()` は、aufgerufen を開始し、89 並列で Prozesse → Lüfter、CPU-Last、Absturz wenn erster Test fehlschlug.   を実行します。
**修正:** `aura_engine.py` Zeilen 1167-1168 のコメント:
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ 問題 5: 「または True」ウィンドウ タイトル スパム
**日付:** `scripts/py/func/process_text_in_background.py`  
**説明:** `if settings.DEV_MODE or True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**修理：**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

---

### ✅ 問題 6: empty_all の Gefährliche Regeln
**日付:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** テキストの内容:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**修正:** すべてのコメントを参照してください。 Nur `LECKER_EXAKT` (harmlos) の活動を実行してください。

---

### ✅ 問題 7: pygame セグメンテーション違反 (スレッド安全でない標準出力)
**Ursache:** `SafeStreamToLogger.write()` schrieb `self.terminal.write(buf)` はスレッドロックです。 Auf CachyOS (積極的なスレッド スケジューリング) で pygame がクラッシュし、Zugriff aus mehreren Threads.  
**スタック トレース:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
**修正:** `aura_engine.py`、Klasse `SafeStreamToLogger`:
```python
def __init__(self, ...):
    ...
    self._lock = threading.Lock()  # NEU

def write(self, buf):
    ...
    with self._lock:               # NEU
        self.terminal.write(buf)
```

---

### ✅ 問題 8: os.path.relpath() セグメンテーション違反
**日付:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` がインターン stdout → pygame Segfault aus Thread   をトリガーします
**修理：**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

---

## 3. アクトゥラースタンド

CachyOS と kann **4+ ディクテート ヒント** に関するオーラが表示されます:
- ✅ Voskトランスクリプション機能
- ✅ Regelanwendung funktioniert  
- ✅ LanguageTool-Korrektur 機能 (全体的な表現)
- ✅ テキスト wird geschrieben und gesprochen
- ⚠️オーラ シュテュルツ ナッハ 1-5 ディクタテン ノッホ アブ

---

## 4. Noch offenes 問題: Stiller Crash nach 1-5 Diktaten

**症状:** 標準エラー出力、Python-Traceback sichtbar でのセグメンテーション違反が発生します。

**クラッシュ時のスタックの説明 (標準エラー出力):**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

**Wahrscheinliche Ursachen:**
1. `SafeStreamToLogger` のスレッド安全でないステレン (z.B. `self.file_handler_ref.handle(record)`)
2. バックグラウンドでの例外例外 - スレッドが依然として停止している
3. サブプロジェクトのメンテナンスタスク (`trigger_aura_maintenance.py`) が起動してクラッシュしました

**ネヒスター診断:**
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**最新情報** — `is_logging` スレッドセーフであることを示すフラグ:
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
ベッサー:
```python
with self._lock:
    if buf and not buf.isspace() and not self.is_logging:
        self.is_logging = True
        try:
            ...
        finally:
            self.is_logging = False
```

---

## 5. Weitere bekannte 問題 (nicht kritisch)

### Ollama 接続エラー
CachyOS を使用した Ollama → `z_fallback_llm/ask_ollama.py` の製品情報 Fehler-Logs.  
一時的な操作:
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

### プラグイン/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen — alte ZIP-Dateien und Backups。

### DEV_MODE_all_processing と settings.DEV_MODE の比較
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` は、ファルシェン ウェルトを管理します。ニヒト・クリティシュ・アバー・ヴァーヴィレンド。

### プライベートマップの名前エラー
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` 自動マップデータの名前エラーが発生しました。 Kein Absturz、aber Potenziell instabil。

---

## 6. Geänderte Dateien (Zusammenfassung)

|ダテイ |アンデルング |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` と `.zip` vom Timestamp-Scan を使用する |
| `aura_engine.py` | e2e-Test オーコメンティアート; `SafeStreamToLogger` の `threading.Lock`; 「または真」 entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (デバッグのための一時的) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln のコメント |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` |うーんベナント zu `.py_bak` |

---

## 7. 詳細については README をご覧ください

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
コミット: `"CachyOS は現時点では制限されています"`

---


Auf CachyOS は pygame の stdout-Ersatz ニッチ スレッドセーフです。
スレッドロックの修正:
bashsed -n '418,422p' aura_engine.py



## 8. ヒルフライヒェ・ベフェレ

```bash
# Aura starten:
~/projects/py/stt/scripts/restart_venv_and_run-server.sh

# Crash-Log:
cat /tmp/aura_stderr.log | tail -30

# CPU-Verbrauch prüfen:
top -b -n 1 | head -15

# Hintergrundprozesse nach Crash killen:
pkill -f gawk; pkill -f translate_md; pkill -f maintenance

# mimalloc aktiv? (in Konsole beim Start sichtbar):
# "Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so)."

# Alle Prozesse nach Crash killen:
pkill -9 -f aura_engine; pkill -9 -f python3
```

---

*Bericht aktualisiert am 21.03.2026 07:00 Uhr — Claude Sonnet 4.6*   によるデバッグ セッション
*セッションダウアー: ~17 スタンデン*