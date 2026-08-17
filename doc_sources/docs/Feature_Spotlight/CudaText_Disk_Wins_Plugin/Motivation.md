# Motivation: Why "Disk Wins"?

## The Problem in Aura grandma-mode

In [Aura Oma Mode](../../GettingStarted.md) (see line 67), Aura operates largely autonomously:
the user speaks commands, and Aura writes to files on its own —
configurations, scripts, log entries, generated text.

The following scenario happens constantly:

1. The user has a file open in the editor (e.g. a rule file or a script).
2. They forget the editor is still active and speak an Aura command.
3. Aura changes the file on disk.
4. The editor detects the external change — and **asks**.

This prompt is a **showstopper** in Oma Mode:
- The user may be sitting on the couch, using voice input,
  and cannot see or reach the dialog.
- Or they accidentally pressed a key in the editor, the buffer is now
  "modified", and every external change blocks with a
  "Reload? / Keep local?" dialog.
- The result: Aura keeps working, but the editor shows a stale version.
  The user thinks they are looking at the current file, but edits based
  on an old state — chaos is guaranteed.

## What We Need

Editor behavior that **always prioritizes the disk**.
When Aura (or any other tool) changes the file, the editor must
immediately and **without any prompt** show the new content.
Unsaved input in the editor may be silently discarded — because in
Oma Mode, Aura is the source of truth, not the human keyboard input.

## Why Standard Editors Fail

Almost all common editors (Kate, VS Code, Sublime Text, Notepad++,
Emacs, Vim, CudaText out-of-the-box) have a protection mechanism:
as soon as the buffer contains unsaved changes, they **always** ask
when an external change occurs. This is a feature for normal
developer work — but a bug for Aura Oma Mode.

This plugin closes exactly that gap for CudaText.

## Target Audience

- Users of Aura Oma Mode who view files in an editor in parallel.
- Automation scenarios where a process writes files and an editor
  serves only as a live viewer.
- Anyone for whom "disk always wins" is the desired behavior.
