# Übergabe-Bericht v2: Depuração CachyOS – Pós-processamento Aura STT

**Data:** 21 de março de 2026 (Sessão: 20.03.14h00 – 21.03.07h00)  
**Projekt:** `~/projects/py/stt` (Aura STT – sistema de voz para texto offline)  
**Status:** Maior Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabil  

---

## 1. Ausgangssituation (início da sessão)

As seguintes funções do **CachyOS** não são:
- Keine Rechtschreibkorrektur via LanguageTool
- Keine Regex-Regeln griffen
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%, Lüfter auf Vollgas

Em **Manjaro e Windows** todas as funções são executadas com código idêntico.

---

## 2. Gelöste Probleme (em Reihenfolge der Entdeckung)

### ✅ Problema 1: Falsches venv beim Start
**Data:** `scripts/activate-venv_and_run-server.sh`  
**Ursache:** `python3 -m venv .env` foi escrito para `python3 -m venv .venv` foi adicionado → falsches venv, pacote fehlende  
**Correção:** Zeile `python3 -m venv .env` entfernt

---

### ✅ Problema 2: Vosk Double-Free (glibc 2.43)
**Ursache:** Vosk 0.3.45 tem bug latente de dupla liberdade. glibc 2.43 no CachyOS é iniciado e encerra o processo. Manjaro/ältere glibc ignorado ainda está.  
**Correção:** mimalloc como alternativo Allocator:
```bash
sudo pacman -S mimalloc
```
O código inicial é implementado — automaticamente após `/usr/lib/libmimalloc.so`.

**Verificação:**
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

### ✅ Problema 3: plugins.zip Endlos-Repack-Loop (100% CPU)
**Ursache:** `secure_packer_lib.py` scannte beim Timestamp-Check alle Dateien im Quellverzeichnis — inclusive `aura_secure.blob` (2,4 GB). Um Zugriff em `.blob` é atualizado até o momento → Timestamp novo para ZIP → Repack → Evento do sistema de arquivos → Recarga de mapa → Zugriff em `.blob` → Endlosschleife.  
**Indicado:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.  
**Correção:** `scripts/py/func/secure_packer_lib.py`, Zeile ~86:
```python
# Vorher:
if file.startswith('.') or file.endswith('.pyc'):
# Nachher:
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
```

---

### ✅ Problema 4: e2e-Tests beim Start (89 paralelo Prozesse)
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen, startete 89 paralelo Prozesse → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.  
**Correção:** `aura_engine.py` Zeilen 1167-1168 adicionado:
__CODE_BLOCO_3__

---

### ✅ Problema 5: Spam de título de janela `ou verdadeiro`
**Data:** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE or True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/Sekunde  
**Consertar:**
```python
# from scripts.py.func.checks.live_reload_e2e_func_test import run_e2e_live_reload_func_test_v2
# run_e2e_live_reload_func_test_v2(logger, active_lt_url)
```

---

### ✅ Problema 6: Gefährliche Regeln em empty_all
**Data:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** Text löschen:
__CODE_BLOCO_5__
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**Correção:** Alle gefährlichen Beispielregeln auskommentiert. Nur `LECKER_EXAKT` (danos) está ativo.

---

### ✅ Problema 7: pygame Segfault (stdout inseguro para thread)
**Ursache:** `SafeStreamToLogger.write()` digite `self.terminal.write(buf)` sem Thread-Lock. No CachyOS (agendamento de thread agressivo) trava o pygame com o aumento de tempo de execução de mais Threads.  
**Rastreamento de pilha:**
```python
# Vorher:
if settings.DEV_MODE or True:
# Nachher:
if settings.DEV_MODE:
```
**Correção:** `aura_engine.py`, classe `SafeStreamToLogger`:
```python
('', r'^(?!Haus).*$', 5, {'flags': re.IGNORECASE}),      # löscht alles außer "Haus"
('', r'^(?!Schach|Matt|bad|Haus).*$', 5, ...),            # löscht alles außer diesen Wörtern
```

---

