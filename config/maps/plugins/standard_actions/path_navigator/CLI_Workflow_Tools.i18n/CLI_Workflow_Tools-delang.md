### Markdown-Dokument: „STT/settings/maps/plugins/standard_actions/path_navigator/CLI_Workflow_Tools.md“.

```markdown
CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# CLI Workflow Tools: FZF to Kate Integration

This document describes a high-efficiency command-line workflow that leverages the fuzzy file search implemented in the `path_navigator` plugin to quickly open files in the Kate editor.

## 1. Fast File Selection (Aura Command)

The `path_navigator` action uses the following Git-aware `fzf` command. Its purpose is to output a file path directly into the system clipboard.

**Command Logic:**
- Uses `git ls-files` inside a Git repository (excludes ignored files).
- Falls back to `find . -type f` outside a Git repository.
- Outputs the selected path to the clipboard using `xclip -selection clipboard`.

## 2. Fast File Execution (The 'k' Function)

To complete the loop, the custom shell function `k` is used. This function takes the path from the clipboard and instantly opens the file in `kate`.

### Implementation

Add the following function to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`):

```bash
# Funktion zum Öffnen eines Dateipfads aus der Systemzwischenablage in Kate
Funktion k {
# Überprüfen Sie, ob xclip verfügbar ist
Wenn ! Befehl -v xclip &> /dev/null; Dann
echo „Fehler: xclip ist erforderlich, aber nicht installiert.“
Rückkehr 1
fi
  
# 1. Holen Sie sich den Inhalt der Zwischenablage
CLIPBOARD_CONTENT=$(xclip -selection clipboard -o 2>/dev/null)
  
# Überprüfen Sie, ob die Zwischenablage leer ist
if [ -z "${CLIPBOARD_CONTENT}" ]; Dann
echo „Fehler: Zwischenablage ist leer. Nichts zum Öffnen.“
Rückkehr 1
fi

# 2. Auf mehrzeiligen Inhalt prüfen (stellt sicher, dass nur ein einziger Dateipfad verwendet wird)
LINE_COUNT=$(echo „${CLIPBOARD_CONTENT}“ | wc -l)
  
if [ "${LINE_COUNT}" -gt 1 ]; Dann
echo „Fehler: Zwischenablage enthält ${LINE_COUNT} Zeilen. Es werden nur einzeilige Dateipfade unterstützt.“
Rückkehr 1
fi
  
# 3. Drucken Sie den Befehl vor der Ausführung aus (Benutzer-Feedback)
echo „kate \“${CLIPBOARD_CONTENT}\““
  
# 4. Endgültige Ausführung
# Die doppelten Anführungszeichen um den Inhalt behandeln Dateinamen mit Leerzeichen korrekt.
# Das „&“ führt den Befehl im Hintergrund aus und gibt das Terminal frei.
kate „${CLIPBOARD_CONTENT}“ &
}
```

### Usage

1.  Use the `path_navigator` command (e.g., type `search file` in your trigger tool).
2.  Find and select the desired file (e.g., `src/main/config.py`).
3.  In your terminal, type `k` and press **ENTER**.
4.  The file opens instantly in Kate.
```