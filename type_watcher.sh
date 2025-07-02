#!/bin/bash
# type_watcher.sh
FILE_TO_WATCH="/tmp/tts_output.txt"
DIR_TO_WATCH=$(dirname "$FILE_TO_WATCH")
BASEFILE=$(basename "$FILE_TO_WATCH")

#!/bin/bash
LOCKFILE="/tmp/type_watcher.lock"

if [ -e "$LOCKFILE" ]; then
    OLD_PID=$(cat "$LOCKFILE")
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "Another instance of type_watcher.sh is already running (PID $OLD_PID). Exiting."

        # echo "Waiting for $FILE_TO_WATCH ..."
        # notify-send "Waiting for $FILE_TO_WATCH ..."

        exit 0
    else
        echo $$ > "$LOCKFILE"
    fi
else
    echo $$ > "$LOCKFILE"
fi

echo "Watcher started. Waiting for $FILE_TO_WATCH to be written..."
notify-send "Watcher started. Waiting for $FILE_TO_WATCH to be written..."

while true; do
    # Warte auf close_write oder create im Verzeichnis
    EVENT=$(inotifywait -q -e close_write,create --format '%e %f' "$DIR_TO_WATCH")
    EVENT_TYPE=$(echo "$EVENT" | awk '{print $1}')
    EVENT_FILE=$(echo "$EVENT" | awk '{print $2}')

    # Prüfe, ob das Ereignis unsere Datei betrifft
    if [ "$EVENT_FILE" = "$BASEFILE" ]; then
        # Gib dem Dateisystem einen kurzen Moment
        sleep 0.1
        if [ -f "$FILE_TO_WATCH" ]; then
            TEXT_TO_TYPE=$(cat "$FILE_TO_WATCH")
            rm -f "$FILE_TO_WATCH" # Direkt löschen
            if [ -n "$TEXT_TO_TYPE" ]; then
                # echo "File detected. Typing: $TEXT_TO_TYPE"
                xdotool type --clearmodifiers "$TEXT_TO_TYPE"
                sleep 2 # Optional: Warte, bevor du das nächste Event annimmst
            fi
        fi
    fi
done

# On exit, remove the lock
trap "rm -f $LOCKFILE" EXIT


