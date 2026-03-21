# Mise à jour v2 : Débogage CachyOS – Post-traitement Aura STT

**Donnée :** 21 mars 2026 (Session : 20.03. 14h00 – 21.03. 07h00)  
**Projet :** `~/projects/py/stt` (Aura STT – système voix-texte hors ligne)  
**Statut :** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1. Situation ausgangs (début de la session)

Auf **CachyOS** funktionierten folgende Dinge nicht:
- Keine Rechtschreibkorrektur via LanguageTool
- Keine Regex-Regeln griffen
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%, Lüfter auf Vollgas

Auf **Manjaro et Windows** toutes les fonctions sont compatibles avec le code identitaire.

---

## 2. Gelöste Probleme (dans Reihenfolge der Entdeckung)

### ✅ Problème 1 : Falsches venv beim Start
**Date :** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env` a été créé pour `python3 -m venv .venv` ausgeführt → faux venv, fehlende Pakete  
**Correction :** Mise à jour de `python3 -m venv .env`

---

### ✅ Problème 2 : Vosk Double-Free (glibc 2.43)
**Ursache :** Vosk 0.3.45 a latente d'un bug Double-Free. glibc 2.43 sur CachyOS fonctionne et termine le processus. Manjaro/autre glibc ignoré est toujours.  
**Correction :** mimalloc comme allocateur alternatif :
```bash
sudo pacman -S mimalloc
```
Il est mis en œuvre dans le script de démarrage — tel qu'automatiquement dans `/usr/lib/libmimalloc.so`.

**Vérification :**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ Problème 3 : plugins.zip Endlos-Repack-Loop (100 % CPU)
**Ursache :** `secure_packer_lib.py` scanne avec Timestamp-Check alle Dateien in Quellverzeichnis — incluant `aura_secure.blob` (2,4 Go). Jeder Zugriff auf `.blob` aktualisierte dessen atime → Timestamp new as ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff auf `.blob` → Endlosschleife.  
**Utilisation :** Les dates ZIP dans les versions de numérisation sont disponibles pour le retour au fichier Wachstum.  
**Correction :** `scripts/py/func/secure_packer_lib.py`, Zeile ~86 :
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ Problème 4 : e2e-Tests au démarrage (89 processus parallèles)
**Ursache:** `run_e2e_live_reload_func_test_v2()` est prêt à démarrer, démarre 89 processus parallèles → Temps, dernier processeur, résumé lors du premier test fehlschlug.  
**Correction :** `aura_engine.py` Date 1167-1168 commentaires :
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ Problème 5 : `ou True` Window-Title-Spam
**Date :** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE ou True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**Réparer:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

---

### ✅ Problème 6 : Gefährliche Regeln in empty_all
**Date :** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** Text löschen:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**Correction :** Tous les paramètres d'affichage gefährlichen sont commentés. Nur `LECKER_EXAKT` (harmlos) est actif.

---

### ✅ Problème 7 : pygame Segfault (sortie standard thread-unsafe)
**Ursache :** `SafeStreamToLogger.write()` écrit `self.terminal.write(buf)` sans Thread-Lock. Auf CachyOS (Thread-Scheduling agressif) crashe pygame en raison d'une mauvaise utilisation de plusieurs Threads.  
**Trace de la pile :**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
**Correction :** `aura_engine.py`, classe `SafeStreamToLogger` :
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

### ✅ Problème 8 : os.path.relpath() Segfault
**Date :** `scripts/py/func/log_memory_details.py`  
**Ursache :** `os.path.relpath()` déclenche la sortie standard interne → pygame Segfault sur Thread  
**Réparer:**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

---

## 3. Stand Aktueller

Aura läuft auf CachyOS et peut **4+ Diktate Hintereinander** erfolgreich verarbeiten :
- ✅ Fonctionnalité Vosk-Transkription
- ✅ Réglementation fonctionnelle  
- ✅ Fonctionnalité LanguageTool-Correction (Großschreibung)
- ✅ Text wird geschrieben und gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Problème le plus offensif : Stiller Crash après 1-5 Diktaten

**Symptôme :** Aura s'active sans erreur de segment en mode normal, mais la barre d'affichage Python-Traceback est plus claire.

**Letzer bekannter Stack vor Crash (aus früherem stderr) :**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

**Wahrscheinliche Ursachen:**
1. Autres threads non sécurisés dans `SafeStreamToLogger` (par exemple `self.file_handler_ref.handle(record)`)
2. Exception non autorisée dans un fil de fond qui reste toujours un problème
3. La tâche de maintenance (`trigger_aura_maintenance.py`) du sous-projet a démarré et s'est écrasée

**Nächster Diagnosticschritt:**
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**Nous avons d'autres étoiles** — L'indicateur `is_logging` n'est pas thread-safe :
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
Besser :
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

## 5. Nous rencontrons un problème (nicht kritisch)

### Erreurs de connexion Ollama
Ollama ne fonctionne pas sur CachyOS → `z_fallback_llm/ask_ollama.py` produit plusieurs Fehler-Logs.  
Désactivation temporaire :
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

### plugins/ Verzeichnis zu groß (2,8 Go)
Braucht Aufräumen — autres fichiers ZIP et sauvegardes.

### DEV_MODE_all_processing vs settings.DEV_MODE Incompatibilité
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` fonctionne avec de fausses valeurs. Nicht kritisch aber verwirrend.

### NameError dans les cartes privées
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` s'applique à chaque Diktat — une NameError dans une date de carte privée sera automatiquement corrigée. Kein Absturz, mais potentiellement instabil.

---

## 6. Geänderte Dateien (Zusammenfassung)

| Datei | À propos |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` et `.zip` pour l'analyse d'horodatage |
| `aura_engine.py` | Commentaires e2e-Test ; `threading.Lock` dans `SafeStreamToLogger` ; `ou True` entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (temporaire pour le débogage) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Réglementations Catch-All variées commentées |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | Remplacement de `.py_bak` |

---

## 7. README est actualisé

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
Commit : `"CachyOS limité pour le moment"`

---


Auf CachyOS est la sortie standard de Pygame qui n'est pas thread-safe.
Le correctif est un verrouillage de thread :
bashsed -n '418,422p' aura_engine.py



## 8. Hilfreiche Befehle

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

* Mise à jour le 21.03.2026 à 07h00 — Session de débogage avec Claude Sonnet 4.6*  
*Durée de la session : ~17 heures*