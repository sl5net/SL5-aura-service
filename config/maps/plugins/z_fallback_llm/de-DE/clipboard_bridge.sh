#!/bin/bash
# ~/clipboard_bridge.sh

# Datei im RAM (/tmp ist tmpfs)
FILE="/tmp/aura_clipboard.txt"

echo "Starte Clipboard-Bridge... (Drücke Strg+C zum Beenden)"

while true; do
    # Versuche xclip (X11)
    if command -v xclip &> /dev/null; then
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    # Fallback Wayland
    elif command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    fi

    # Kurz schlafen - kaum CPU Last
    sleep 1.5
done
