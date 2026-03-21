# Remarque : Débogage CachyOS – Post-traitement Aura STT

**Donnée :** 20 mars 2026  
**Projet :** `~/projects/py/stt` (Aura STT – système voix-texte hors ligne)  
**Statut :** Problème non résolu – Übergabe an nächsten Mitarbeiter  

---

## 1. Description du problème

Lorsque la fonction **CachyOS** est activée dans Aura, cela n'a rien de plus :

- **Rechtschreibkorrektur via LanguageTool** qui n'est pas utilisé
- **Tous les ~674 Regex-Regeln** ne sont pas pris en compte dans le FUZZY_MAP_pre-Dateien
- Vosk-Transkriptionen werden **ungefiltert und unkorrigiert** ausgegeben (alles kleingeschrieben, keine Ersetzungen)
- **Auf Manjaro et Windows** fonctionnent avec le code source identifié

Exemple : Vosk liefert `"mal sehen ob es schwitzt bretzfeld"` → sollte nach Regelanwendung korrigiert werden, wird aber unverändert ausgegeben.

---

## 2. Gestion du système

| | Manjaro ✅ | CachyOS ⚠️ |
|---|---|---|
| Python | 3.14.2 | 3.14.3 |
| Java | OpenJDK 17 | OpenJDK 17.0.18 |
| Outil linguistique | 6.6 | 6.6 |
| Port LT | 8082 | 8082 |
| WatchFiles-Reloads dans Démarrer | 0 | früher viele (inzwischen behoben) |

---

## 3. Était bereits untersucht et ausgeschlossen wurde

### ✅ LanguageTool a été corrigé
- Démarrage LT sur le port 8082
- Test isolé avec la fonction Python-Aufruf directe :
  ```
  POST /v2/check → 200
  "Das ist ein gross Fehler" → "Das ist ein groß Fehler"
  ```
- Problème : LT Wird von Aura **gar nicht aufgerufen** (kein POST im LT-Log)

### ✅ Paramètres corrigés
```python
USE_EXTERNAL_LANGUAGETOOL = False
LANGUAGETOOL_PORT = 8082
LANGUAGETOOL_CHECK_URL = "http://127.0.0.1:8082/v2/check"
```

### ✅ Regex-Cache fonctionnel
```python
get_cached_regex(r'^test$', re.IGNORECASE)
# → re.compile('^test$', re.IGNORECASE)  ✓
```

### ✅ Version Python identique (3.14.x sur chaque système)

### ✅ inotify-Werte identisch (524288 / 16384)

### ✅ venv-Problème à venir
Le script de démarrage `activate-venv_and_run-server.sh` contient :
```bash
python3 -m venv .env   # ← falsch, wurde entfernt
python3 -m venv .venv  # ← korrekt, bleibt
```
Das double venv-Erstellen wurde entfernt. Dadurch ist jetzt wieder ein Log vorhanden.

### ✅ Problème de journalisation signalé
Aura schrieb kein Log weil `&` den Prozess in den Hintergrund schickt et stdout verschwand. Gelöst durch Umleitung in Log-Datei (Empfehlung, noch nicht umgesetzt) :
```bash
# In activate-venv_and_run-server.sh:
PYTHONDONTWRITEBYTECODE=1 python3 "$SCRIPT_TO_START" >> "$PROJECT_ROOT/log/aura_engine.log" 2>&1 &
```

---

## 4. Comment le pipeline fonctionne-t-il (sans problème)

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

### Warum LT n'est pas disponible (déclaré):

Dans `apply_all_rules_may_until_stable` :
```python
if full_text_replaced_by_rule:
    skip_list.append('LanguageTool')   # ← LT wird in skip_list gesetzt
    return new_processed_text, True, skip_list, ...
```

Et plus encore dans `process_text_in_background.py` :
```python
regex_pre_is_replacing_all = regex_pre_is_replacing_all_maybe
# ...
if (not regex_pre_is_replacing_all ...):
    correct_text_by_languagetool(...)  # ← nur wenn False
```

Je suis log steht bei jedem Durchlauf :
```
🚀Iterative-All-Rules: full_text_replaced_by_rule='True, skip_list='[]'
```

Cela signifie : `full_text_replaced_by_rule = True` → LT sera supprimé.

**Offen :** La question est que `full_text_replaced_by_rule` sur CachyOS soit `True`, mais sur Manjaro n'est-il pas ?

---

## 5. Format réglementaire (verständnis)

```python
# FUZZY_MAP_pre Einträge:
FUZZY_MAP_pre = [
    ('git commit ', r'^geht cobit einen$', 85, {'flags': re.IGNORECASE}),
    ('Sebastian', r'^(mein vorname|sebastian)$', 85, {'flags': re.IGNORECASE}),
]
```

