#!/bin/bash
# scripts/search_rules/toggle_one_per_file.sh

ONE_PER_FILE_STATE_FILE="$HOME/.search_rules_one_per_file"
current=$(cat "$ONE_PER_FILE_STATE_FILE" 2>/dev/null)
if [ "$current" = "1" ]; then
    echo "0" > "$ONE_PER_FILE_STATE_FILE"
else
    echo "1" > "$ONE_PER_FILE_STATE_FILE"
fi
