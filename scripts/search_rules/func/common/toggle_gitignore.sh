#!/bin/bash
# scripts/search_rules/toggle_gitignore.sh
GITIGNORE_STATE_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_respect_gitignore"
current=$(cat "$GITIGNORE_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$GITIGNORE_STATE_FILE"
else
    echo "1" > "$GITIGNORE_STATE_FILE"
fi
