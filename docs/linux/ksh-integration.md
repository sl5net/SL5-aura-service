# Ksh (Korn Shell) Integration

To make interacting with the STT (Speech-to-Text) CLI easier, you can add a shortcut function to your `~/.kshrc`. This allows you to simply type `s "your question"` in the terminal.

## Setup Instructions

1. Open your Ksh configuration with an editor you like:
   ```bash
   nano ~/.kshrc
   kate ~/.kshrc
   ```

2. Paste the following block at the end of the file:

```ksh
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
function s {
    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi
    update_github_ip
    TEMP_FILE=$(mktemp)
    SHORT_TIMEOUT_SECONDS=2
    LONG_TIMEOUT_SECONDS=70
    # Path shortcuts
    PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"
    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1
    EXIT_CODE=$?
    OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"
    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."
        start_service
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1
    # 2. Timeout (124) OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."
        TEMP_FILE_2=$(mktemp)
        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1
        EXIT_CODE_2=$?
        OUTPUT_2=$(cat "$TEMP_FILE_2")
        rm "$TEMP_FILE_2"
        echo "$OUTPUT_2"
        if [ $EXIT_CODE_2 -ne 0 ]; then
             echo "WARNUNG: Timeout > $LONG_TIMEOUT_SECONDS Sec. "
        fi
        return 0
    else
        echo "ERROR"
        echo "$OUTPUT"
        return $EXIT_CODE
    fi
}
```

3. Make sure Ksh loads your configuration file. Add or verify this in `~/.profile`:
   ```ksh
   export ENV="$HOME/.kshrc"
   ```

4. Reload your configuration:
   ```ksh
   . ~/.kshrc
   ```

## Ksh-Specific Notes

- Ksh supports both `function name { }` and `name() { }` syntax; the `function` keyword is used here for clarity.
- `local` is **not** supported in all Ksh variants (e.g. `ksh88`). Variables in the function above are therefore declared without `local`. If you are using `mksh` or `ksh93`, `typeset` can be used instead: `typeset TEMP_FILE=$(mktemp)`.
- The `ENV` variable controls which file Ksh sources for interactive sessions, similar to `.bashrc`.

## Features

- **Dynamic Paths**: Automatically finds the project root via the `/tmp` marker file.
- **Auto-Restart**: If the backend is down, it attempts to run `start_service` and local Wikipedia services.
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.
