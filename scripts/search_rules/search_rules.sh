#!/bin/bash
# scripts/search_rules/search_rules.sh
# (Part 1 of 2)
source "$(dirname "${BASH_SOURCE[0]}")/search_helpers.sh"
cd "$PROJECT_ROOT" || exit 1

M_DIR="${1:-${MAPS_DIR:-config/maps}}"
M_DIR="${M_DIR/#\~/$HOME}"
[[ ! -d "$M_DIR" ]] && exit 1
H_FILE="$HOME/.search_rules_history"
IQ=".py pre # EXAMPLE:"
[ -s "$H_FILE" ] && IQ=$(tail -n 1 "$H_FILE")

while true; do

F_OUT=$(grep -rnH -I $(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --include=/g; s/^/--include=/') . "$M_DIR" | \
    fzf --history="$H_FILE" --query="$IQ" \
        --header="Enter: Edit | Ctrl+G: GitHub" --delimiter=":" \
        --bind="ctrl-g:execute-silent(bash -c 'open_github {1} {2}')" \
        --preview-window="up:50%" --preview='python3 '"$SCRIPT_DIR"'/preview_rule.py {1} {2}' \
)

[[ -z "$F_OUT" ]] && exit 0
F_PATH="$(echo "$F_OUT" | cut -d: -f1)"
L_NUM=$(echo "$F_OUT" | cut -d: -f2)
logger_info "Editing: $F_PATH:$L_NUM"
[[ "$PREFERRED_EDITOR" = "kate" ]] && nohup kate "$F_PATH" --line "$L_NUM" >/dev/null 2>&1 & || $PREFERRED_EDITOR "$F_PATH" & disown
done

