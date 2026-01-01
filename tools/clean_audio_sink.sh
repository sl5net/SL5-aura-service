#!/bin/bash
echo "🧹 Suche nach Altlasten mit '_Sink'..."

# Findet die IDs aller Module, die "_Sink" enthalten
MODULE_IDS=$(pactl list short modules | grep "_Sink" | cut -f1)

if [ -z "$MODULE_IDS" ]; then
    echo "✅ Keine Geister-Sinks gefunden."
else
    for ID in $MODULE_IDS; do
        echo "🚫 Entlade Modul-ID: $ID"
        pactl unload-module $ID
    done
    echo "✨ System gereinigt."
fi


# Findet die IDs aller Module, die "_Sink" enthalten
MODULE_IDS=$(pactl list short modules | grep "_sink" | cut -f1)

if [ -z "$MODULE_IDS" ]; then
    echo "✅ Keine Geister-Sinks gefunden."
else
    for ID in $MODULE_IDS; do
        echo "🚫 Entlade Modul-ID: $ID"
        pactl unload-module $ID
    done
    echo "✨ System gereinigt."
fi

# Optional: Auch alle hängenden Loopbacks entfernen (falls gewünscht)
pactl unload-module module-loopback 2>/dev/null
