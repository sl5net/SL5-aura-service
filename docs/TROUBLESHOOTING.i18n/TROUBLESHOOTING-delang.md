# Fehlerbehebung bei SL5 Aura

## Schnelle Diagnose

Beginnen Sie immer hier:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## Problem: Aura startet nicht

**Symptom:** Kein Startton, kein Prozess in „pgrep“ sichtbar.

**Überprüfen Sie das Protokoll:**
```bash
tail -30 log/aura_engine.log
```

**Häufige Ursachen:**

| Fehler im Protokoll | Fix |
|---|---|
| `ModuleNotFoundError` | Führen Sie das Setup-Skript erneut aus: „bash setup/manjaro_arch_setup.sh“ |
| `Kein Modul namens 'objgraph'` | „.venv“ wurde neu erstellt – Neuinstallation: „pip install -r require.txt“ |
| `Adresse bereits verwendet` | Alten Prozess beenden: `pkill -9 -f aura_engine` |
| „Modell nicht gefunden“ | Führen Sie das Setup erneut aus, um fehlende Modelle herunterzuladen |

---

## Problem: Aura stürzt nach dem ersten Diktat ab

**Symptom:** Funktioniert einmal und endet dann lautlos.

**Überprüfen Sie stderr:**
```bash
cat /tmp/aura_stderr.log | tail -30
```

**Wenn Sie „Segmentierungsfehler“ oder „doppelt frei“ sehen:**

Dies ist ein bekanntes Problem auf Systemen mit glibc 2.43+ (CachyOS, neueres Arch).

```bash
sudo pacman -S mimalloc
```

mimalloc wird automatisch vom Startskript verwendet, sofern es installiert ist. Bestätigen Sie, dass es aktiv ist. Beim Start sollte Folgendes angezeigt werden:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## Problem: Auslösetaste bewirkt nichts

**Symptom:** Sie drücken den Hotkey, aber es passiert nichts – kein Ton, kein Text.

**Überprüfen Sie, ob der Datei-Watcher läuft:**
```bash
pgrep -a type_watcher
```

Wenn nichts angezeigt wird, starten Sie Aura neu:
```bash
./scripts/restart_venv_and_run-server.sh
```

**Überprüfen Sie, ob die Triggerdatei erstellt wird:**
```bash
ls -la /tmp/sl5_record.trigger
```

Wenn die Datei nie erstellt wird, funktioniert Ihre Hotkey-Konfiguration (CopyQ / AHK) nicht.
Weitere Informationen finden Sie im Abschnitt zur Hotkey-Einrichtung in [README.md](../../README.i18n/README-delang.md#configure-your-hotkey).

---

## Problem: Text erscheint, aber ohne Korrekturen

**Symptom:** Das Diktat funktioniert, aber alles bleibt in Kleinbuchstaben geschrieben, es gibt keine Grammatikkorrekturen.

**Überprüfen Sie, ob LanguageTool ausgeführt wird:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

Wenn dies einen Fehler zurückgibt, wird LanguageTool nicht ausgeführt. Aura sollte damit beginnen
automatisch – überprüfen Sie das Protokoll auf Fehler im Zusammenhang mit LanguageTool:

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**Überprüfen Sie das LanguageTool-Protokoll:**
```bash
cat log/languagetool_server.log | tail -20
```

---

## Problem: Aura bleibt im DEV_MODE hängen

**Symptom:** Bei „DEV_MODE = 1“ bleibt Aura nach dem ersten Auslöser hängen und stoppt
antworten.

**Ursache:** Ein hohes Protokollvolumen von mehreren Threads überlastet das Protokollierungssystem.

**Fix:** Fügen Sie einen Protokollfilter in „config/filters/settings_local_log_filter.py“ hinzu:

```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"window_title",
    r":st:",
]
LOG_EXCLUDE = []
```

Speichern Sie die Datei – Aura lädt den Filter automatisch neu. Kein Neustart erforderlich.

---

## Problem: „plugins.zip“ wächst endlos / hohe CPU-Auslastung

**Symptom:** 100 % CPU, Lüfter auf Hochtouren, „plugins.zip“ wächst ohne anzuhalten.

**Ursache:** Der Secure Packer packt Dateien in einer Endlosschleife neu.

**Fix:** Stellen Sie sicher, dass „.blob“- und „.zip“-Dateien vom Zeitstempelscan ausgeschlossen sind.
Überprüfen Sie „scripts/py/func/secure_packer_lib.py“ in Zeile 86:

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

Wenn diese Zeile fehlt, fügen Sie sie hinzu.

---

## Problem: Regeln werden nicht ausgelöst

**Symptom:** Sie diktieren eine Triggerphrase, aber die Regel führt nichts aus.

**Checkliste:**

1. Ist die Regel in der richtigen Datei? (`FUZZY_MAP_pre.py` = vor LanguageTool,
`FUZZY_MAP.py` = danach)
2. Wird die Kartendatei gespeichert? Aura wird beim Speichern neu geladen – überprüfen Sie das Protokoll
„Erfolgreich neu geladen“.
3. Stimmt das Muster mit dem überein, was Vosk tatsächlich transkribiert? Überprüfen Sie das Protokoll auf
die rohe Transkription:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. Ist „only_in_windows“ eingestellt und das falsche Fenster ist aktiv?
5. Passt zuerst eine allgemeinere Regel? Regeln werden von oben nach unten verarbeitet –
Stellen Sie spezifische Regeln vor allgemeine Regeln.

---

## Sammeln von Protokollen für Fehlerberichte

Wenn Sie ein Problem melden, geben Sie bitte Folgendes an:

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

Posten an: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)