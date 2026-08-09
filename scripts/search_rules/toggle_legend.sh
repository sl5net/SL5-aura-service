#!/bin/bash
# scripts/search_rules/toggle_legend.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_legend_state"
current=$(cat "$STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$STATE_FILE"
else
    echo "1" > "$STATE_FILE"
fi
