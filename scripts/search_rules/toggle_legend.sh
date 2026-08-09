#!/bin/bash
# scripts/search_rules/toggle_legend.sh
STATE_FILE="$HOME/.search_rules_legend_state"
current=$(cat "$STATE_FILE" 2>/dev/null || echo "on")
if [ "$current" = "on" ]; then
    echo "off" > "$STATE_FILE"
else
    echo "on" > "$STATE_FILE"
fi
