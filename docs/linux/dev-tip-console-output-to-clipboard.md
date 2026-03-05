# Dev Tip: Automatically Copy Console Output to Clipboard

**Category:** Linux / Shell Productivity  
**Platform:** Linux (zsh + Konsole/KDE)

---

## The Problem

When working with AI assistants, you often need to copy terminal output and paste it into the chat. This usually means:
1. Run command
2. Select output with mouse
3. Copy
4. Switch to browser
5. Paste

That's too many steps.

---

## The Solution: Auto-capture via `preexec` / `precmd`

Add this to your `~/.zshrc`:

```bash
# === AUTO-OUTPUT LOGGER ===
# Automatically saves console output to ~/t.txt and copies to clipboard.
# Toggle: set AUTO_CLIPBOARD=true/false
AUTO_CLIPBOARD=true

# Redirect stdout+stderr to ~/t.txt before each command
preexec() {
    case "$1" in
        sudo*|su*) return ;;
        *) exec > >(tee ~/t.txt) 2>&1 ;;
    esac
}

precmd() {
    # Restore stdout after command finishes
    exec >/dev/tty 2>&1
    if [ "$AUTO_CLIPBOARD" = "true" ] && [ -s ~/t.txt ]; then
        # Filter out ANSI escape codes and KDE Konsole title sequences
        cat ~/t.txt | sed 's/\][0-9]*;[^]]*\][0-9]*;//g; s/^[0-9]*;//g' \
            | xclip -selection clipboard
        echo "[📋 In Zwischenablage kopiert]"
    fi
}
```

Then reload:
```bash
source ~/.zshrc
```

### Result

After every command, the output is automatically in your clipboard — ready to paste into your AI chat with **Ctrl+V**.

The output is also always saved in `~/t.txt` for reference.

---

## How it works

| Part | What it does |
|------|-------------|
| `preexec()` | Runs before each command, redirects output to `~/t.txt` |
| `precmd()` | Runs after each command, restores stdout and copies to clipboard |
| `tee ~/t.txt` | Saves output to file while still showing it in terminal |
| `sed '...'` | Strips KDE Konsole title escape sequences (`]2;...`  `]1;`) |
| `xclip` | Copies cleaned output to clipboard |

---

## Requirements

```bash
# Install xclip if not present
sudo pacman -S xclip       # Manjaro/Arch
sudo apt install xclip     # Ubuntu/Debian
```

---

## ⚠️ What NOT to do

Do **not** use `fc -ln -1 | bash` to re-execute the last command:

```bash
# ❌ DANGEROUS - do not use!
precmd() {
    output=$(fc -ln -1 | bash 2>&1)  # Re-executes last command!
    echo "$output" | xclip -selection clipboard
}
```

This re-executes every command after it finishes, which can cause destructive side effects — for example overwriting files, re-running `git commit`, re-running `sed -i`, etc.

The `preexec`/`precmd` approach above captures output **during** execution — safe and reliable.
