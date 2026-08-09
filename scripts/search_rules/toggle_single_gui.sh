#!/bin/bash
# scripts/search_rules/toggle_single_gui.sh

SINGLE_GUI_STATE_FILE="$HOME/.search_rules_single_gui"
current=$(cat "$SINGLE_GUI_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$SINGLE_GUI_STATE_FILE"
else
    echo "1" > "$SINGLE_GUI_STATE_FILE"
fi
