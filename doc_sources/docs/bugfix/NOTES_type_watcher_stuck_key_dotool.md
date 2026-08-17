# Notes: type_watcher.sh stuck-key issue (dotool)

## Symptom
Shortly after a Manjaro reboot, on the first dictation after `sl5net Aura`
auto-started, a single character got stuck and repeated infinitely
(e.g. "n" repeated hundreds of times) until the trigger key was pressed
again as a manual workaround.

Observed once on 2026-07-21 ~09:44 (Tue), text: "Die Ideen niemand wird
mehr gefragt, aber es soll trotzdem genauso sein wie...nnnnn...".

## Timeline (proven via logs)
- 09:29:17 - `type_watcher.sh` started (log/type_watcher.log)
- 09:41:56 - dictation "ideen niemand wird mehr gefragt..." received
  (log/aura_engine.log, Thread-13/14)
- 09:42:03 - text finished processing (`best fuzzy score:0%`),
  presumably written to a `tts_output_*.txt` file
- ~09:42:04-09:42:09 - `type_watcher.sh` crashed (inferred: watchdog
  poll interval is 5s, see below)
- 09:42:09 - watchdog log (log/type_watcher_keep_alive.log):
  "WATCHDOG: 'type_watcher.sh' is not running. Starting it now."
- 09:42:13 - `type_watcher.sh` restarted (log/type_watcher.log)
- No `typed content of ...` entry for the "ideen niemand..." file was
  ever found in log/type_watcher.log — the typing of that specific
  text was never completed/logged.

## Root cause status
- CONFIRMED: `type_watcher.sh` crashed between finishing text
  processing (09:42:03) and the watchdog detecting it as not running
  (09:42:09). The watchdog (`type_watcher_keep_alive.sh`) only kills
  and restarts on a config-file timestamp change (`ts1`/`ts2`,
  confirmed unchanged in this incident) or restarts automatically when
  `pgrep -f "type_watcher.sh"` finds no process — i.e. this was very
  likely a self-crash, not an external kill.
- HYPOTHESIS (not proven): `set -euo pipefail` (type_watcher.sh line 5)
  caused the script to exit on some non-zero exit code inside the
  pipeline, possibly while `do_type()`'s `dotool` pipe (line 125) was
  mid-stream. If the bash process dies while streaming into `dotool`,
  the separate `dotoold` daemon (which keeps running independently)
  can be left with a key in a "down" state with no matching "up" ever
  received, causing OS-level key-repeat.
- NOT YET PROVEN: the exact command/line that caused the non-zero
  exit under `set -euo pipefail`. No stderr from the crashed
  `type_watcher.sh` process was captured (the watchdog calls it
  without any output redirection, `type_watcher_keep_alive.sh` line 79).
- The affected key was NOT always the same character across different
  occurrences of this bug (user report: previously "t" as well).

## Already investigated and ruled out
- Not a config-change-triggered restart (confirmed by user: config
  unchanged, and `ts1_old != ts1_new` check would log "Config changed").
- Not a duplicate autostart of `type_watcher.sh` overlapping with
  itself (only one "Hello from Watcher" entry preceded the crash).
- `do_type()`'s `dotool type` call is atomic per invocation and does
  not itself send per-character key down/up — ruling out `type_watcher.sh`
  application logic as the direct source of a stuck key under normal
  (non-crashing) operation.

## Fix already applied (fallback / mitigation, not root cause fix)
Both `cleanup()` in `type_watcher.sh` and `do_cleanup()` in
`keep-keys-up.sh` previously released only modifier keys (shift, ctrl,
alt, etc.) via `dotool`/`xdotool`. This did nothing for a stuck regular
key (letter, number, punctuation).

- `type_watcher.sh`: `cleanup()` now sends `dotool key <name>:up` for
  all letters, numbers, and common punctuation/whitespace keys, not
  just modifiers.
- `type_watcher.sh`: `INPUT_METHOD` is now exported after detection, so
  other scripts can see which backend (`dotool` / `xdotool`) is active.
- `keep-keys-up.sh`: `do_cleanup()` gained a `dotool` branch (using the
  `keyup` verb, no per-key delay, for performance) active only when
  `INPUT_METHOD=dotool`, mirroring the existing `xdotool keyup` call
  for modifiers.

This does not fix the underlying crash of `type_watcher.sh`; it only
ensures that if the crash happens again, a stuck key gets released on
the next cleanup pass (`--cleanup`, called after every `do_type()`, and
via the `trap cleanup EXIT INT TERM` handler) instead of repeating
indefinitely until a manual trigger-key press.

## Next steps if this happens again
- Capture stderr of `type_watcher.sh` on crash. Currently
  `type_watcher_keep_alive.sh` line 79 calls it with no redirection, so
  any bash error message is lost (goes to the watchdog's own
  stdout/stderr, wherever that is directed by the autostart mechanism).
- Consider a debug mode, e.g. `bash -x scripts/type_watcher/type_watcher.sh
  2>> log/type_watcher_debug.log`, toggled via an env var such as
  `TYPE_WATCHER_DEBUG=1`, to capture the exact failing line on the next
  crash.
- Check what starts `type_watcher_keep_alive.sh` at Manjaro boot
  (autostart `.desktop` file, systemd `--user` unit, etc.) and whether
  its stdout/stderr are captured anywhere.
- If reproducible, test whether the crash correlates with
  `dotoold` still initializing right after boot (see the `sleep 0.1`
  at type_watcher.sh line 8 and the `dotoold` startup loop at lines
  102-110).
