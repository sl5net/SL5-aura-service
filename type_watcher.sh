#!/bin/bash
# type_watcher.sh

DIR_TO_WATCH="/tmp/sl5_dictation"

LOCKFILE="/tmp/type_watcher.lock"

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
LOGFILE="$SCRIPT_DIR/log/type_watcher.log"

AUTO_ENTER_FLAG="/tmp/sl5_auto_enter.flag" # The flag file for auto-enter

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
    echo "✅ Watcher starting in macOS mode (using fswatch and osascript)."
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
    echo "✅ Watcher starting in Linux mode (using inotifywait and xdotool)."
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
                    if [ -z "$CI" ]; then
                        LC_ALL=C.UTF-8 xdotool type --clearmodifiers --delay 0 --file "$f"
                    fi



                    GAME_WINDOW_ID=$(xdotool search --name "0 A.D." | head -1) # Replace "Your Game Window Name"

                    # LC_ALL=C.UTF-8 xdotool --window $GAME_WINDOW_ID clearmodifiers # Clear after typing too


                    # alt+i Alt+i
                    mapfile -t lines < "$f"
                    for line in "${lines[@]}"; do
                        # Remove leading/trailing whitespace from the line for robust comparison
                        trimmed_line=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')


                        if [[ "$trimmed_line" == 'alt+i' ]]; then
                            # LC_ALL=C.UTF-8 xdotool windowactivate $GAME_WINDOW_ID
                            sleep 0.01
                            LC_ALL=C.UTF-8 xdotool key --window $GAME_WINDOW_ID alt+i clearmodifiers # Clear after typing too
                            # LC_ALL=C.UTF-8 xdotool key alt+i
                            # LC_ALL=C.UTF-8 xdotool --clearmodifiers
                            sleep 0.1
                            echo "Sent alt+i" # Optional: for debugging/confirmation
                        fi

                        if [[ "$trimmed_line" == 'alt+w' ]]; then
        # LC_ALL=C.UTF-8 xdotool windowactivate --sync $GAME_WINDOW_ID
        # LC_ALL=C.UTF-8 xdotool windowactivate $GAME_WINDOW_ID
                            sleep 0.01
                            LC_ALL=C.UTF-8 xdotool key alt+w clearmodifiers # Clear after typing too
                            # LC_ALL=C.UTF-8 xdotool key alt+i
                            # LC_ALL=C.UTF-8 xdotool --clearmodifiers
                            sleep 1
                            echo "Sent alt+w" # Optional: for debugging/confirmation
                        fi

                        if [[ "$trimmed_line" == 'baue Haus' ]]; then

                        # printf "${line}"
                            LC_ALL=C.UTF-8 xdotool --clearmodifiers key h clearmodifiers # Clear after typing too
                            sleep 0.15
                            xdotool click --delay 10 --repeat 8 1
                            sleep 0.1
                            LC_ALL=C.UTF-8 --clearmodifiers                             echo "Baue Haus" # Optional: for debugging/confirmation einen
                        fi
                    done

                    rm "$f"

                    # if you want newline/return/enter at the end:
                    # LC_ALL=C.UTF-8 xdotool key Return

                    # log_message "INFO: Auto-Enter?"

                    # --- Conditional Enter Key ---
                    if [ -f "$AUTO_ENTER_FLAG" ] && [ "$(cat "$AUTO_ENTER_FLAG")" = "1" ]; then
                        # echo "INFO: Auto-Enter?"
                        log_message "INFO: Auto-Enter plugin is enabled. Pressing Return."
                        if [ -z "$CI" ]; then
                            LC_ALL=C.UTF-8 xdotool key Return
                        fi
                    fi
                    # --- End of Conditional Block ---



                fi
            done
        fi
    done
else
    echo "ERROR: Unsupported operating system '$OS_TYPE'. Exiting."
    exit 1
fi
