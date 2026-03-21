# Übergabe-Bericht v2：CachyOS 调试 – Aura STT 后处理

**日期：** 2026 年三月 21 日（会议：20.03. 14:00 – 21.03. 07:00 Uhr）  
**项目：** `~/projects/py/stt` （Aura STT – 离线语音转文本系统）  
**状态：** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1.Ausgangssituation（会议开始）

Auf **CachyOS** 功能如下：
- Keine Rechtschreibkorrektur 通过 LanguageTool
- 凯恩·正则表达式-雷格尔恩·格里芬
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%，Lüfter auf Vollgas

Auf **Manjaro 和 Windows** alles funktionsfähig mit identischem Code。

---

## 2. Gelöste Probleme（在 Reihenfolge der Entdeckung 中）

### ✅ 问题 1：Falsches venv beim Start
**Datei:** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env` wurde vor `python3 -m venv .venv` ausgeführt → falsches venv，fehlende Pakete  
**修复：** Zeile `python3 -m venv .env` entfernt

---

### ✅ 问题 2：Vosk 双自由 (glibc 2.43)
**Ursache：** Vosk 0.3.45 帽子潜在的双重免费错误。 glibc 2.43 已在 CachyOS 中启用并终止。 Manjaro/altere glibc ignorierte es still.  
**修复：** mimalloc 是替代分配器：
__代码_块_0__
这是我的 Startskript 实现 — 例如“/usr/lib/libmimalloc.so”。

**验证：**
__代码_块_1__

---

### ✅ 问题 3：plugins.zip Endlos-Repack-Loop（100% CPU）
**Ursache：** `secure_packer_lib.py` 扫描时间戳 - 检查 Quellverzeichnis 中的所有日期 — 包含 `aura_secure.blob` (2,4 GB)。 Jeder Zugriff auf `.blob` aktualisierte dessen atime → 时间戳作为 ZIP → 重新打包 → 文件系统事件 → 地图重新加载 → Zugriff auf `.blob` → Endlosschleife.  
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.  
**修复：** `scripts/py/func/secure_packer_lib.py`，Zeile ~86：
__代码_块_2__

---

### ✅ 问题 4：e2e-Tests beim Start（89 并行 Prozesse）
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen, startete 89 paralle Prozesse → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.  
**修复：** `aura_engine.py` Zeilen 1167-1168 auskommentiert：
__代码_块_3__

---

### ✅ 问题 5：`or True` 窗口标题垃圾邮件
**Datei：** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE or True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**使固定：**
__代码_块_4__

---

### ✅ 问题 6：empty_all 中的 Gefährliche Regeln
**Datei:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache：** Aktive (nicht auskommentierte) Regeln die **jeden** 文本内容：
__代码_块_5__
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**修复：** Alle gefährlichen Beispielregeln auskommentiert。 Nur `LECKER_EXAKT` (harmlos) blieb aktiv。

---

### ✅ 问题 7：pygame Segfault（线程不安全的标准输出）
**Ursache:** `SafeStreamToLogger.write()` schrieb `self.terminal.write(buf)` ohne 线程锁。 Auf CachyOS (aggressiveres Thread-Scheduling) crashte pygame beim gleichzeitigen Zugriff aus mehreren Threads.  
**堆栈跟踪：**
__代码_块_6__
**修复：** `aura_engine.py`，类`SafeStreamToLogger`：
__代码_块_7__

---

### ✅ 问题 8：os.path.relpath() 段错误
**Datei:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` 触发实习生标准输出 → pygame Segfault aus Thread  
**使固定：**
__代码_块_8__

---

## 3. Aktueller 展台

Aura läuft auf CachyOS 和 kann **4+ Diktatehintereinander** erfolgreich verarbeiten:
- ✅ Vosk 转录功能
- ✅ Regelanwendung funktioniert  
- ✅ LanguageTool-Korrektur funktioniert (Großschreibung)
- ✅ 发送文本 geschrieben 和 gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Noch 违规问题：Stiller Crash nach 1-5 Diktaten

**症状：** Aura Stirbt ohne Segfault in stderr，kein klarer Python-Traceback sichtbar。

**Letzter bekannter Stack vor Crash (aus früherem stderr):**
__代码_块_9__

**Wahrscheinliche Ursachen：**
1. `SafeStreamToLogger` 中的 Weitere 线程不安全 Stellen (z.B. `self.file_handler_ref.handle(record)`)
2. Unbehandelte Exception in einem Background-Thread die still schluckt
3. Subprozesse启动并崩溃的维护任务（`trigger_aura_maintenance.py`）

**Nächster Diagnoseschritt：**
__代码_块_10__

**Weitere verdächtige Stelle** — `is_logging` 标记 ist nicht 线程安全：
__代码_块_11__
贝塞尔：
__代码_块_12__

---

## 5.Weitere bekannte Probleme (nicht kritisch)

### Ollama 连接错误
Ollama läuft nicht auf CachyOS → `z_fallback_llm/ask_ollama.py` produziert hunderte Fehler-Logs.  
临时关闭：
__代码_块_13__

### 插件/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen — 旧的 ZIP 日期和备份。

### DEV_MODE_all_processing 与 settings.DEV_MODE Inkonsistenz
__代码_块_14__
`dynamic_settings.py` 是一个手动设置。 Nicht kritisch aber verwirrend。

### 私人地图中的名称错误
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` erscheint bei jedem Diktat — 在私人地图数据中出现名称错误并自动修复。 Kein Absturz，aber potenziell instabil。

---

## 6. Geänderte Dateien (Zusammenfassung)

|达泰|下一篇：
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` 和 `.zip` vom Timestamp-Scan ausgeschlossen |
| `aura_engine.py` | e2e-测试 auskommentiert； `SafeStreamToLogger` 中的 `threading.Lock`； `或 True` entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True`（临时调试）|
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln auskommentiert |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | `.py_bak` 的使用 |

---

## 7. README 是有效的

__代码_块_15__
承诺：“CachyOS 目前受到限制”

---


Auf CachyOS 是 pygame 的 stdout-Ersatz nicht 线程安全的。
固定是在螺纹锁中：
bashsed -n '418,422p' aura_engine.py



## 8.Hilfreiche Befehle

__代码_块_16__

---

*Bericht aktualisiert am 21.03.2026 07:00 Uhr — 调试会话 mit Claude Sonnet 4.6*  
*Session-Dauer：~17 Stunden*