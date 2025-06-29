#!/bin/bash

FILE_TO_WATCH="/tmp/tts_output.txt"
DIR_TO_WATCH=$(dirname "$FILE_TO_WATCH")
BASEFILE=$(basename "$FILE_TO_WATCH")

echo "Watcher started. Waiting for $FILE_TO_WATCH to be written..."

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
