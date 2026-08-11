#!/usr/bin/env bash
# scripts/search_rules/func/common/toggle_one_g_state_file.sh
# Toggle the alt-g state file between 0 and 1 (mirror of toggle_one_per_file.sh).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
ALT_G_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_alt_g_active"

current=$(cat "$ALT_G_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$ALT_G_STATE_FILE"
else
    echo "1" > "$ALT_G_STATE_FILE"
fi
