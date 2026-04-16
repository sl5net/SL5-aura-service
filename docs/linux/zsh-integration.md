# Zsh Shell Integration

To make interacting with the STT (Speech-to-Text) CLI easier, you can add a shortcut function to your `~/.zshrc`. This allows you to simply type `s "your question"` in the terminal.

## Setup Instructions

1. Open your zsh configuration with a editor you like:
   ```bash
   nano ~/.zshrc
   kate ~/.zshrc
   ```

2. Paste the following block at the end of the file:

```zsh
# --- STT Project Path Resolution ---

unalias s 2>/dev/null
s() {
    LATEST_CHANGE=$(stat -c %Y /tmp/sl5_aura/sl5net_aura_project_root)
    PID=$(pgrep -f "scripts.py.service_api" | head -n 1)
    PROC_START=$(stat -c %Y /proc/$PID 2>/dev/null || echo 0)
    if [ "$LATEST_CHANGE" -gt "$PROC_START" ]; then
        echo "Code is newer. restart Api..."
        pkill -9 -f uvicorn 2>/dev/null
        start_service
    fi

    if [ $# -eq 0 ]; then
        echo "question <your question>"
        return 1
    fi

    update_github_ip

    local TEMP_FILE=$(mktemp)
    local SHORT_TIMEOUT_SECONDS=2
    local LONG_TIMEOUT_SECONDS=70

    # Path shortcuts
    local PY_EXEC="$PROJECT_ROOT/.venv/bin/python3"
    local CLI_SCRIPT="$PROJECT_ROOT/scripts/py/cli_client.py"

    # --- 1. try
    timeout $SHORT_TIMEOUT_SECONDS \
    "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
    --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE" 2>&1

    local EXIT_CODE=$?
    local OUTPUT=$(cat "$TEMP_FILE")
    rm "$TEMP_FILE"

    if echo "$OUTPUT" | grep -q "Verbindungsfehler" || ! pgrep -f "streamlit-chat.py" > /dev/null; then
        echo "Service-Check: Backend oder Frontend fehlt. Starte neu..."

        start_service

        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'
        local KIWIX_SCRIPT="$PROJECT_ROOT/config/maps/plugins/standard_actions/wikipedia_local/de-DE/kiwix-docker-start-if-not-running.sh"
        if [ -f "$KIWIX_SCRIPT" ]; then
            bash "$KIWIX_SCRIPT"
        fi
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++'

        echo "BITTE ERNEUT EINGEBEN: s $*"
        return 1

    # 2. Timeout (124) == OR success (0)
    elif [ $EXIT_CODE -eq 124 ] || [ $EXIT_CODE -eq 0 ]; then
        if [ $EXIT_CODE -eq 0 ]; then
            echo "$OUTPUT"
            return 0
        fi
        echo "answer > $SHORT_TIMEOUT_SECONDS sec. set Timeout= $LONG_TIMEOUT_SECONDS s..."

        local TEMP_FILE_2=$(mktemp)

        timeout $LONG_TIMEOUT_SECONDS \
        "$PY_EXEC" -u "$CLI_SCRIPT" "$*" \
        --lang "de-DE" --unmasked < /dev/null > "$TEMP_FILE_2" 2>&1

        local EXIT_CODE_2=$?
        local OUTPUT_2=$(cat "$TEMP_FILE_2")
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

3. Reload your configuration:
   ```bash
   source ~/.zshrc
   ```

## Features
- **Dynamic Paths**: Automatically finds the project root via the `/tmp` marker file.
- **Auto-Restart**: If the backend is down, it attempts to run `start_service` and local Wikipedia services.
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.
```
