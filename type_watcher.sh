#!/bin/bash
# type_watcher.sh

set -euo pipefail

DIR_TO_WATCH="/tmp/sl5_aura"
LOCKFILE="/tmp/type_watcher.lock"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOG_DIR="$SCRIPT_DIR/log"
LOGFILE="$LOG_DIR/type_watcher.log"

AUTO_ENTER_FLAG="/tmp/sl5_auto_enter.flag" # The flag file for auto-enter

speak_file_path="$HOME/projects/py/TTS/speak_file.py"



# --- START: Read Python config to conditionally disable speaker ---
PROJECT_ROOT="$HOME/projects/py/STT"
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python3"

# Read the setting from config.settings.py. Default to "ERROR" on failure.

PRIMARY_TTS_ENGINE=$($PYTHON_BIN -c "import sys; sys.path.append('$PROJECT_ROOT'); from config.settings import USE_AS_PRIMARY_SPEAK; print(USE_AS_PRIMARY_SPEAK)" 2>/dev/null) || PRIMARY_TTS_ENGINE="ERROR"


echo "PRIMARY_TTS_ENGINE=$PRIMARY_TTS_ENGINE"

# If the setting is ESPEAK, empty the path to disable the speaker script
if [[ "$PRIMARY_TTS_ENGINE" == "ESPEAK" ]]; then
    echo "Primary speak is ESPEAK, disabling external speaker script by clearing path."
    speak_file_path=""
fi
# --- END: Read Python config ---








if [ -e $speak_file_path ]
then
  echo " ok $speak_file_path exist"
else
    speak_file_path=''
    echo "$speak_file_path dont exist"
fi

# Ensure log directory exists
mkdir -p "$LOG_DIR"

log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}
log_message "Hello from Watcher"

# --- Lockfile-Logic
if [ -e "$LOCKFILE" ]; then
    pid=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$pid" ] && ps -p "$pid" > /dev/null; then
        msg="Watcher already runs (PID: $pid). Exiting."
        echo "$msg"
        log_message "$msg"
        exit 0
    fi
    rm -f "$LOCKFILE"
fi
echo $$ > "$LOCKFILE"
trap 'rm -f "$LOCKFILE"' EXIT

# --- Wait for the directory to be created by the main service ---
while [ ! -d "$DIR_TO_WATCH" ]; do
    sleep 0.5
done

# Function to get the title of the active window
get_active_window_title() {
    active_window_id=$(xdotool getactivewindow)
    xdotool getwindowname "$active_window_id"
}

OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Darwin" ]]; then
    # --- macOS Logic ---
    echo "✅ Watcher starting in macOS mode (using fswatch and osascript)."
    log_message "Watcher starting in macOS mode (using fswatch and osascript)."
    fswatch -0 "$DIR_TO_WATCH" | while read -d "" file; do
        if [[ "$file" == *tts_output_*.txt ]]; then
            osascript -e "tell application \"System Events\" to keystroke \"$(cat "$file")\""
            rm -f "$file"
        fi
    done
elif [[ "$OS_TYPE" == "Linux" ]]; then
    # --- Linux Logic ---
    echo "✅ Watcher starting in Linux mode (using inotifywait and xdotool)."
    log_message "Watcher starting in Linux mode (using inotifywait and xdotool)."

    while true; do
        inotifywait -q -e create,close_write "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"
        sleep 0.1

        # Use null-separated find for safer file handling (handles spaces/newlines)
        while IFS= read -r -d '' f; do
            [ -f "$f" ] || continue

            # Read lines into an array
            mapfile -t lines < "$f"
            for line in "${lines[@]}"; do
                trimmed_line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
                GAME_WINDOW_ID=$(xdotool search --name "0 A.D." | head -1 || true)

                if [[ -n "$GAME_WINDOW_ID" ]]; then
                    log_message "GAME_WINDOW_ID = $GAME_WINDOW_ID"
                    if [[ "$trimmed_line" == 'alt+i' ]]; then
                        LC_ALL=C.UTF-8 xdotool windowactivate "$GAME_WINDOW_ID"
                        sleep 0.2
                        log_message "Sende ALT+i explizit mit keydown/keyup"
                        LC_ALL=C.UTF-8 xdotool keydown --window "$GAME_WINDOW_ID" 64
                        sleep 0.05
                        LC_ALL=C.UTF-8 xdotool key --window "$GAME_WINDOW_ID" 31
                        sleep 0.05
                        LC_ALL=C.UTF-8 xdotool keyup --window "$GAME_WINDOW_ID" 64
                        sleep 0.1
                        log_message "Fertig mit ALT+i Sequenz"
                        log_message "Sent alt+i"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi

                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'alt+w' ]]; then
                        xte "keydown Alt_L" "keydown w" "keyup w" "keyup Alt_L"
                        log_message "Sent alt+w"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'ctrl+c' ]]; then
                        LC_ALL=C.UTF-8 xdotool key ctrl+c clearmodifiers
                        log_message "Sent ctrl+c"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'baue Haus' ]]; then
                        LC_ALL=C.UTF-8 xdotool key h
                        sleep 0.15
                        xdotool click --delay 10 --repeat 8 1
                        log_message "baue Haus"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'baue Lagerhaus' ]]; then
                        LC_ALL=C.UTF-8 xdotool key s
                        sleep 0.15
                        xdotool click --delay 10 --repeat 8 1
                        log_message "baue Lagerhaus"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'select iddle' ]]; then
                        xdotool keydown alt
                        xdotool type '#'
                        xdotool keyup alt
                        sleep 0.15
                        # xdotool click --delay 10 --repeat 8 1
                        log_message "select iddle"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    elif [[ "$trimmed_line" == 'baue Baracke' ]]; then
                        LC_ALL=C.UTF-8 xdotool key b
                        sleep 0.15
                        xdotool click --delay 10 --repeat 8 1
                        sleep 4
                        log_message "baue Baracke"
                        if [[ -n "$speak_file_path" ]]; then
                          python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                          sleep 0.01
                        fi
                        rm -f "$f"
                        continue
                    fi
                fi

                # Fallback: type file content (if not a special command)
                if [ -z "${CI:-}" ]; then
                    LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 0 --file "$f"
                    log_message "type --file $f"

                    # When you also want to have a voice feedback (means STT + littleAI + TTS )
                    #  Then you could use this repository:
                    # https://github.com/sl5net/gemini-tts/blob/main/speak_file.py
                    #  You could start the STT Service like so:
                    # ~/projects/py/TTS/scripts/restart_venv_and_run-server.sh
                    #  And add to type_watcher.sh the following line here:
                    if [[ -n "$speak_file_path" ]]; then
                      python3 "$speak_file_path" "$f" > /tmp/speak_error.log 2>&1
                      sleep 0.01
                    fi

                    rm -f "$f"
                    continue
                fi
            done



            rm -f "$f"

            # --- Conditional Enter Key ---
            window_title=$(get_active_window_title)
            if [[ -f "$AUTO_ENTER_FLAG" ]]; then
                regexLine=$(cat "$AUTO_ENTER_FLAG")
                if echo "$window_title" | grep -Eq "$regexLine"; then
                    log_message "INFO: Auto-Enter is enabled. Pressing Return."
                    if [ -z "${CI:-}" ]; then
                        LC_ALL=C.UTF-8 xdotool key Return
                    fi
                fi
            fi
        done < <(find "$DIR_TO_WATCH" -maxdepth 1 -type f -name 'tts_output_*.txt' -print0)
    done
else
    echo "ERROR: Unsupported operating system '$OS_TYPE'. Exiting."
    exit 1
fi
