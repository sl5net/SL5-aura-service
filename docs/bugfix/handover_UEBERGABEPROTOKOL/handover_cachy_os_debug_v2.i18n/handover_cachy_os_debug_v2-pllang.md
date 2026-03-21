# Übergabe-Bericht v2: Debugowanie CachyOS – przetwarzanie końcowe Aura STT

**Data:** 21 marca 2026 r. (Sesja: 20.03. 14:00 – 21.03. 07:00 Uhr)XSPACEbreakX
**Projekt:** `~/projects/py/stt` (Aura STT – system zamiany głosu na tekst offline)XSPACEbreakX
**Stan:** Großer Fortschritt — 4+ erfolgreiche Diktate möglich, aber noch instabilXSPACEbreakX

---

## 1. Sytuacja ausgangstuation (sesja początkująca)

Auf **CachyOS** funkcje dodatkowe Dinge nicht:
- Keine Rechtschreibkorrektur za pomocą narzędzia LanguageTool
- Keine Regex-Regeln gryf
- Aura stürzte nach erstem Diktat sofort ab
- CPU dauerhaft bei 100%, Lüfter auf Vollgas

Auf **Manjaro i Windows** wszystkie funkcje z kodem identyfikacyjnym.

---

## 2. Gelöste Probleme (w Reihenfolge der Entdeckung)

### ✅ Problem 1: Błędne działanie przy starcie
**Data:** `skrypty/aktywuj-venv_and_run-server.sh`XSPACEbreakX
**Ursache:** `python3 -m venv .env` wurde vor `python3 -m venv .venv` ausgeführt → falsches venv, fehlende PaketeXSPACEbreakX
**Poprawka:** Zeile `python3 -m venv .env` odwróć

---

### ✅ Problem 2: Vosk Double-Free (glibc 2.43)
**Ursache:** Vosk 0.3.45 z ukrytym podwójnym błędem. glibc 2.43 na CachyOS zostanie utworzony i nigdyrt den Prozess. Manjaro/ältere glibc ignorowane jest nadal.XSPACEbreakX
**Poprawka:** mimalloc als alternatywny alokator:
__KOD_BLOKU_0__
Bereits im Startskript implementiert — sucht automatisch nach `/usr/lib/libmimalloc.so`.

**Weryfikacja:**
__KOD_BLOKU_1__

---

### ✅ Problem 3: plugins.zip Endlos-Repack-Loop (100% CPU)
**Ursache:** `secure_packer_lib.py` scannte beim Timestamp-Check alle Dateien im Quellverzeichnis — łącznie z `aura_secure.blob` (2,4 GB). Jeder Zugriff na `.blob` aktualny czas → Znacznik czasu nowy w ZIP → Przepakuj → Zdarzenie systemu plików → Map-Reload → Zugriff na `.blob` → Endlosschleife.XSPACEbreakX
**Zusätzlich:** ZIP-Dateien im Scan-Verzeichnis führten zu rekursivem Wachstum.XSPACEbreakX
**Poprawka:** `scripts/py/func/secure_packer_lib.py`, Zeile ~86:
__KOD_BLOKU_2__

---

### ✅ Problem 4: e2e-Tests beim Start (89 równoległych procesów)
**Ursache:** `run_e2e_live_reload_func_test_v2()` wurde beim Start aufgerufen, rozpocznij 89 równoległych procesów → Lüfter, CPU-Last, Absturz wenn erster Test fehlschlug.XSPACEbreakX
**Poprawka:** `aura_engine.py` Zeilen 1167-1168 auskommentiert:
__KOD_BLOKU_3__

---

### ✅ Problem 5: „lub prawdziwy” spam w tytule okna
**Data:** `scripts/py/func/process_text_in_background.py`  
**Ursache:** `if settings.DEV_MODE lub True:` → immer True → bei jedem Funktionsaufruf wurde window_title geprinted → hunderte Prints/SekundeXSPACEbreakX
**Naprawić:**
__KOD_BLOKU_4__

---

### ✅ Problem 6: Gefährliche Regeln w pustym_all
**Data:** `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py`  
**Ursache:** Aktive (nicht auskommentierte) Regeln die **jeden** Text löschen:
__KOD_BLOKU_5__
→ `full_text_replaced_by_rule = True` → LT wurde dauerhaft übersprungen  
**Poprawka:** Alle gefährlichen Beispielregeln auskommentiert. Nur `LECKER_EXAKT` (harmlos) blieb aktiv.

---

