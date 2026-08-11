#!/bin/bash
# scripts/search_rules/toggle_one_per_file.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"

ONE_PER_FILE_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_one_per_file"
current=$(cat "$ONE_PER_FILE_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$ONE_PER_FILE_STATE_FILE"
else
    echo "1" > "$ONE_PER_FILE_STATE_FILE"
fi
