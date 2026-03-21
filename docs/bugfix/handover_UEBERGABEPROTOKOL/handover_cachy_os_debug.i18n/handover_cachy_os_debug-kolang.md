# Übergabe-Bericht: CachyOS 디버깅 – Aura STT 사후 처리

**데이텀:** 20. März 2026XSPACEbreakX
**프로젝트:** `~/projects/py/stt`(Aura STT – 오프라인 음성-텍스트 시스템)  
**상태:** 문제 noch nicht gelöst – Übergabe an nächsten MitarbeiterXSPACEbreakX

---

## 1. 문제 해결

Nach dem Wechsel auf **CachyOS** 기능은 Aura folgende Dinge nicht mehr에서 작동됩니다.

- **Rechtschreibkorrektur via LanguageTool** wird nicht ausgeführt
- **모든 ~674 Regex-Regeln** aus den FUZZY_MAP_pre-Dateien greifen nicht
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro 및 Windows** funktioniert alles mit identischem 소스 코드

Beispiel: Vosk liefert ``mal sehen ob es schwitzt bretzfeld"` → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

---

## 2. 시스템움게붕

| | 만자로 ✅ | CachyOS ⚠️ |
|---|---|---|
| 파이썬 | 3.14.2 | 3.14.3 |
| 자바 | OpenJDK 17 | 오픈JDK 17.0.18 |
| 언어 도구 | 6.6 | 6.6 |
| LT 포트 | 8082 | 8082 |
| WatchFiles-Reloads 시작 시작 | 0 | 프뤼허 비엘레(inzwischen behoben) |

---

## 3. 예상치 못한 일과 ausgeschlossen wurde가 발생했나요?

### ✅ LanguageTool läuft korrekt
- 포트 8082로 LT 시작
- Python-Aufruf 기능 방향에 대한 Isolierter 테스트:
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- 문제: LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ 설정 확인
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

### ✅ 정규식 캐시 기능
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

### ✅ Python 버전 identisch(3.14.x auf beiden Systemen)

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-Problem behoben
Startskript `activate-venv_and_run-server.sh` 항목:
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```
Das doppelte venv-Erstellen wurde enfernt. Dadurch ist jetzt wieder ein Log vorhanden.

### ✅ 로그 문제 behoben
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand. Gelöst durch Umleitung in Log-Datei(Empfehlung, noch nicht umgesetzt):
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

---

## 4. Wie die Pipeline funktioniert(wichtig zum Verstehen)

```
Vosk (Speech-to-Text)
    ↓
process_text_in_background.py
    ↓
apply_all_rules_may_until_stable(text, GLOBAL_FUZZY_MAP_PRE, logger)
    ↓
apply_all_rules_until_stable(text, rules_map, logger)
    ↓  (gibt zurück: current_text, full_text_replaced_by_rule, skip_list, privacy_taint)
    ↓
if not regex_pre_is_replacing_all        # ← HIER wird LT blockiert
   and not is_only_number
   and 'LanguageTool' not in skip_list:
    correct_text_by_languagetool(...)    # ← wird nie erreicht
```

### Warum LT nie aufgerufen wird (bekannt):

`apply_all_rules_may_until_stable`에서:
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

`process_text_in_Background.py`에 더 자세한 내용을 추가하세요:
```python
regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe
# ...
if (not regex_pre_is_replacing_all ...):
    correct_text_by_languagetool(...)  # ← nur wenn False
