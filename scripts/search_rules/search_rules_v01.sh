#!/bin/bash
# search_rules.sh
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
PREFERRED_EDITOR="kate"
HISTORY_FILE="$HOME/.search_rules_history"
DEFAULT_QUERY=".py pre"

# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------
function logger_info() {
    echo "INFO: $1" >&2
}

logger_info "Initializing search_rules.sh..."

# -----------------------------------------------------------------------------
# SETUP
# -----------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
MAPS_DIR="$PROJECT_ROOT/config/maps"

logger_info "Editor configured: $PREFERRED_EDITOR"
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
# PREVIEW COMMAND (AWK)
# -----------------------------------------------------------------------------
# Why AWK?
# 1. It handles arithmetic natively (no Bash $((...)) quoting hell).
# 2. It reads files safely.
# 3. It is standard on almost every Linux system.
#
# Logic:
# -v t={2}    : Pass the target line number from fzf to awk variable 't'.
# NR          : Current line number in awk.
# t+0         : Forces 't' to be treated as a number (strips potential quotes).
# output      : Prints line number and content, adds '>' for the matching line.

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
# SEARCH & SELECT
# -----------------------------------------------------------------------------
# grep --color=never: Important to keep the input clean for fzf.
SELECTED_LINE=$(grep --color=never -rnH -I . "$MAPS_DIR" | \
    fzf --delimiter : \
        --history "$HISTORY_FILE" \
        --query "$INITIAL_QUERY" \
        --preview "$PREVIEW_CMD" \
        --preview-window=up:50% \
)

# -----------------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------------
if [ -n "$SELECTED_LINE" ]; then
    FILE_PATH=$(echo "$SELECTED_LINE" | cut -d: -f1)
    LINE_NUM=$(echo "$SELECTED_LINE" | cut -d: -f2)

    logger_info "Opening: $FILE_PATH at line $LINE_NUM"
    "$PREFERRED_EDITOR" "$FILE_PATH:$LINE_NUM" &
else
    logger_info "No selection made."
fi
