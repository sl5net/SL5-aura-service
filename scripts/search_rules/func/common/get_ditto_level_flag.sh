#!/usr/bin/env bash
# Helper script to read the ditto display level.
# 1 = ditto marks duplicates, 2 = collapsed to first entry per group.

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
DITTO_LEVEL_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_ditto_level"

[ -f "$DITTO_LEVEL_STATE_FILE" ] || echo "1" > "$DITTO_LEVEL_STATE_FILE"

get_ditto_level() {
    cat "$DITTO_LEVEL_STATE_FILE" 2>/dev/null || echo "1"
}

get_ditto_level "$@"
