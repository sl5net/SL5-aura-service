#!/bin/bash
# scripts/search_rules/proot_control.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
PROOT_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_proot"

ACTION="$1"
BASE_ROOT="$2"
NEW_PROOT="$3"

case "$ACTION" in
  up)
    current=$(cat "$PROOT_STATE_FILE" 2>/dev/null)
    [ -z "$current" ] && current="$BASE_ROOT"
    if [ "$current" != "$BASE_ROOT" ]; then
        parent=$(dirname "$current")
        if [ "${#parent}" -lt "${#BASE_ROOT}" ]; then
            parent="$BASE_ROOT"
        fi
        echo "$parent" > "$PROOT_STATE_FILE"
    fi
    ;;
  reset)
    echo "$BASE_ROOT" > "$PROOT_STATE_FILE"
    ;;
  set)
    [ -n "$NEW_PROOT" ] && [ -d "$NEW_PROOT" ] && echo "$NEW_PROOT" > "$PROOT_STATE_FILE"
    ;;
esac
