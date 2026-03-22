# Troubleshooting SL5 Aura

## Quick Diagnosis

Always start here:

```bash
# Check the main log:
tail -50 log/aura_engine.log

# Is Aura running?
pgrep -a -f aura_engine.py

# Is the file watcher running?
pgrep -a type_watcher
```

---

## Problem: Aura Does Not Start

**Symptom:** No startup sound, no process visible in `pgrep`.

**Check the log:**
```bash
tail -30 log/aura_engine.log
```

**Common causes:**

| Error in log | Fix |
|---|---|
| `ModuleNotFoundError` | Run setup script again: `bash setup/manjaro_arch_setup.sh` |
| `No module named 'objgraph'` | `.venv` was recreated — reinstall: `pip install -r requirements.txt` |
| `Address already in use` | Kill old process: `pkill -9 -f aura_engine` |
| `Model not found` | Re-run setup to download missing models |

---

## Problem: Aura Crashes After First Dictation

**Symptom:** Works once, then dies silently.

**Check stderr:**
```bash
python3 "aura_engine.py" 2>/tmp/aura_stderr.log &

cat /tmp/aura_stderr.log | tail -30
```

**If you see `Segmentation Fault` or `double free`:**

This is a known issue on systems with glibc 2.43+ (CachyOS, newer Arch).

```bash
sudo pacman -S mimalloc
```

mimalloc is automatically used by the start script if installed. Confirm it is active — you should see this on startup:
```
Info: Using mimalloc for improved memory management (/usr/lib/libmimalloc.so).
```

---

## Problem: Trigger Key Does Nothing

**Symptom:** You press the hotkey but nothing happens — no sound, no text.

**Check if the file watcher is running:**
```bash
pgrep -a type_watcher
```

If nothing appears, restart Aura:
```bash
./scripts/restart_venv_and_run-server.sh
```

**Check if the trigger file is being created:**
```bash
ls -la /tmp/sl5_record.trigger
```

If the file is never created, your hotkey configuration (CopyQ / AHK) is not working.
See the hotkey setup section in [README.md](../README.md#configure-your-hotkey).

---

## Problem: Text Appears But Without Corrections

**Symptom:** Dictation works but everything stays lowercase, no grammar fixes.

**Check if LanguageTool is running:**
```bash
curl -s http://127.0.0.1:8082/v2/languages | head -5
```

If this returns an error, LanguageTool is not running. Aura should start it
automatically — check the log for errors related to LanguageTool:

```bash
grep -i "languagetool\|LT\|8082" log/aura_engine.log | tail -10
```

**Check LanguageTool log:**
```bash
cat log/languagetool_server.log | tail -20
```

---

## Problem: Aura Hangs in DEV_MODE

**Symptom:** With `DEV_MODE = 1`, Aura hangs after the first trigger and stops
responding.

**Cause:** High log volume from multiple threads overloads the logging system.

**Fix:** Add a log filter in `config/filters/settings_local_log_filter.py`:

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

Save the file — Aura reloads the filter automatically. No restart needed.

---

## Problem: plugins.zip Grows Endlessly / High CPU

**Symptom:** 100% CPU, fans at full speed, `plugins.zip` grows without stopping.

**Cause:** The secure packer is repackaging files in an infinite loop.

**Fix:** Make sure `.blob` and `.zip` files are excluded from the timestamp scan.
Check `scripts/py/func/secure_packer_lib.py` around line 86:

```python
if file.startswith('.') or file.endswith('.pyc') or file.endswith('.blob') or file.endswith('.zip'):
    continue
```

If this line is missing, add it.

---

## Problem: Rules Not Firing

**Symptom:** You dictate a trigger phrase but the rule does nothing.

**Checklist:**

1. Is the rule in the correct file? (`FUZZY_MAP_pre.py` = before LanguageTool,
   `FUZZY_MAP.py` = after)
2. Is the map file saved? Aura reloads on save — check the log for
   `Successfully reloaded`.
3. Does the pattern match what Vosk actually transcribes? Check the log for
   the raw transcription:
   ```bash
   grep "Yielding chunk" log/aura_engine.log | tail -5
   ```
4. Is `only_in_windows` set and the wrong window is active?
5. Is a more general rule matching first? Rules are processed top-to-bottom —
   put specific rules before general ones.

---

## Collecting Logs for Bug Reports

When reporting an issue, please include:

```bash
# Last 100 lines of main log:
tail -100 log/aura_engine.log

# Crash output:
cat /tmp/aura_stderr.log

# System info:
uname -a
python3 --version
```

Post to: [GitHub Issues](https://github.com/sl5net/SL5-aura-service/issues)
