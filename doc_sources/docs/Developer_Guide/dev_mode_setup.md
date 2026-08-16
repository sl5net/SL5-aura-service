# DEV_MODE Setup Guide

## The Problem

since we are compatible with Weyland we use `threading.Lock` for logging.

Now (21.3.'26 Sat) the rules for logging have changed. At Manjaro it was  unproblematic.

When `DEV_MODE = 1` is active, Aura produces hundreds of log entries per second 
from multiple threads. This can cause `SafeStreamToLogger` to deadlock, making 
Aura hang after the first dictation trigger.

## The Fix: Use LOG_ONLY Filter

When developing with `DEV_MODE = 1`, you **must** also configure a log filter in:
`config/filters/settings_local_log_filter.py`

### Minimal working filter for DEV_MODE:
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

## One-liner for settings_local.py
Add this comment as a reminder next to your DEV_MODE setting:
```python
DEV_MODE = 1  # ⚠️ Requires LOG_ONLY filter! See docs/dev_mode_setup.md
```

## Root Cause (since we are compatible with Weyland)
`SafeStreamToLogger` uses a `threading.Lock` to protect stdout writes.
Under high log load (DEV_MODE), lock contention causes deadlocks on systems 
with aggressive thread scheduling (e.g. CachyOS with newer kernels/glibc).
