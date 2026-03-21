# Übergabe-Bericht v2: CachyOS Debugging – Aura STT Post-Processing

**Datum:** 21. März 2026 (Session: 20.03. 14:00 – 21.03. 07:00 Uhr)  
**Projekt:** `~/projects/py/stt` (Aura STT – offline Voice-to-Text System)  
**Status:** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1. Ausgangssituation (Beginn der Session)

Auf **CachyOS** funktionierten folgende Dinge nicht:
- Keine Rechtschreibkorrektur via LanguageTool
- Keine Regex-Regeln griffen
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%, Lüfter auf Vollgas

Auf **Manjaro und Windows** alles funktionsfähig mit identischem Code.

---

## 2. Gelöste Probleme (in Reihenfolge der Entdeckung)

### ✅ Problem 1: Falsches venv beim Start
**Datei:** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env` wurde vor `python3 -m venv .venv` ausgeführt → falsches venv, fehlende Pakete  
**Fix:** Zeile `python3 -m venv .env` entfernt

---

### ✅ Problem 2: Vosk Double-Free (glibc 2.43)
**Ursache:** Vosk 0.3.45 hat latenten Double-Free Bug. glibc 2.43 auf CachyOS erkennt und terminiert den Prozess. Manjaro/ältere glibc ignorierte es still.  
**Fix:** mimalloc als alternativer Allocator:
```bash
sudo pacman -S mimalloc
```
Bereits im Startskript implementiert — sucht automatisch nach `/usr/lib/libmimalloc.so`.

**Verifikation:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ Problem 3: plugins.zip Endlos-Repack-Loop (100% CPU)
**Ursache:** `secure_packer_lib.py` scannte beim Timestamp-Check alle Dateien im Quellverzeichnis — inklusive `aura_secure.blob` (2,4 GB). Jeder Zugriff auf `.blob` aktualisierte dessen atime → Timestamp neuer als ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff auf `.blob` → Endlosschleife.  
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.  
**Fix:** `scripts/py/func/secure_packer_lib.py`, Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ Problem 4: e2e-Tests beim Start (89 parallele Prozesse)
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen, startete 89 parallele Prozesse → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.  
**Fix:** `aura_engine.py` Zeilen 1167-1168 auskommentiert:
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ Problem 5: `or True` Window-Title-Spam
**Datei:** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE or True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**Fix:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

---

### ✅ Problem 6: Gefährliche Regeln in empty_all
**Datei:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** Text löschen:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**Fix:** Alle gefährlichen Beispielregeln auskommentiert. Nur `LECKER_EXAKT` (harmlos) blieb aktiv.

---

### ✅ Problem 7: pygame Segfault (Thread-unsafe stdout)
**Ursache:** `SafeStreamToLogger.write()` schrieb `self.terminal.write(buf)` ohne Thread-Lock. Auf CachyOS (aggressiveres Thread-Scheduling) crashte pygame beim gleichzeitigen Zugriff aus mehreren Threads.  
**Stack trace:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
**Fix:** `aura_engine.py`, Klasse `SafeStreamToLogger`:
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

### ✅ Problem 8: os.path.relpath() Segfault
**Datei:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` triggerte intern stdout → pygame Segfault aus Thread  
**Fix:**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

---

## 3. Aktueller Stand

Aura läuft auf CachyOS und kann **4+ Diktate hintereinander** erfolgreich verarbeiten:
- ✅ Vosk-Transkription funktioniert
- ✅ Regelanwendung funktioniert  
- ✅ LanguageTool-Korrektur funktioniert (Großschreibung)
- ✅ Text wird geschrieben und gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Noch offenes Problem: Stiller Crash nach 1-5 Diktaten

**Symptom:** Aura stirbt ohne Segfault in stderr, kein klarer Python-Traceback sichtbar.

**Letzter bekannter Stack vor Crash (aus früherem stderr):**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

**Wahrscheinliche Ursachen:**
1. Weitere thread-unsafe Stellen in `SafeStreamToLogger` (z.B. `self.file_handler_ref.handle(record)`)
2. Unbehandelte Exception in einem Background-Thread die still schluckt
3. Maintenance-Task (`trigger_aura_maintenance.py`) der Subprozesse startet und crashed

**Nächster Diagnoseschritt:**
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**Weitere verdächtige Stelle** — `is_logging` Flag ist nicht thread-safe:
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
Besser:
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

## 5. Weitere bekannte Probleme (nicht kritisch)

### Ollama Connection Errors
Ollama läuft nicht auf CachyOS → `z_fallback_llm/ask_ollama.py` produziert hunderte Fehler-Logs.  
Temporär deaktiviert:
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

### plugins/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen — alte ZIP-Dateien und Backups.

### DEV_MODE_all_processing vs settings.DEV_MODE Inkonsistenz
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` lädt manchmal den falschen Wert. Nicht kritisch aber verwirrend.

### NameError in privaten Maps
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` erscheint bei jedem Diktat — ein NameError in einer privaten Map-Datei wird automatisch korrigiert. Kein Absturz, aber potenziell instabil.

---

## 6. Geänderte Dateien (Zusammenfassung)

| Datei | Änderung |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` und `.zip` vom Timestamp-Scan ausgeschlossen |
| `aura_engine.py` | e2e-Test auskommentiert; `threading.Lock` in `SafeStreamToLogger`; `or True` entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (temporär für Debugging) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln auskommentiert |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | Umbenannt zu `.py_bak` |

---

## 7. README bereits aktualisiert

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
Commit: `"CachyOS limited at the moment"`

---


Auf CachyOS ist pygame's stdout-Ersatz nicht thread-safe.
Der Fix ist ein threading Lock:
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

*Bericht aktualisiert am 21.03.2026 07:00 Uhr — Debugging-Session mit Claude Sonnet 4.6*  
*Session-Dauer: ~17 Stunden*
