#!/bin/bash
# type_watcher.sh

DIR_TO_WATCH="/tmp/sl5_dictation"

LOCKFILE="/tmp/type_watcher.lock"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOGFILE="$SCRIPT_DIR/log/type_watcher.log"

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
trap "rm -f $LOCKFILE" EXIT

# --- Wait for the directory to be created by the main service ---
while [ ! -d "$DIR_TO_WATCH" ]; do
  sleep 0.5 # Wait half a second before checking again
done



# --- OS Detection and Main Loop ---
OS_TYPE=$(uname -s)

if [[ "$OS_TYPE" == "Darwin" ]]; then
    # --- macOS Logic ---
    echo "Watcher starting in macOS mode (using fswatch and osascript)."
    log_message "Watcher starting in macOS mode (using fswatch and osascript)."
    fswatch -0 "$DIR_TO_WATCH" | while read -d "" file; do
        if [[ "$file" == *tts_output_*.txt ]]; then
            # Use osascript to type the file content on macOS
            osascript -e "tell application \"System Events\" to keystroke \"$(cat "$file")\""
            rm "$file"
        fi
    done
elif [[ "$OS_TYPE" == "Linux" ]]; then
    # --- Linux Logic ---
    echo "Watcher starting in Linux mode (using inotifywait and xdotool)."
    log_message "Watcher starting in Linux mode (using inotifywait and xdotool)."

    while true; do
        inotifywait -q -e create,close_write "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"
        sleep 0.1

        files_to_process=$(ls -tr "$DIR_TO_WATCH"/tts_output_*.txt 2>/dev/null)

        if [ -n "$files_to_process" ]; then
            for f in $files_to_process; do
                if [ -f "$f" ]; then
                    # FIX: Pipe file content directly to xdotool to preserve UTF-8
                    # cat "$f" | LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 0 --file -
                    LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 0 --file "$f"
                    rm "$f"
                    # if you want newline/return/enter at the end:
                    # LC_ALL=C.UTF-8 xdotool key Return
                fi
            done
        fi
    done
else
    echo "ERROR: Unsupported operating system '$OS_TYPE'. Exiting."
    exit 1
fi
