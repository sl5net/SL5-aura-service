# DEV_MODE-Setup-Anleitung

## Das Problem

Da wir mit Weyland kompatibel sind, verwenden wir „threading.Lock“ für die Protokollierung.

Jetzt (Sa. 21.3.26) haben sich die Regeln für die Protokollierung geändert. Bei Manjaro war es unproblematisch.

Wenn „DEV_MODE = 1“ aktiv ist, erzeugt Aura Hunderte von Protokolleinträgen pro Sekunde
aus mehreren Threads. Dies kann zu einem Deadlock von „SafeStreamToLogger“ führen
Aura hängt nach dem ersten Diktatauslöser.

## Die Lösung: Verwenden Sie den LOG_ONLY-Filter

Wenn Sie mit „DEV_MODE = 1“ entwickeln, **müssen** Sie auch einen Protokollfilter konfigurieren in:
`config/filters/settings_local_log_filter.py`

### Minimaler Arbeitsfilter für DEV_MODE:
```python
LOG_ONLY = [
    r"Successfully",
    r"CRITICAL",
    r"📢📢📢 #",
    r"Title",
    r"window",
    r":st:",
]
LOG_EXCLUDE = []
```

## Einzeiler für Settings_local.py
Fügen Sie diesen Kommentar als Erinnerung neben Ihrer DEV_MODE-Einstellung hinzu:
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## Grundursache (da wir mit Weyland kompatibel sind)
„SafeStreamToLogger“ verwendet eine „threading.Lock“, um stdout-Schreibvorgänge zu schützen.
Bei hoher Protokolllast (DEV_MODE) führt ein Sperrenkonflikt zu Deadlocks auf Systemen
mit aggressiver Thread-Planung (z. B. CachyOS mit neueren Kerneln/glibc).