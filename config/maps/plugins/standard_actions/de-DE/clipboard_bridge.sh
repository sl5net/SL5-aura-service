#!/bin/bash
# ~/clipboard_bridge.sh

FILE_IN="/tmp/aura_clipboard.txt"
FILE_OUT="/tmp/aura_clipboard_out.txt"

echo "Starte Bidirektionale Clipboard-Bridge..."

while true; do
    # 1. RÜCKKANAL PRÜFEN (Python -> Clipboard)
    if [ -f "$FILE_OUT" ]; then
        echo "Änderung erkannt. Schreibe in Zwischenablage..."

        if command -v xclip &> /dev/null; then
            cat "$FILE_OUT" | xclip -selection clipboard -i
        elif command -v wl-copy &> /dev/null; then
            cat "$FILE_OUT" | wl-copy
        fi

        # Löschen, damit nicht endlos geschrieben wird
        rm "$FILE_OUT"

        # Kurze Pause, um Race Conditions mit dem Lesen zu vermeiden
        sleep 0.5

        # Aktualisiere auch direkt die Input-Datei, damit Konsistenz herrscht
        if command -v xclip &> /dev/null; then
            xclip -selection clipboard -o > "$FILE_IN" 2>/dev/null
        elif command -v wl-paste &> /dev/null; then
            wl-paste --no-newline > "$FILE_IN" 2>/dev/null
        fi

    else
        # 2. NORMALBETRIEB (Clipboard -> Python)
        if command -v xclip &> /dev/null; then
            xclip -selection clipboard -o > "$FILE_IN" 2>/dev/null
        elif command -v wl-paste &> /dev/null; then
            wl-paste --no-newline > "$FILE_IN" 2>/dev/null
        fi
    fi

    sleep 1.0
done
