#!/usr/bin/env bash
# Helper script to read the language folder filter state.
# Default ON: only the current language folder is shown.

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
LANGUAGE_FILTER_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_language_filter"

[ -f "$LANGUAGE_FILTER_STATE_FILE" ] || echo "1" > "$LANGUAGE_FILTER_STATE_FILE"

get_language_filter_flag() {
    cat "$LANGUAGE_FILTER_STATE_FILE" 2>/dev/null || echo "1"
}

get_language_filter_flag "$@"
