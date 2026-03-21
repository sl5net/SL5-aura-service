# Übergabe-Bericht: Depuração CachyOS – Pós-processamento Aura STT

**Data:** 20 de março de 2026  
**Projekt:** `~/projects/py/stt` (Aura STT – sistema de voz para texto offline)  
**Status:** Problema noch nicht gelöst – Übergabe an nächsten Mitarbeiter  

---

## 1. Resolução de problemas

Nach dem Wechsel auf **CachyOS** funciona no Aura abaixo Dinge não mais:

- **Rechtschreibkorrektur via LanguageTool** não será usado
- **Todos ~674 Regex-Regeln** no FUZZY_MAP_pre-Dateien verde não
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro e Windows** funciona com código-fonte idêntico

Beispiel: Vosk liefert `"mal sehen ob es schwitzt bretzfeld"` → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

---

## 2. Configuração do sistema

| | Manjaro ✅ | CachyOS ⚠️ |
|---|---|---|
| Pitão | 3.14.2 | 3.14.3 |
| Java | OpenJDK 17 | OpenJDK 17.0.18 |
| Ferramenta de Idioma | 6.6 | 6.6 |
| Porta LT | 8082 | 8082 |
| WatchFiles-Reloads em Iniciar | 0 | früher viele (inzwischen behoben) |

---

## 3. Foi bereits untersucht und ausgeschlossen wurde

### ✅ LanguageTool mais recente
- LT iniciado na porta 8082
- Teste isolado com funções diretamente do Python:
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- Problema: LT wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ Configurações corretas
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

### ✅ Função Regex-Cache
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

### ✅ Versão Python idêntica (3.14.x no sistema anterior)

### ✅ inotify-Werte identisch (524288/16384)

### ✅ venv-Problem behoben
O nome do Startskript `activate-venv_and_run-server.sh`:
__CODE_BLOCO_3__
Das duas partes venv-Erstellen wurde entfernt. Dadurch ist jetzt wieder ein Log vorhanden.

### ✅ Log-Problem behoben
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt und stdout verschwand. Gelöst durch Umleitung in Log-Datei (Empfehlung, noch nicht umgesetzt):
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```

---

## 4. Quais são as funções do Pipeline (qualquer coisa para fazer)

__CODE_BLOCO_5__

### Warum LT não foi atualizado (bekannt):

Em `apply_all_rules_may_until_stable`:
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

E mais informações em `process_text_in_background.py`:
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

Im Log steht bei jedem Durchlauf:
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

A resposta é: `full_text_replaced_by_rule = True` → LT será alterado.

**Offen:** Warum é `full_text_replaced_by_rule` no CachyOS mais `True`, no Manjaro não é?

---

## 5. Formato Regel (para Verständnis)

__CODE_BLOCO_9__

Formato: `(substituição, regex_pattern, limite, opções_dict)`

`apply_all_rules_until_stable` versão:
- `compilado regex.full match(current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → partida Match, defina `full_text_replaced_by_rule` **não**

---

## 6. Autoteste Schlägt fehl (DEV_MODE)

Im DEV_MODE foi ativado Aura ao iniciar testes automaticamente. No CachyOS:
```python
regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe
# ...
if (not regex_pre_is_replacing_all ...):
    correct_text_by_languagetool(...)  # ← nur wenn False
```

**O que é importante:** O padrão de teste é `r'^geht cobit einen$'` (braucht "einen"), a entrada de teste é apenas `'geht cobit'` → este teste específico é fehlerhaft e não deve ser usado no CachyOS. **Aber:** Todos os outros testes foram realizados em CachyOS também fehl, em Manjaro laufen sie alle durch.

---

## 7. O próximo texto: GLOBAL_debug_skip_list

O texto mais próximo é `GLOBAL_debug_skip_list` para ser ativado. Este sinalizador gibt `print()`-Ausgaben diretamente no stdout — não instalado no Logging-System. Das zeigt Schritt für Schritt estava no Regelschleife passiert.

```
🚀Iterative-All-Rules: full_text_replaced_by_rule='True, skip_list='[]'
```

Dann auf `True` setzen e Aura starten. A impressão é enviada diretamente para o Terminal.

### Alternativa: Direkter Isolationstest do Regelengine

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

---

## 8. Verdächtige Stellen im Code

###8a. privacidade_taint_occurred é enviado para sua conta
Em `apply_all_rules_until_stable`:
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```
Das könnte dazu führen dass Logs unterdrückt werden und Verhalten other ist.

###8b. Duas funções Regex diferentes
```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```
Unterschiedliche Signaturen – könnte zu Verwirrung führen.

###8c. NameError-Risiko em aura_engine.py
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

## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

Em `correct_text_by_languagetool.py`:
- `get_lt_session_202601311817()` refere-se a `_lt_session` que não existe → `NameError` quando ativado
- `correct_text_by_languagetool_202601311818()` é uma cópia verdadeira
- `adapter` com `pool_connections=25` no módulo que não foi usado

---

## 10. README atualizado

```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```

Commit: `"CachyOS limitado no momento"`

---

## 11. Data relevante

| Data | Relevância |
|---|---|
| `aura_engine.py` | Ponto principal, LT-Start, active_lt_url |
| `scripts/py/func/process_text_in_background.py` | Regel-Pipeline, LT-Aufruf |
| `scripts/py/func/start_languagetool_server.py` | LT-Start-Logik, Sentinela |
| `scripts/py/func/correct_text_by_languagetool.py` | LT HTTP Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE carregado |
| `config/settings.py` | LANGUAGETOOL_PORT=8082, CHECK_URL |
| `config/settings_local.py` | DEV_MODE=Verdadeiro/Falso (definição local) |
| `config/filtros/settings_local_log_filter.py` | LOG_ONLY, LOG_EXCLUDE |
| `scripts/ativar-venv_and_run-server.sh` | Startskript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog (war lange leer wegen &-Bug) |
| `log/linguagemtool_server.log` | LT-Servidor-Log |

---

## 12. Hilfreiche Befehle

```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```

---

* Lançado em 20.03.2026 — Sessão de depuração com Claude Sonnet 4.6*