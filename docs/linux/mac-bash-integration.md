# macOS Bash Shell Integration

> **Default shell before macOS Catalina (10.15).** Since Catalina, macOS ships with Zsh as the default shell. If you are on a modern Mac and have not changed your shell, see the [macOS Zsh Integration](./mac-zsh-integration.md) guide instead.
>
> You can check your current shell with:
> ```bash
> echo $SHELL
> ```

To make interacting with the STT (Speech-to-Text) CLI easier, you can add a shortcut function to your `~/.bash_profile`. This allows you to simply type `s "your question"` in the terminal.

## Setup Instructions

1. Open your Bash configuration with an editor you like:
   ```bash
   nano ~/.bash_profile
   open -e ~/.bash_profile   # opens in TextEdit
   ```

2. Paste the following block at the end of the file:

```bash
# --- STT Project Path Resolution ---
unalias s 2>/dev/null
s() {
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
    # 2. Timeout (124) OR success (0)
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
   source ~/.bash_profile
   ```

## macOS-Specific Notes

- **`timeout` is not built into macOS.** Install it via Homebrew before using this function:
  ```bash
  brew install coreutils
  ```
  After installation, `timeout` is available as `gtimeout`. Either add an alias or replace `timeout` with `gtimeout` in the function above:
  ```bash
  alias timeout=gtimeout
  ```
  Add the alias above the `s()` function in your `~/.bash_profile`.

- **macOS uses `~/.bash_profile` for login shells** (Terminal.app opens login shells by default), whereas Linux typically uses `~/.bashrc`. If you want the function available in all contexts, you can source one from the other:
  ```bash
  # Add to ~/.bash_profile:
  [ -f ~/.bashrc ] && source ~/.bashrc
  ```

- **macOS ships with Bash 3.2** (due to the GPLv3 license). This function is fully compatible with Bash 3.2+. If you need Bash 5, install it via Homebrew:
  ```bash
  brew install bash
  ```

- **Python path**: Make sure your virtual environment is set up at `$PROJECT_ROOT/.venv`. If you manage Python with `pyenv` or `conda`, adjust `PY_EXEC` accordingly.

## Features

- **Dynamic Paths**: Automatically finds the project root via the `/tmp` marker file.
- **Auto-Restart**: If the backend is down, it attempts to run `start_service` and local Wikipedia services.
- **Smart Timeouts**: Tries a quick 2-second response first, then falls back to a 70-second deep processing mode.
