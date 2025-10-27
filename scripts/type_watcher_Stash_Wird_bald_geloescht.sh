#!/bin/bash
# type_watcher_keep_alive.sh (Version 4 - Final)

# --- Set FULL Environment explicitly for background tools ---
export DISPLAY=:0
export XAUTHORITY=${HOME}/.Xauthority
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

# ... (der Rest des Skripts bleibt exakt gleich) ...

# --- Dependency Check ---
if ! command -v inotifywait &> /dev/null || ! command -v xdotool &> /dev/null; then
    exit 1
fi

DIR_TO_WATCH="/tmp"
# DIR_TO_WATCH="${HOME}/.sl5_stt_tmp"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT="$SCRIPT_DIR/.."

FILE_PATTERN_BASE="tts_output_"
# LOCKFILE="/tmp/type_watcher.lock"
LOCKFILE="${DIR_TO_WATCH}/type_watcher.lock" # Lockfile also moves

LOG_FILE="$PROJECT_ROOT/type_watcher.log"

if [ -e "$LOCKFILE" ] && ps -p "$(cat "$LOCKFILE")" > /dev/null; then
    exit 0
fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

inotifywait -m -q -e create --format '%f' "$DIR_TO_WATCH" | while read -r FILE; do
    if [[ "$FILE" == ${FILE_PATTERN_BASE}* ]]; then
        FULL_PATH="${DIR_TO_WATCH}/${FILE}"
        sleep 0.05
        if [ -s "$FULL_PATH" ]; then
            TEXT=$(cat "$FULL_PATH")
            rm "$FULL_PATH"
            [ -n "$TEXT" ] && xdotool type --clearmodifiers "$TEXT"
        fi
    fi
done

