# Übergabe-Bericht：CachyOS 调试 – Aura STT 后处理

**数据：** 20. 三月 2026  
**项目：** `~/projects/py/stt` （Aura STT – 离线语音转文本系统）  
**状态：** 问题 noch nicht gelöst – Übergabe an nächsten Mitarbeiter  

---

## 1. 问题描述

Nach dem Wechsel auf **CachyOS** Funktionieren in Aura folgende Dinge nicht mehr:

- **Rechtschreibkorrektur 通过 LanguageTool** wird nicht ausgeführt
- **Alle ~674 Regex-Regeln** aus den FUZZY_MAP_pre-Dateien greifen nicht
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro 和 Windows** 具有 identischem 源代码的功能

说明： Vosk liefert“mal sehen ob es schwitzt bretzfeld”→ sollte nach Regelanwendung korrigiert werden，wird aber unverändert ausgegeben。

---

## 2. 系统管理

| |曼扎罗 ✅ | CachyOS ⚠️ |
|---|---|---|
|蟒蛇 | 3.14.2 | 3.14.3 |
|爪哇 | OpenJDK 17 | OpenJDK 17.0.18 |
|语言工具 | 6.6 | 6.6 6.6 | 6.6
| LT 端口 | 8082 | 8082 |
| WatchFiles-从开始 | 重新加载0 | früher viele（inzwischen behoben）|

---

## 3. Was bereits untersucht und ausgeschlossen wurde

### ✅ LanguageTool läuft korrekt
- LT 启动端口 8082
- 直接 Python-Aufruf 功能的隔离测试：
__代码_块_0__
- 问题：LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ 设置相关
__代码_块_1__

### ✅ 正则表达式缓存功能
__代码_块_2__

### ✅ Python 版本相同（3.14.x auf beiden Systemen）

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-问题behoben
Das Startskript `activate-venv_and_run-server.sh` enthielt：
__代码_块_3__
Das doppelte venv-Erstellen wurde entfernt。 Dadurch ist jetzt wieder ein Log vorhanden。

### ✅ 日志问题 behoben
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand。 Log-Datei 中的 Gelöst durch Umleitung (Empfehlung, noch nicht umgesetzt)：
__代码_块_4__

---

## 4. Wie die Pipeline funktioniert (wichtig zum Verstehen)

__代码_块_5__

### Warum LT nie aufgerufen wrd (bekannt):

在“apply_all_rules_may_until_stable”中：
__代码_块_6__

以及 `process_text_in_background.py` 中的 weiter oben：
__代码_块_7__

我记录的是 jedem Durchlauf：
__代码_块_8__

Das bedeutet: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**Offen:** Warum ist `full_text_replaced_by_rule` auf CachyOS immer `True`, auf Manjaro aber nicht？

---

## 5.Regelformat（zum Verständnis）

__代码_块_9__

格式：`(替换、regex_pattern、阈值、options_dict)`

`apply_all_rules_until_stable`版本：
- `编译的 regex.full match(current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → 部分匹配，设置 `full_text_replaced_by_rule` **nicht**

---

## 6. 自检 schlägt fehl (DEV_MODE)

Im DEV_MODE führt Aura beim Start automatisch Tests aus。 Auf CachyOS：
__代码_块_10__

**Wichtig:** Das Testpattern lautet `r'^geht cobit einen$'` (braucht "einen"), der Test-Input ist aber nur `'geht cobit'` → dieser spezifische Test ist fehlerhaft und beweist nichts über CachyOS. **Aber：** Alle anderen 测试了 CachyOS 和 Manjaro laufen 的测试。

---

## 7. 最新施里特：GLOBAL_debug_skip_list

Der vielversprechendste nächste Schritt ist `GLOBAL_debug_skip_list` zu aktivieren. Dieser Flag gibt `print()`-Ausgaben direkt auf stdout — unabhängig vom 日志记录系统。 Das zeigt Schritt für Schritt 处于 der Regelschleife Passiert 状态。

__代码_块_11__

Dann auf `True` setzen 和 Aura starten。打印 - 在终端上直接打印。

### 替代方案：Regelengine 的 Direkter Isolationstest

__代码_块_12__

---

## 8. Verdächtige Stellen 代码

### 8a。隐私污染发生的法律规定
在“apply_all_rules_until_stable”中：
__代码_块_13__
Das könnte dazu führen dass Logs unterdrückt werden und Verhalten anders ist。

### 8b。两个正则表达式功能
__代码_块_14__
Unterschiedliche Signaturen – könnte zu Verwirrung führen。

### 8c。 aura_engine.py 中的 NameError-Risiko
__代码_块_15__

---

## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

在 ` Correct_text_by_languagetool.py` 中：
- `get_lt_session_202601311817()` 参考 `_lt_session` 不存在 → `NameError` wenn aufgerufen
- ` Correct_text_by_languagetool_202601311818()` ist eine veraltete Kopie
- `adapter` mit `pool_connections=25` am Modulende wird nie verwendet

---

## 10. 自述文件是有效的

__代码_块_16__

承诺：“CachyOS 目前受到限制”

---

## 11. 相关日期

|达亭|相关 |
|---|---|
| `aura_engine.py` | Haupteinstiegspunkt、LT-Start、active_lt_url |
| `scripts/py/func/process_text_in_background.py` |雷格尔管道，LT-Aufruf |
| `scripts/py/func/start_languagetool_server.py` | LT-Start-Logik，哨兵 |
| `scripts/py/func/ Correct_text_by_languagetool.py` | LT HTTP-Aufruf | LT HTTP-Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE-负载 |
| `config/settings.py` | LANGUAGETOOL_PORT=8082，CHECK_URL |
| `config/settings_local.py` | DEV_MODE=True/False（本地化）|
| `config/filters/settings_local_log_filter.py` | LOG_ONLY、LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog（war lange leer wegen &-Bug）|
| `log/languagetool_server.log` | LT-服务器日志 |

---

## 12.希尔弗赖什·贝菲勒

__代码_块_17__

---

*Bericht erstellt am 20.03.2026 — 调试会议 mit Claude Sonnet 4.6*