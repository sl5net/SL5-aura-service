#!/bin/bash
# scripts/search_rules/toggle_language_filter.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

LANGUAGE_FILTER_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_language_filter"
current=$(cat "$LANGUAGE_FILTER_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$LANGUAGE_FILTER_STATE_FILE"
else
    echo "1" > "$LANGUAGE_FILTER_STATE_FILE"
fi
