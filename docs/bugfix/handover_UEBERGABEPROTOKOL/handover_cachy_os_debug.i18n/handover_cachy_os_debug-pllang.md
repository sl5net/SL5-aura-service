# Übergabe-Bericht: Debugowanie CachyOS – przetwarzanie końcowe Aura STT

**Data:** 20. marca 2026XSPACEbreakX
**Projekt:** `~/projects/py/stt` (Aura STT – system zamiany głosu na tekst offline)XSPACEbreakX
**Stan:** Problem noch nicht gelöst – Übergabe an nächsten MitarbeiterXSPACEbreakX

---

## 1. Opis problemu

Nach dem Wechsel auf **CachyOS** funktionieren in Aura folgende Dinge nicht mehr:

- **Rechtschreibkorrektur poprzez LanguageTool** wird nicht ausgeführt
- **Wszystkie ~674 Regex-Regeln** aus den FUZZY_MAP_pre-Dateien greifen nicht
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro und Windows** funkcje wszystkie z identyfikacją kodu źródłowego

Beispiel: Voskliefert `"mal sehen ob es schwitzt bretzfeld"` → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

---

## 2. Systemumgebung

| | Manjaro ✅ | CachyOS ⚠️ |
|---|---|---|
| Pythona | 3.14.2 | 3.14.3 |
| Jawa | OpenJDK 17 | OpenJDK 17.0.18 |
| Narzędzie językowe | 6,6 | 6,6 |
| Port LT | 8082 | 8082 |
| WatchFiles — ładuje ponownie przy starcie | 0 | früher viele (inzwischen behoben) |

---

## 3. Was bereits untersucht und ausgeschlossen wurde

### ✅ LanguageTool läuft korrekt
- LT start na porcie 8082
- Test izolacji z bezpośrednią funkcją Python-Aufruf:
__KOD_BLOKU_0__
- Problem: LT wird von Aura **gar nicht aufgerufen** (kein POST w LT-Log)

### ✅ Poprawiono ustawienia
__KOD_BLOKU_1__

### ✅ Funkcja Regex-Cache
__KOD_BLOKU_2__

### ✅ Identyfikacja wersji Pythona (3.14.x w systemie)

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-Problem behoben
Das Startskript `activate-venv_and_run-server.sh` w następujący sposób:
__KOD_BLOKU_3__
Das doppelte venv-Erstellen wurde entfernt. Dadurch ist jetzt wieder ein Log vorhanden.

### ✅ Problem z logiem behoben
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand. Gelöst durch Umleitung in Log-Datei (Empfehlung, noch nicht umgesetzt):
__KOD_BLOKU_4__

---

## 4. Wie die Pipeline funktioniert (wichtig zum Verstehen)

__KOD_BLOKU_5__

### Warum LT nie aufgerufen wird (bekannt):

W `apply_all_rules_may_until_stable`:
__KOD_BLOKU_6__

Więcej informacji w `process_text_in_background.py`:
__KOD_BLOKU_7__

Im Log steht bei jedem Durchlauf:
__KOD_BLOKU_8__

Das bedeutet: `full_text_replaced_by_rule = True` → LT wird übersprungen.

**Wykroczenie:** Warum ist `full_text_replaced_by_rule` auf CachyOS immer `True`, auf Manjaro aber nicht?

---

## 5. Regelformat (zum Verständnis)

__KOD_BLOKU_9__

Format: `(zastąpienie, wzór_regex, próg, dykt_opcji)`

Opcja `apply_all_rules_until_stable`:
- `skompilowany regex.full match(bieżący_tekst)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → dopasowanie częściowe, setzt `full_text_replaced_by_rule` **nicht**

---

## 6. Autotest schlägt fehl (DEV_MODE)

Im DEV_MODE führt Aura beim Rozpocznij automatyczne testy aus. Na CachyOS:
__KOD_BLOKU_10__

**Wichtig:** Das Testpattern lautet `r'^geht cobit einen$'` (braucht "einen"), wejście testowe jest aber nur `'geht cobit'` → dieser spezifische Test ist fehlerhaft und beweist nichts über CachyOS. **Aber:** Alle anderen Tests schlagen auf CachyOS auch fehl, auf Manjaro laufen sie alle durch.

---

## 7. Nowy plik Schritt: GLOBAL_debug_skip_list

Der vielversprechendste nächste Schritt ist `GLOBAL_debug_skip_list` zu aktivieren. Dieser Flag gibt `print()`-Ausgaben direkt auf stdout — unabhängig vom Logging-System. Das zeigt Schritt für Schritt był in der Regelschleife passiert.

__KOD_BLOKU_11__

Dann auf `True` setzen und Aura starten. Die print-Ausgaben erscheinen direkt im Terminal.

### Alternatywa: Direkter Isolationstest der Regelengine

__KOD_BLOKU_12__

---

## 8. Verdächtige Stellen im Code

### 8a. Privacy_taint_occurred wird zu früh gesetzt
W `apply_all_rules_until_stable`:
__KOD_BLOKU_13__
Das könnte dazu führen dass Logs unterdrückt werden und Verhalten anders ist.

### 8b. Zwei verschiedene Regex-Funktionen
__KOD_BLOKU_14__
Unterschiedliche Signaturen – könnte zu Verwirrung führen.

### 8c. NameError-Risiko w aura_engine.py
__KOD_BLOKU_15__

---

## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

W `correct_text_by_languagetool.py`:
- `get_lt_session_202601311817()` referenziert `_lt_session` die nicht istiert → `NameError` wenn aufgerufen
- `correct_text_by_languagetool_202601311818()` jest prawdziwą kopią
- `adapter` mit `pool_connections=25` am Modulende wird nie verwendet

---

## 10. README bereits aktualisiert

__KOD_BLOKU_16__

Zatwierdź: `„CachyOS jest obecnie ograniczony”`

---

## 11. Odpowiednie dane

| Data | Relewantność |
|---|---|
| `aura_engine.py` | Haupteinstiegspunkt, LT-Start, active_lt_url |
| `scripts/py/func/process_text_in_background.py` | Regel-Pipeline, LT-Aufruf |
| `scripts/py/func/start_languagetool_server.py` | LT-Start-Logik, Sentinel |
| `scripts/py/func/correct_text_by_languagetool.py` | LT HTTP-Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE-obciążony |
| `config/settings.py` | LANGUAGETOOL_PORT=8082, CHECK_URL |
| `config/settings_local.py` | DEV_MODE=Prawda/Fałsz (lokalny überschreiben) |
| `config/filters/settings_local_log_filter.py` | LOG_ONLY, LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog (wojna lange leer wegen &-Bug) |
| `log/languagetool_server.log` | Dziennik serwera LT |

---

## 12. Hilfreiche Befehle

__KOD_BLOKU_17__

---

*Bericht pojawił się 20.03.2026 — sesja debugowania z Claude Sonnet 4.6*