#!/usr/bin/env bash
# Helper script to read the one-per-file search rule state.

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
ONE_PER_FILE_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_one_per_file"

[ -f "$ONE_PER_FILE_STATE_FILE" ] || echo "0" > "$ONE_PER_FILE_STATE_FILE"

get_one_per_file_flag() {
    cat "$ONE_PER_FILE_STATE_FILE" 2>/dev/null || echo "0"
}

get_one_per_file_flag "$@"