Format : `(remplacement, regex_pattern, seuil, options_dict)`

`apply_all_rules_until_stable` fonctionne :
- `compilé regex.full match (current_text)` → setzt `full_text_replaced_by_rule = True`
- `compiled_regex.search(current_text)` → Partieller Match, setzt `full_text_replaced_by_rule` **pas**

---

## 6. Fonctionnement de l'auto-test (DEV_MODE)

Im DEV_MODE führt Aura beim Start automatisch Tests aus. Sur CachyOS :
```
ERROR - ❌ FAIL: git
   Input:    'geht cobit'
   Expected: 'git commit'
   Got:      'geht cobit'
```

**Ce qui est :** Le modèle de test permet de "r'^geht cobit un $'` (braucht "einen"), l'entrée de test est seulement "geht cobit" → ce test spécifique est fait et n'est pas disponible sur CachyOS. **Aber :** Tous les autres tests sont effectués sur CachyOS auch fehl, sur Manjaro laufen sie alle durch.

---

## 7. Le prochain schéma : GLOBAL_debug_skip_list

Le niveau le plus élevé à proximité de Schritt est `GLOBAL_debug_skip_list` pour l'activer. Cet indicateur donne `print()` - directement sur la sortie standard - sans connexion avec le système de journalisation. Das zeigt Schritt für Schritt était dans la Regelschleife passiert.

```bash
# Wo ist GLOBAL_debug_skip_list definiert?
grep -n "GLOBAL_debug_skip_list" scripts/py/func/process_text_in_background.py | head -5
```

Puis auf `True` setzen et Aura starten. Die print-Ausgaben erscheinen direkt im Terminal.

### Alternative : Direkter Isolationstest der Regelengine

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

### 8a. Privacy_taint_occurred sera utilisé pour le prochain usage
Dans `apply_all_rules_until_stable` :
```python
privacy_taint_occurred = True  # ← wird bei JEDEM Match gesetzt, auch nicht-privaten!
```
Das könnte dazu führen dass Logs unterdrückt werden et Verhalten anders ist.

### 8b. Deux fonctions Regex polyvalentes
```python
get_cached_regex(pattern, flags)    # in apply_all_rules_until_stable
get_compiled_regex(pattern, logger) # in apply_all_rules_may_until_stable
```
Unterschiedliche Signaturen – könnte zu Verwirrung führen.

### 8c. NameError-Risiko dans aura_engine.py
```python
if settings.USE_EXTERNAL_LANGUAGETOOL:
    active_lt_url = settings.EXTERNAL_LANGUAGETOOL_URL
    # languagetool_process ← NIE gesetzt in diesem Zweig!

if not languagetool_process:  # ← NameError wenn USE_EXTERNAL_LANGUAGETOOL=True
    sys.exit(1)
```

---

## 9. Bekannte Altlasten im Code (nicht kritisch, aber zu beachten)

Dans `correct_text_by_lingualtool.py` :
- `get_lt_session_202601311817()` renvoie `_lt_session` qui n'existe pas → `NameError` lorsqu'il est affiché
- `correct_text_by_lingualtool_202601311818()` est une copie authentique
- `adapter` avec `pool_connections=25` am Modulende wird ni utilisé

---

## 10. README est actualisé

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```

Commit : `"CachyOS limité pour le moment"`

---

## 11. Dates pertinentes

| Datei | Pertinence |
|---|---|
| `aura_engine.py` | Point d'accès principal, LT-Start, active_lt_url |
| `scripts/py/func/process_text_in_background.py` | Regel-Pipeline, LT-Aufruf |
| `scripts/py/func/start_languetool_server.py` | LT-Start-Logik, Sentinelle |
| `scripts/py/func/correct_text_by_lingualtool.py` | LT HTTP-Aufruf |
| `scripts/py/func/config/dynamic_settings.py` | DEV_MODE-Chargé |
| `config/settings.py` | LANGUAGETOOL_PORT=8082, CHECK_URL |
| `config/settings_local.py` | DEV_MODE=True/False (affichage local) |
| `config/filters/settings_local_log_filter.py` | LOG_ONLY, LOG_EXCLUDE |
| `scripts/activate-venv_and_run-server.sh` | Startscript (venv-Bug behoben) |
| `log/aura_engine.log` | Hauptlog (war lange leer wegen &-Bug) |
| `log/langagetool_server.log` | Journal du serveur LT |

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

* Date de sortie le 20.03.2026 — Session de débogage avec Claude Sonnet 4.6*