# Übergabe-Bericht v2: Depuración de CachyOS – Postprocesamiento Aura STT

**Fecha:** 21. marzo 2026 (Sesión: 20.03. 14:00 – 21.03. 07:00 horas)  
**Proyecto:** `~/projects/py/stt` (Aura STT – Sistema de voz a texto sin conexión)  
**Estado:** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1. Ausgangssituation (Comienzo de la sesión)

Las siguientes funciones de **CachyOS** no son:
- Keine Rechtschreibkorrektur a través de LanguageTool
- Keine Regex-Regeln grifo
- Aura stürzte nach erstem Diktat sofort ab
- CPU activada al 100%, Lüfter auf Vollgas

En **Manjaro y Windows** todas las funciones con código de identificación.

---

## 2. Gelöste Probleme (en Reihenfolge der Entdeckung)

### ✅ Problema 1: Falsches venv beim Inicio
**Fecha:** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env` está disponible para `python3 -m venv .venv` ausgeführt → falsches venv, fehlende Pakete  
**Solución:** Se cambia `python3 -m venv .env`

---

### ✅ Problema 2: Vosk Double-Free (glibc 2.43)
**Ursache:** Vosk 0.3.45 tiene un error de doble liberación. glibc 2.43 en CachyOS se activa y finaliza el proceso. Manjaro/ältere glibc ignorierte es still.  
**Solución:** mimalloc y asignador alternativo:
```bash
sudo pacman -S mimalloc
```
Bereits im Startskript implementiert — sucht automaticisch nach `/usr/lib/libmimalloc.so`.

**Verificación:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ Problema 3: plugins.zip Endlos-Repack-Loop (100% CPU)
**Ursache:** `secure_packer_lib.py` escaneado en Timestamp-Check alle Dateien im Quellverzeichnis — incluido `aura_secure.blob` (2,4 GB). Jeder Zugriff auf `.blob` actualiza desde un tiempo → Marca de tiempo nunca como ZIP → Repack → Filesystem-Event → Map-Reload → Zugriff auf `.blob` → Endlosschleife.  
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.  
**Solución:** `scripts/py/func/secure_packer_lib.py`, Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ Problema 4: e2e-Tests beim Start (89 paralelo proceso)
**Ursache:** `run_e2e_live_reload_func_test_v2()` cuando se inicia el inicio, se inicia el proceso paralelo 89 → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.  
**Reparación:** `aura_engine.py` Comentarios 1167-1168:
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ Problema 5: `o Verdadero` Título de ventana-Spam
**Fecha:** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE o True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**Arreglar:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```

---

### ✅ Problema 6: Gefährliche Regeln en vacío_todo
**Fecha:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** Texto löschen:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**Solución:** Alle gefährlichen Beispielregeln auskommentiert. Nur `LECKER_EXAKT` (harmlos) blieb aktiv.

---

### ✅ Problema 7: pygame Segfault (salida estándar no segura para subprocesos)
**Ursache:** `SafeStreamToLogger.write()` escribe `self.terminal.write(buf)` sin Thread-Lock. Auf CachyOS (programación de subprocesos agresiva) bloquea pygame cuando se bloquea el tiempo en otros subprocesos.  
**Seguimiento de pila:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```
**Solución:** `aura_engine.py`, clase `SafeStreamToLogger`:
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

### ✅ Problema 8: os.path.relpath() Segfault
**Fecha:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` activa la salida estándar interna → pygame Segfault en Thread  
**Arreglar:**
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```

---

## 3. Soporte Aktueller

Aura läuft auf CachyOS y kann **4+ Diktate hindereinander** erfolgreich verarbeiten:
- ✅ Función de transcripción Vosk
- ✅ Función reglamentaria  
- ✅ Función LanguageTool-Korrektur (Großschreibung)
- ✅ Texto wird geschrieben und gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Noch offenes Problem: Stiller Crash nach 1-5 Diktaten

**Síntoma:** Aura agitada sin Segfault en stderr, no es clara la barra de seguridad de Python-Traceback.

**Permita que Stack vor Crash (aus früherem stderr):**
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

**Wahrscheinliche Ursachen:**
1. Agregar archivos no seguros para subprocesos en `SafeStreamToLogger` (por ejemplo, `self.file_handler_ref.handle(record)`)
2. Excepción no deseada en un hilo de fondo que todavía está bloqueado
3. La tarea de mantenimiento (`trigger_aura_maintenance.py`) el subproceso se inició y falló

**Nächster Diagnoseschritt:**
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

**Weitere verdächtige Stelle** — `is_logging` La bandera no es segura para subprocesos:
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
mejor:
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

### Errores de conexión de Ollama
Ollama no aparece en CachyOS → `z_fallback_llm/ask_ollama.py` produce hundentes Fehler-Logs.  
Desactivado temporalmente:
```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

### complementos/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen: alte ZIP-Dateien y Backups.

### DEV_MODE_all_processing vs settings.DEV_MODE Inconsistencia
```
DEV_MODE=1, settings.DEV_MODE = 0
```
`dynamic_settings.py` mantiene el contenido falso. Nicht kritisch aber verwirrend.

### Error de nombre en mapas privados
`_apply_fix_name_error('FUZZY_MAP.py' Ninguno...)` se escribe según un dictado: un NameError en una fecha de mapa privada se corrige automáticamente. Kein Absturz, aber potenziell instabil.

---

## 6. Geänderte Dateien (Zusammenfassung)

| Fechai | Enderung |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` activado |
| `scripts/py/func/secure_packer_lib.py` | `.blob` y `.zip` del Timestamp-Scan ausgeschlossen |
| `aura_engine.py` | e2e-Test auskomentiert; `threading.Lock` en `SafeStreamToLogger`; `o Verdadero` entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (tiempo para depuración) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Comentarios sobre Gefährliche Catch-All-Regeln |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | Umbenannt zu `.py_bak` |

---

## 7. README actualizado

```markdown
*   **Linux (Wayland):** ⚠️ Likely supported, but not fully tested.
*   **Linux (CachyOS / Arch-based rolling release):** ⚠️ Partially supported.
    Post-processing rules and LanguageTool correction currently unreliable.
    Investigation ongoing. Manjaro (also Arch-based) works correctly.
```
Confirmación: `"CachyOS limitado por el momento"`

---


Auf CachyOS es el sustituto estándar de pygame que no es seguro para subprocesos.
El Fix es un bloqueo de roscado:
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

*Actualizado el 21.03.2026 07:00 h — Sesión de depuración con Claude Sonnet 4.6*  
*Sesión-Dauer: ~17 Stunden*