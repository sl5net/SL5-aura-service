#!/usr/bin/env bash
# Helper script to determine whether to pass --no-ignore flag based on gitignore state file.

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
GITIGNORE_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_respect_gitignore"

[ -f "$GITIGNORE_STATE_FILE" ] || echo "0" > "$GITIGNORE_STATE_FILE"

get_ignore_flag() {
    local respect
    respect=$(cat "$GITIGNORE_STATE_FILE" 2>/dev/null)
    if [ "$respect" = "1" ]; then
        echo ""
    else
        echo "--no-ignore"
    fi
}

get_ignore_flag "$@"
