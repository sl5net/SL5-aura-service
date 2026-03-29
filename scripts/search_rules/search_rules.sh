#!/bin/bash
# scripts/search_rules/search_rules.sh
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
#
# Make MAPS_DIR configurable via positional arg or environment variable
#
# Use parameter expansion so the script keeps its hard-coded default but
# allows overrides:
#
# - Priority: 1) first positional parameter ($1), 2) existing MAPS_DIR env var,
#   3) hard-coded default "$PROJECT_ROOT/config/maps".
# - Improves flexibility for CI, local overrides and testing without editing the script.
# - Adds quoting and a directory existence check to fail early if the path is invalid.

# Example usage:
# - ./search_rules.sh                 # uses default
# - ./search_rules.sh ./docs    # uses provided path
# - MAPS_DIR=/env/maps ./search_rules.sh

# There is also a version for Windows PC (in this folder) that can do a little less : search_rules.ps1


# This preserves backward compatibility while making configuration explicit.
# (s, 28.3.'26 23:07 Sat)

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
PREFERRED_EDITOR="kate"
HISTORY_FILE="$HOME/.search_rules_history"
DEFAULT_QUERY=".py pre # EXAMPLE:"
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"
# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------
function logger_info() {
    echo "" >&2
    # echo "INFO: $1" >&2 # for debuggin useful
}
logger_info "Initializing search_rules.sh..."
# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

MAPS_DIR="${1:-${MAPS_DIR:-$PROJECT_ROOT/config/maps}}"
# MAPS_DIR="$PROJECT_ROOT/config/maps"



if [[ ! -d "$MAPS_DIR" ]]; then
    echo "MAPS_DIR '$MAPS_DIR' dont exist" >&2
    exit 1
fi


export PROJECT_ROOT
export REPO_URL
logger_info "Editor configured: $PREFERRED_EDITOR"
logger_info "Project root: $PROJECT_ROOT"
logger_info "Target maps directory: $MAPS_DIR"
if ! command -v fzf &> /dev/null; then
    logger_info "Error: fzf is not installed."
    exit 1
fi
if [ ! -d "$MAPS_DIR" ]; then
    logger_info "Error: Maps directory not found at $MAPS_DIR"
    exit 1
fi
# -----------------------------------------------------------------------------
# PREVIEW COMMAND (AWK - Text Only)
# -----------------------------------------------------------------------------
PREVIEW_CMD='awk -v t={2} "BEGIN {t=t+0} NR>t-5 && NR<t+5 {printf \"%s%4d: %s\n\", (NR==t ? \">\" : \" \"), NR, \$0}" {1}'
# -----------------------------------------------------------------------------
# HISTORY LOGIC
# -----------------------------------------------------------------------------
INITIAL_QUERY="$DEFAULT_QUERY"
if [ -f "$HISTORY_FILE" ] && [ -s "$HISTORY_FILE" ]; then
    LAST_HISTORY_ENTRY=$(tail -n 1 "$HISTORY_FILE")
    if [ -n "$LAST_HISTORY_ENTRY" ]; then
        INITIAL_QUERY="$LAST_HISTORY_ENTRY"
    fi
fi
logger_info "Starting interactive search..."
# -----------------------------------------------------------------------------
# GITHUB OPEN (exported function for execute-silent)
# -----------------------------------------------------------------------------
open_github() {
    local file_path="$1"
    local line_num="$2"
    local rel="${file_path#$PROJECT_ROOT/}"
    local url="$REPO_URL/$rel#L$line_num"
    logger_info "Opening GitHub: $url"
    xdg-open "$url"
}
export -f open_github
# -----------------------------------------------------------------------------
# SEARCH & SELECT
# -----------------------------------------------------------------------------
SELECTED_LINE=$(grep --color=never -rnH -I . "$MAPS_DIR" | \
    fzf --delimiter : \
        --history "$HISTORY_FILE" \
        --query "$INITIAL_QUERY" \
        --header $'Ctrl+G: GitHub | Ctrl+X: Zeile kopieren | Ctrl+O: Pfad kopieren | Ctrl+Z/Y: History | Enter: Editor' \
        --bind 'ctrl-c:cancel' \
        --bind 'ctrl-z:previous-history' \
        --bind 'ctrl-y:next-history' \
        --bind 'ctrl-p:previous-history' \
        --bind 'ctrl-n:next-history' \
        --bind 'ctrl-a:select-all' \
        --bind 'ctrl-left:backward-word' \
        --bind 'ctrl-right:forward-word' \
        --bind 'ctrl-backspace:unix-word-rubout' \
        --bind 'ctrl-delete:kill-word' \
        --bind "ctrl-g:execute-silent(bash -c 'open_github {1} {2}')" \
        --bind 'ctrl-x:execute-silent(echo {3..} | xclip -selection clipboard)' \
        --bind 'ctrl-o:execute-silent(echo {1} | xclip -selection clipboard)' \
        --preview "$PREVIEW_CMD" \
        --preview-window="up:50%" \
)
# -----------------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------------
if [ -n "$SELECTED_LINE" ]; then
    FILE_PATH=$(echo "$SELECTED_LINE" | cut -d: -f1)
    LINE_NUM=$(echo "$SELECTED_LINE" | cut -d: -f2)
    logger_info "Opening: $FILE_PATH at line $LINE_NUM"
    "$PREFERRED_EDITOR" "$FILE_PATH:$LINE_NUM" &
    exit 0
else
    logger_info "No selection made."
fi