### ✅ Problem 7: pygame Segfault (standardowe wyjście niebezpieczne dla wątków)
**Ursache:** `SafeStreamToLogger.write()` schrieb `self.terminal.write(buf)` ohne Thread-Lock. Auf CachyOS (agresywne planowanie wątków) powoduje awarię pygame przy gleichzeitigen Zugriff aus mehreren Threads.XSPACEbreakX
**Ślad stosu:**
__KOD_BLOKU_6__
**Poprawka:** `aura_engine.py`, klasa `SafeStreamToLogger`:
__KOD_BLOKU_7__

---

### ✅ Problem 8: błąd Segfault os.path.relpath().
**Data:** `scripts/py/func/log_memory_details.py`  
**Ursache:** `os.path.relpath()` wyzwalacz intern stdout → pygame Segfault z ThreadXSPACEbreakX
**Naprawić:**
__KOD_BLOKU_8__

---

## 3. Stojak Aktueller

Aura läuft auf CachyOS und kann **4+ Diktate podpowiedzi** erfolgreich verarbeiten:
- ✅ Funkcja Vosk-Transkription
- ✅ Regelanwendung funktioniertXSPACEbreakX
- ✅ LanguageTool-Korrektur funktioniert (Großschreibung)
- ✅ Tekst wird geschrieben und gesprochen
- ⚠️ Aura stürzt nach 1-5 Diktaten noch ab

---

## 4. Brak przestępstw Problem: Stiller Crash nach 1-5 Diktaten

**Objaw:** Aura stirbt ohne Segfault w stderr, nie wymaga klarowania Python-Traceback sichtbar.

**Letzter bekannter Stack vor Crash (aus früherem stderr):**
__KOD_BLOKU_9__

**Wahrscheinliche Ursachen:**
1. Więcej plików Stellen niebezpiecznych dla wątków w `SafeStreamToLogger` (np. `self.file_handler_ref.handle(record)`)
2. Unbehandelte wyjątek w tle-wątek nadal jest schluckt
3. Zadanie konserwacji (`trigger_aura_maintenance.py`) zostało uruchomione i uległo awarii podprocesu

**Nächster Diagnoseschritt:**
__KOD_BLOKU_10__

**Weitere verdächtige Stelle** — `is_logging` Flaga jest bezpieczna dla wątków:
__KOD_BLOKU_11__
Besser:
__KOD_BLOKU_12__

---

## 5. Weitere bekannte Probleme (nicht kritisch)

### Błędy połączenia Ollama
Ollama läuft nicht auf CachyOS → `z_fallback_llm/ask_ollama.py` produziert hunderte Fehler-Logs.XSPACEbreakX
Tymczasowa deaktywacja:
__KOD_BLOKU_13__

### wtyczki/ Verzeichnis zu groß (2,8 GB)
Braucht Aufräumen — inne dane ZIP i kopie zapasowe.

### DEV_MODE_all_processing a ustawienia.DEV_MODE Inkonsistenz
__KOD_BLOKU_14__
`dynamic_settings.py` lädt manchmal den falschen Wert. Nicht kritisch aber verwirrend.

### Błąd nazwy w prywatnych mapach
`_apply_fix_name_error('FUZZY_MAP.py' Brak ...)` erscheint bei jedem Diktat — ein NameError in einer private Data Map-Datei wird automatyczne korygowanie. Kein Absturz, aber potenziell niestabilny.

---

## 6. Geänderte Dateien (Zusammenfassung)

| Data | Zakończenie |
|---|---|
| `scripts/activate-venv_and_run-server.sh` | `python3 -m venv .env` usuń |
| `scripts/py/func/secure_packer_lib.py` | `.blob` i `.zip` vom Timestamp-Scan ausgeschlossen |
| `aura_engine.py` | e2e-Test auskommentiert; `threading.Lock` w `SafeStreamToLogger`; `lub True` przejdź |
| `scripts/py/func/log_memory_details.py` | `os.path.relpath` → `os.path.basename` |
| `scripts/py/func/map_reloader.py` | `log_everything = True` (tymczasowe debugowanie) |
| `config/maps/plugins/empty_all/de-DE/FUZZY_MAP_pre.py` | Gefährliche Catch-All-Regeln auskommentiert |
| `config/maps/plugins/z_fallback_llm/de-DE/ask_ollama.py` | Umbenannt zu `.py_bak` |

---

## 7. README bereits aktualisiert

__KOD_BLOKU_15__
Zatwierdź: `„CachyOS jest obecnie ograniczony”`

---


Auf CachyOS to stdout-Ersatz nicht pygame, bezpieczny dla wątków.
Der Fix jest blokadą gwintowania:
bashsed -n '418,422p' aura_engine.py



## 8. Hilfreiche Befehle

__KOD_BLOKU_16__

---

*Bericht aktualności am 21.03.2026 07:00 Uhr — Sesja debugowania z Claude Sonnet 4.6*XSPACEbreakX
*Sesja-Dauer: ~17 Stunden*