### ✅ Problema 8: os.path.relpath() Segfault
**Data:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` aciona stdout interno → pygame Segfault em Thread  
**Consertar:**
```
process_text_in_background.py → load_maps_for_language → logging.info()
→ SafeStreamToLogger.write() → self.terminal.write() → pygame SEGFAULT
```

---

## 3. Suporte Aktueller

Aura läuft auf CachyOS und kann **4+ Diktate hintereinander** erfolgreich verarbeiten:
- ✅ Função Vosk-Transkription
- ✅ Função de configuração  
- ✅ Funcionalidade LanguageTool-Korrektur (grande)
- ✅ O texto foi escrito e desenvolvido
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Noch ofensas Problema: Stiller Crash nach 1-5 Diktaten

**Sintoma:** Aura agitada sem Segfault em stderr, sem definir a barra de rastreamento do Python.

** Letzter bekannter Stack vor Crash (aus früherem stderr): **
__CODE_BLOCO_9__

**Wahrscheinliche Ursachen:**
1. Veja Stellen thread-inseguro em `SafeStreamToLogger` (z.B. `self.file_handler_ref.handle(record)`)
2. Exceção indevida em um thread de fundo que ainda é ruim
3. Tarefa de manutenção (`trigger_aura_maintenance.py`) que o subprocesso foi iniciado e travado

**Escrita de diagnóstico seguinte:**
```python
def __init__(self, ...):
    ...
    self._lock = threading.Lock()  # NEU

def write(self, buf):
    ...
    with self._lock:               # NEU
        self.terminal.write(buf)
```

**Mais estrelas válidas** — `is_logging` O sinalizador não é thread-safe:
```python
# Vorher:
caller_file_and_line = f"{os.path.relpath(frame_info.filename)}:{frame_info.lineno}"
# Nachher:
caller_file_and_line = f"{os.path.basename(frame_info.filename)}:{frame_info.lineno}"
```
Besser:
```
process_text_in_background.py:480 in load_maps_for_language
→ apply_all_rules_may_until_stable:878
→ log4DEV / logging
→ pygame Segfault
```

---

## 5. Weitere bekannte Probleme (nicht kritisch)

### Erros de conexão do Ollama
Eu não ligo para CachyOS → `z_fallback_llm/ask_ollama.py` produz hunderte Fehler-Logs.  
Temporariamente desativado:
```bash
# Vollständige Ausgabe inkl. aller Warnings:
cd ~/projects/py/stt
source .venv/bin/activate.fish
LD_PRELOAD=/usr/lib/libmimalloc.so python3 -W all aura_engine.py 2>&1 | tee /tmp/aura_full.log

# Nach Crash:
tail -50 /tmp/aura_full.log
```

### plugins/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen – outros dados ZIP e backups.

### DEV_MODE_all_processing vs settings.DEV_MODE Inconsistência
```python
# In SafeStreamToLogger.write():
if buf and not buf.isspace() and not self.is_logging:
    self.is_logging = True  # ← Race Condition! Kein Lock hier
```
`dynamic_settings.py` fornece um valor falso. Não há críticas a serem feitas.

### NameError em mapas privados
`_apply_fix_name_error('FUZZY_MAP.py' None ...)` segue o mesmo ditado — um NameError em um mapa privado será corrigido automaticamente. Kein Absturz, mas pode ser instável.

---

## 6. Geänderte Dateien (Zusammenfassung)

| Data | Änderung |
|---|---|
| `scripts/ativar-venv_and_run-server.sh` | `python3 -m venv .env` entfernt |
| `scripts/py/func/secure_packer_lib.py` | `.blob` e `.zip` da verificação de carimbo de data/hora |
| `aura_engine.py` | e2e-Test recomendado; `threading.Lock` em `SafeStreamToLogger`; `ou Verdadeiro` Entfernt |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (temporário para depuração) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln auskommentiert |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | Atualizado para `.py_bak` |

---

## 7. README atualizado

```python
with self._lock:
    if buf and not buf.isspace() and not self.is_logging:
        self.is_logging = True
        try:
            ...
        finally:
            self.is_logging = False
```
Commit: `"CachyOS limitado no momento"`

---


O CachyOS é o stdout-Ersatz do pygame não é thread-safe.
Der Fix é um bloqueio de threading:
bashsed -n '418.422p' aura_engine.py



## 8. Hilfreiche Befehle

```bash
mv config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py \
   config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py_bak
```

---

*Atualizado em 21.03.2026 07:00 Horas - Sessão de depuração com Claude Sonnet 4.6*  
*Sessão-Dauer: ~17 dias*