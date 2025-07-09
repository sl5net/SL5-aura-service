#!/bin/bash
# /type_watcher.sh

DIR_TO_WATCH="/tmp"
LOCKFILE="/tmp/type_watcher.lock"

# --- Lockfile-Logic
if [ -e "$LOCKFILE" ]; then
    pid=$(cat "$LOCKFILE" 2>/dev/null)
    if [ -n "$pid" ] && ps -p "$pid" > /dev/null; then
        # echo "Watcher already runs (PID: $pid). Exiting."
        exit 0
    fi
    rm -f "$LOCKFILE"
fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

while true; do
    inotifywait -q -e create,close_write "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"
    sleep 0.1

    files_to_process=$(ls -tr "$DIR_TO_WATCH"/tts_output_*.txt 2>/dev/null)

    if [ -n "$files_to_process" ]; then
        for f in $files_to_process; do
            if [ -f "$f" ]; then
                TEXT=$(cat "$f")
                rm "$f"
                if [ -n "$TEXT" ]; then
                    xdotool type --clearmodifiers --delay 0 "$TEXT"
                fi
            fi
        done
    fi
done
