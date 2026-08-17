# Auto-Reload in Other Editors

This document describes how to set up automatic reloading on external
file changes in common editors — and why this is often **not enough**
in Aura Oma Mode.

---

## Kate (KDE)

### Setup

1. **Settings → Configure Kate → Open/Save → Advanced**
2. Enable:
   - **"Automatically reload files"**

### What works

- When the buffer is **unchanged**, Kate reloads the file immediately.
- This is sufficient for pure viewing mode.

### What does **not** work (and why it fails in Oma Mode)

- As soon as you press **a single key** in the buffer (even just a
  space or accidental keystroke), the buffer is considered "modified".
- From that moment on, Kate **always** asks on every external change:
  > "The file was changed externally. Do you want to reload it?"
- In Oma Mode, the user may not be at the computer or may not see the
dialog — Aura keeps writing, but the editor stays on the old version.
- **Kate has no setting** that silently discards unsaved buffer changes
  in favor of the disk version.

> **Bottom line:** Kate is unsuitable for Oma Mode as soon as the user
> accidentally types in the editor.

---

## VS Code

### Setup

In `settings.json`:

```json
{
    "files.autoSave": "afterDelay",
    "files.autoSaveDelay": 1000
}
```

### Limitations

- `autoSave` saves the buffer — it overwrites Aura's changes with the
  local version, not the other way around.
- A prompt still appears for unsaved changes.
- No option for "disk always wins".

---

## Emacs

```elisp
(global-auto-revert-mode t)
```

### Limitations

- Only reloads automatically when the buffer is unchanged.
- Asks when the buffer is modified.

---

## Vim / Neovim

```vim
set autoread
au FocusGained,BufEnter,CursorHold * :checktime
```

### Limitations

- `autoread` only reloads when the buffer is unchanged.
- Does not overwrite a `modified` buffer automatically.

---

## CudaText (without plugin)

In `user.json`:

```json
{
    "ui_notif": true,
    "ui_notif_confirm": 0
}
```

### Limitations

- All values of `ui_notif_confirm` (0–4) show some form of prompt —
  modal or modal-less.
- There is **no** value that means: "Reload immediately, never ask."
- Hence the `cuda_disk_wins` plugin is required.

---

## Overview

| Editor | Auto-Reload (unchanged) | Auto-Reload (modified) | License |
|--------|-------------------------|------------------------|---------|
| Kate | Yes | Always prompts | Open Source |
| VS Code | Yes | Always prompts | Open Source |
| Sublime Text | Yes | Always prompts | Proprietary |
| Emacs | Yes | Always prompts | Open Source |
| Vim | Yes | Always prompts | Open Source |
| CudaText (no plugin) | Yes | Always prompts | Open Source |
| **CudaText + Disk Wins** | Yes | **No prompt** | Open Source |

---

## Why No Editor Can Do This Out-of-the-Box

Silently discarding unsaved changes is considered a **massive data-loss
bug** in software development. No serious editor offers a setting
"overwrite my buffer without asking". This is correct and important —
for normal developer work.

In Aura Oma Mode, however, the priority is reversed: Aura is the source
of truth, and the human editor buffer is secondary. Therefore an
explicit plugin intervention is needed to enforce this behavior for
this specific use case.
