# CudaText Plugin: "Disk Wins" (Force Auto-Reload on External Change)

CudaText has no built-in option that silently reloads a file the moment it
changes on disk — every built-in "changed on disk" mode still shows some
kind of prompt (modal or modal-less) before reloading
(see `ui_notif_confirm` in `default.json`, values `0`-`4`, all of which
ask). This plugin closes that gap: **disk always wins**, no prompt, ever.

Archived here so nobody has to re-derive the CudaText plugin API for this
again. Source of truth for the plugin itself lives in
[`cuda_disk_wins/`](./cuda_disk_wins/) in this folder.

## What it does

- Polls every open, named file once per second (configurable via
  `TIMER_INTERVAL` in `__init__.py`).
- If a file's mtime on disk changed, the plugin re-reads it and calls
  `Editor.set_text_all()` — **overwriting any unsaved changes in the
  editor tab without asking**.
- Clears the "modified" flag afterwards (`PROP_MODIFIED = False`), so the
  tab looks clean, as if nothing ever diverged.
- Best-effort restores caret position and the top visible line after
  reload.
- Adds two commands under `Plugins → Disk Wins`:
  - `Toggle auto-reload on/off`
  - `Check now` (manual one-shot check)

## Why a plugin instead of a setting

CudaText's own file-watcher (`ui_notif`) only ever offers "ask" behaviors:

| `ui_notif_confirm` | Behavior                                          |
|---------------------|----------------------------------------------------|
| 0                    | modal-less prompt, always                          |
| 1                    | modal-less prompt, if editor modified or Undo not empty |
| 2                    | modal-less prompt, if editor modified               |
| 3                    | modal prompt, always                                |
| 4                    | modal prompt, if editor modified                    |

There is no value that means "reload automatically, no prompt, keep going."
Hence this small plugin, which runs its own polling loop and reloads
directly through the Python API.

## Installation

```bash
mkdir -p ~/.config/cudatext/py
cp -r cuda_disk_wins ~/.config/cudatext/py/
```

Restart CudaText.

**Important:** also disable CudaText's own change-notification dialog so
it doesn't fight with the plugin. In
`~/.config/cudatext/settings/user.json`:

```json
{
    "ui_notif": false
}
```

(Equivalent to `Options → Settings – user config` in the UI.) Restart
CudaText again after this change.

## Caveats

- This is intentionally destructive: unsaved editor edits are discarded
  silently the moment the file changes externally. That's the entire
  point of the plugin — don't install it if you sometimes want to keep
  local edits over external changes.
- Only reacts to changes in the file's mtime; typing in the editor itself
  does not trigger a reload (no feedback loop).
- If the file is deleted externally, the plugin does nothing until it
  reappears (no crash, no repeated reload attempts).
- Encoding is read via `PROP_ENC` and mapped to the closest Python codec;
  extend `ENC_MAP` in `__init__.py` if you use an encoding not already
  listed.

## Origin

Built for the "always prefer filesystem changes over unsaved editor
buffers, no confirmation" requirement discussed when setting up CudaText
via `yay -S cudatext-qt6-bin python` on Arch.
