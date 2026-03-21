# Übergabe-Bericht v2: CachyOS 디버깅 – Aura STT 사후 처리

**데이텀:** 2026년 3월 21일 März (세션: 20.03. 14:00 – 21.03. 07:00 Uhr)XSPACEbreakX
**프로젝트:** `~/projects/py/stt`(Aura STT – 오프라인 음성-텍스트 시스템)  
**상태:** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1. Ausgangssituation(세션 시작)

Auf **CachyOS** 기능 지원 Dinge nicht:
- LanguageTool을 통한 Keine Rechtschreibkorrektur
- Keine Regex-Regeln 그리펜
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%, Lüfter auf Vollgas

Auf **Manjaro und Windows**는 식별 코드와 관련된 기능을 제공합니다.

---

## 2. Gelöste Probleme(Reihenfolge der Entdeckung)

### ✅ 문제 1: Falsches venv beim Start
**날짜:** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env`를 실행하면 `python3 -m venv .venv` ausgeführt → falsches venv, fehlende PaketeXSPACEbreakX가 실행됩니다.
**수정:** Zeile `python3 -m venv .env` 실행

---

### ✅ 문제 2: Vosk Double-Free(glibc 2.43)
**Ursache:** Vosk 0.3.45 hat latenten Double-Free Bug. glibc 2.43 auf CachyOS erkennt 및 terminiert den Prozess. Manjaro/ältere glibc ignorierte es still.XSPACEbreakX
**수정:** mimalloc 대체 할당자:
```bash
sudo pacman -S mimalloc
```
시작 스크립트를 구현하려면 — `/usr/lib/libmimalloc.so`를 자동으로 실행하세요.

**확인:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ 문제 3:plugins.zip Endlos-Repack-Loop(100% CPU)
**Ursache:** `secure_packer_lib.py` 스캔은 Timestamp-Check alle Dateien im Quellverzeichnis — 암시적 `aura_secure.blob`(2,4GB)입니다. Jeder Zugriff auf `.blob` 활성 시간 지정 → Timestamp neuer als ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff auf `.blob` → Endlosschleife.XSPACEbreakX
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.XSPACEbreakX
**수정:** `scripts/py/func/secure_packer_lib.py`, Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ 문제 4: e2e-Tests beim Start (89 병렬 Prozesse)
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen, startete 89 병렬 Prozesse → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.  
**수정:** `aura_engine.py` Zeilen 1167-1168 auskommentiert:
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ 문제 5: `또는 True` 창-제목-스팸
**날짜:** `scripts/py/func/process_text_in_Background.py`  
**Ursache:** `settings.DEV_MODE 또는 True인 경우:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**고치다:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

---

### ✅ 문제 6: empty_all의 Gefährliche Regeln
**날짜:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** 활성(nicht auskommentierte) Regeln die **jeden** 텍스트 löschen:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**수정:** Alle gefährlichen Beispielregeln auskommentiert. Nur `LECKER_EXAKT` (harmlos) blieb aktiv.

---

### ✅ 문제 7: pygame Segfault(스레드가 안전하지 않은 표준 출력)
**Ursache:** `SafeStreamToLogger.write()` 스크립트 `self.terminal.write(buf)` 또는 Thread-Lock. Auf CachyOS(공격적인 스레드 스케줄링)는 pygame beim gleichzeitigen Zugriff aus mehreren Threads.XSPACEbreakX를 충돌시킵니다.
**스택 추적:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
**수정:** `aura_engine.py`, Klasse `SafeStreamToLogger`:
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

### ✅ 문제 8: os.path.relpath() Segfault
**날짜:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()`는 인턴 표준 출력 → pygame Segfault aus ThreadXSPACEbreakX를 트리거합니다.
**고치다:**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

---

## 3. 악튜엘러 스탠드

CachyOS 및 칸에 대한 Aura läuft auf CachyOS 및 kann **4+ Diktate hindereinander** 성능 확인:
- ✅ Vosk-Transkription 기능
- ✅ Regelanwendung funktioniert  
- ✅ LanguageTool-Korrektur funktioniert (Großschreibung)
- ✅ 텍스트 wird geschrieben und gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Noch 공격 문제: Stiller Crash nach 1-5 Diktaten

**증상:** Aura Stirbt ohne Segfault in stderr, kein klarer Python-Traceback sichtbar.

**스택을 크래시로 설정하는 방법(표준 오류):**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

**Wahrscheinliche Ursachen:**
1. 'SafeStreamToLogger'(z.B. `self.file_handler_ref.handle(record)`)에 스레드가 안전하지 않은 Stellen이 있습니다.
2. 배경 스레드의 Unbehandelte 예외가 여전히 schluckt입니다.
3. 유지 관리 작업(`trigger_aura_maintenance.py`) der 하위 프로세스 시작 및 충돌

**Nächster 진단 문서:**
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**Stelle에 대한 확인** — `is_logging` 플래그는 스레드로부터 안전하지 않습니다.
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
베서:
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

## 5. Weitere bekannte Probleme(nicht kritisch)

### Ollama 연결 오류
Ollama는 CachyOS에서 사용할 수 없습니다 → `z_fallback_llm/ask_ollama.py` produziert hunderte Fehler-Logs.XSPACEbreakX
임시 비활성화:
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

### 플러그인/ Verzeichnis zu groß(2,8GB)
Braucht Aufräumen — 대체 ZIP 날짜 및 백업.

### DEV_MODE_all_processing과 settings.DEV_MODE 잉크 비교
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` lädt manchmal den falschen Wert. Nicht kritisch aber verwirrend.

### 비공개 지도의 NameError
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` erscheint bei jedem Diktat — ein NameError in einer privaten Map-Datei wird automatisch korrigiert. Kein Absturz, 불안정한 전위.

---

## 6. Geänderte Dateien(Zusammenfassung)

| 다테이 | 엔데룽 |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` 실행 |
| `scripts/py/func/secure_packer_lib.py` | `.blob` 및 `.zip` vom Timestamp-Scan ausgeschlossen |
| `aura_engine.py` | e2e-테스트 전문가; `SafeStreamToLogger`의 `threading.Lock`; `또는 True` 실행 |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True`(디버깅을 위한 임시) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln auskommentiert |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | '.py_bak'에 대해 알아보세요 |

---

## 7. README를 확인하세요.

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
커밋: `"현재 CachyOS는 제한되어 있습니다."`

---


Auf CachyOS는 pygame의 stdout-Ersatz nicht 스레드로부터 안전하지 않습니다.
수정 사항은 스레딩 잠금과 관련이 없습니다.
bashsed -n '418,422p' aura_engine.py



## 8. 힐프레이체 베펠레

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

*현재 확인: 2026년 3월 21일 07:00 Uhr — Claude Sonnet 4.6*XSPACEbreakX를 통한 디버깅 세션
*세션-Dauer: ~17 Stunden*