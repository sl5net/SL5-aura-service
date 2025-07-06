#!/bin/bash
# /scripts/type_watcher.sh (CPU-freundliche Version)

DIR_TO_WATCH="/tmp"
LOCKFILE="/tmp/type_watcher.lock"

if [ -e "$LOCKFILE" ]; then exit 0; fi
echo $$ > "$LOCKFILE"
trap "rm -f $LOCKFILE" EXIT

# Unendliche Schleife
while true; do
    # Warte, bis die ERSTE passende Datei auftaucht, und beende dich dann.
    # Das verbraucht fast keine CPU.
    inotifywait -q -e create "$DIR_TO_WATCH" --format '%f' | grep -q "tts_output_"

    # Wenn wir hier sind, ist mindestens eine Datei da.
    # PAUSIERE KURZ, um alle parallelen Events zu sammeln.
    sleep 0.2

    # Sammle ALLE passenden Dateien, sortiert nach Alter, und arbeite sie ab.
    for f in $(ls -tr "$DIR_TO_WATCH"/tts_output_*.txt 2>/dev/null); do
        if [ -f "$f" ]; then
            TEXT=$(cat "$f")
            rm "$f"
            xdotool type --clearmodifiers "$TEXT"
            sleep 0.05 # Kurze Pause nach jedem Tippen
        fi
    done

    # Die Schleife beginnt von vorne und `inotifywait` wartet wieder passiv.
done