```

Im Log steht bei jedem Durchlauf:
```
🚀Iterative-All-Rules: full_text_replaced_by_rule='True, skip_list='[]'
```

기본 사항: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**위법:** Warum은 CachyOS에 'True'로 설정된 'full_text_replaced_by_rule'이 아닙니다. Manjaro는 아무 것도 없나요?

---

## 5. Regelformat (zum Verständnis)

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

형식: `(교체, regex_pattern, 임계값, options_dict)`

`apply_all_rules_until_stable` 버전:
- `컴파일된 regex.full match(current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → 부분 일치, setzt `full_text_replaced_by_rule` **nicht**

---

## 6. 자체 테스트 schlägt fehl(DEV_MODE)

Im DEV_MODE führt Aura beim Start automatisch Tests aus. CachyOS에 대해:
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```

**위치:** Das Testpattern lautet `r'^geht cobit einen$'` (braucht "einen"), der Test-Input ist aber nur `'geht cobit'` → dieser spezifische Test ist fehlerhaft und beweist nichts über CachyOS. **Aber:** Alle anderen 테스트 schlagen auf CachyOS auch fehl, auf Manjaro laufen sie alle durch.

---

## 7. Nächste Schritt: GLOBAL_debug_skip_list

Der vielversprechendste nächste Schritt ist `GLOBAL_debug_skip_list` zu 활동입니다. Dieser Flag gibt`print()`-Ausgaben direct auf stdout — unabhängig vom Logging-System. Das zeigt Schritt für Schritt는 Regelschleife passiert에 있었습니다.

```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```

Dann auf 'True'가 설정되고 Aura가 시작됩니다. Die print-Ausgaben erscheinen direkt im Terminal.

### 대안: Regelengine의 Direkter Isolations 테스트

```python
# /tmp/test_rules.py
import sys, re
sys.path.insert(0, '/home/seeh/projects/py/stt')

# Regeln direkt laden
from config.maps.plugins.git.de_DE import FUZZY_MAP_pre  # Pfad anpassen
from scripts.py.func.process_text_in_background import apply_all_rules_until_stable
import logging
logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

result = apply_all_rules_until_stable('geht cobit einen', FUZZY_MAP_pre, logger)
print('Ergebnis:', result)
```

---

## 8. Verdächtige Stellen im Code

### 8a. Privacy_taint_occurred wird zu früh gesetzt
`apply_all_rules_until_stable`에서:
```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```
Das könnte dazu führen dass Logs unterdrückt werden und Verhalten anders ist.

### 8b. 정규식 기능 수정
```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```
Unterschiedliche Signaturen – könnte zu Verwirrung führen.

### 8c. aura_engine.py의 NameError-Risiko
```python
if settings.USE_EXTERNAL_LANGUAGETOOL:
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # languagetool_process ← NIE gesetzt in diesem Zweig!

if not languagetool_process:  # ← NameError wenn USE_EXTERNAL_LANGUAGETOOL=True
    sys.exit(1)
```

---

## 9. Bekannte Altlasten im Code(nicht kritisch, aber zu beachten)

`corright_text_by_언어tool.py`에서:
- `get_lt_session_202601311817()` 참조 `_lt_session`이 존재하지 않음 → `NameError` wenn aufgerufen
- `corright_text_by_언어tool_202601311818()` ist eine veraltete Kopie
- `어댑터` mit `pool_connections=25` 오전 모듈nde wird nie verwendet

---

## 10. README는 실제 작동을 보장합니다.

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```

커밋: `"현재 CachyOS는 제한되어 있습니다."`

---

## 11. 관련 다티엔

| 다테이 | 관련성 |
|---|---|
| `aura_engine.py` | Haupteinstiegspunkt, LT-Start, active_lt_url |
| `scripts/py/func/process_text_in_Background.py` | Regel-파이프라인, LT-Aufruf |
| `scripts/py/func/start_언어tool_server.py` | LT-Start-Logik, 센티넬 |
| `scripts/py/func/corright_text_by_언어tool.py` | LT HTTP-Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE-라덴 |
| `config/settings.py` | LANGUAGETOOL_PORT=8082, CHECK_URL |
| `config/settings_local.py` | DEV_MODE=True/False(현재 위치) |
| `config/filters/settings_local_log_filter.py` | LOG_ONLY, LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript(venv-Bug behoben) |
| `로그/aura_engine.log` | Hauptlog(war lange leer wegen &-Bug) |
| `로그/언어 도구_서버.log` | LT-서버-로그 |

---

## 12. 힐프레이헤 베펠레

```bash
# Aura starten:
~/projects/py/stt/scripts/restart_venv_and_run-server.sh

# venv aktivieren (Fish):
source ~/projects/py/stt/.venv/bin/activate.fish

# LT manuell starten:
java -Xms512m -Xmx4g \
  -jar ~/projects/py/stt/LanguageTool-6.6/languagetool-server.jar \
  --port 8082 --address 127.0.0.1 --allow-origin "*" &

# LT direkt testen:
curl -s -d "language=de-DE&text=Das ist ein gross Fehler" \
  http://127.0.0.1:8082/v2/check | python3 -m json.tool

# Laufende Prozesse:
pgrep -a -f "aura\|languagetool"

# Log live verfolgen:
tail -f log/aura_engine.log
```

---

*Bericht erstellt 오전 20.03.2026 — Claude Sonnet 4.6을 통한 디버깅 세션*