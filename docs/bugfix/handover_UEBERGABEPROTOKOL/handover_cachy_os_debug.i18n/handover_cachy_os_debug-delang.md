#Übergabe-Bericht: CachyOS Debugging – Aura STT Post-Processing

**Datum:** 20. März 2026  
**Projekt:** `~/projects/py/stt` (Aura STT – Offline-Voice-to-Text-System)  
**Status:** Problem noch nicht gelöst – Übergabe an nächsten Mitarbeiter  

---

## 1. Problembeschreibung

Nach dem Wechsel auf **CachyOS** funktionieren in Aura folgende Dinge nicht mehr:

- **Rechtschreibkorrektur via LanguageTool** wird nicht ausgeführt
- **Alle ~674 Regex-Regeln** aus den FUZZY_MAP_pre-Dateien greifen nicht
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro und Windows** funktioniert alles mit identischem Source-Code

Beispiel: Vosk liefert „mal sehen ob es schwitzt bretzfeld“ → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

---

## 2. Systemumgebung

| | Manjaro ✅ | CachyOS ⚠️ |
|---|---|---|
| Python | 3.14.2 | 3.14.3 |
| Java | OpenJDK 17 | OpenJDK 17.0.18 |
| LanguageTool | 6,6 | 6,6 |
| LT-Port | 8082 | 8082 |
| WatchFiles-Reloads beim Start | 0 | früher viele (inzwischen behoben) |

---

## 3. Wurde bereits untersucht und ausgeschlossen

### ✅ LanguageTool läuft korrekt
- LT startet auf Port 8082
- Isolierter Test mit direktem Python-Aufruf funktioniert:
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- Problem: LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ Einstellungen korrekt
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

### ✅ Regex-Cache funktioniert
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

### ✅ Python-Version identisch (3.14.x auf beiden Systemen)

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-Problem behoben
Das Startskript `activate-venv_and_run-server.sh` enthielt:
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```
Das doppelte Venv-Erstellen wurde entfernt. Dadurch ist jetzt wieder ein Log vorhanden.

### ✅ Log-Problem behoben
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand. Gelöst durch Umleitung in Log-Datei (Empfehlung, noch nicht umgesetzt):
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

---

## 4. Wie die Pipeline funktioniert (wichtig zum Verstehen)

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

In „apply_all_rules_may_until_stable“:
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

Und weiter oben in `process_text_in_background.py`:
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

Das bedeutet: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**Offen:** Warum ist `full_text_replaced_by_rule` auf CachyOS immer `True`, auf Manjaro aber nicht?

---

## 5. Regelformat (zum Verständnis)

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

Format: „(Ersatz, Regex_Muster, Schwellenwert, Optionen_Dikt)“.

`apply_all_rules_until_stable` verwendet:
- `compiled regex.full match(current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → partieller Match, setzt `full_text_replaced_by_rule` **nicht**

---

## 6. Selbsttest schlägt fehl (DEV_MODE)

Im DEV_MODE führt Aura beim Start automatisch Tests aus. Auf CachyOS:
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```

**Wichtig:** Das Testmuster lautet „r'^geht cobit einen$“ (braucht „einen“), der Test-Input ist aber nur „geht cobit“ → Dieser spezielle Test ist fehlerhaft und beweist nichts über CachyOS. **Aber:** Alle anderen Tests schlagen auf CachyOS auch fehl, auf Manjaro laufen sie alle durch.

---

## 7. Der nächste Schritt: GLOBAL_debug_skip_list

Der vielversprechendste nächste Schritt ist `GLOBAL_debug_skip_list` zu aktivieren. Diese Flagge gibt `print()`-Ausgaben direkt auf stdout — unabhängig vom Logging-System. Das zeigt Schritt für Schritt was in der Regelschleife passiert.

```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```

Dann auf „True“ setzen und Aura starten. Die Druckausgaben erscheinen direkt im Terminal.

### Alternativ: Direkter Isolationstest der Regelengine

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
In „apply_all_rules_until_stable“:
```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```
Das könnte dazu führen, dass Protokolle unterdrückt werden und sich anders verhält.

### 8b. Zwei verschiedene Regex-Funktionen
```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```
Unterschiedliche Signaturen – könnte zu Verwirrung führen.

### 8c. NameError-Risiko in aura_engine.py
```python
if settings.USE_EXTERNAL_LANGUAGETOOL:
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # languagetool_process ← NIE gesetzt in diesem Zweig!

if not languagetool_process:  # ← NameError wenn USE_EXTERNAL_LANGUAGETOOL=True
    sys.exit(1)
```

---

## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

In „correct_text_by_lingualtool.py“:
- `get_lt_session_202601311817()` referenziert `_lt_session` die nicht existiert → `NameError` wenn aufgerufen
- `correct_text_by_lingualtool_202601311818()` ist eine veraltete Kopie
- `adapter` mit `pool_connections=25` am Modulede wird nie verwendet

---

## 10. README bereits aktualisiert

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```

Commit: „CachyOS derzeit eingeschränkt“

---

## 11. Relevante Dateien

| Datei | Relevanz |
|---|---|
| `aura_engine.py` | Haupteinstiegspunkt, LT-Start, active_lt_url |
| `scripts/py/func/process_text_in_background.py` | Regel-Pipeline, LT-Aufruf |
| `scripts/py/func/start_lingualtool_server.py` | LT-Start-Logik, Sentinel |
| `scripts/py/func/correct_text_by_lingualtool.py` | LT HTTP-Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE-Laden |
| `config/settings.py` | LANGUAGETOOL_PORT=8082, CHECK_URL |
| `config/settings_local.py` | DEV_MODE=True/False (lokal überschreiben) |
| `config/filters/settings_local_log_filter.py` | LOG_ONLY, LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog (war lange leer wegen &-Bug) |
| `log/lingualtool_server.log` | LT-Server-Log |

---

## 12. Hilfreiche Befehle

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

*Bericht erstellt am 20.03.2026 — Debugging-Session mit Claude Sonnet 4.6*