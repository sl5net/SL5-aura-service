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
#

# MAPS_DIR="$PROJECT_ROOT/config/maps"



# 1. PFADE & VARIABLEN
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"


LOG_DIR="$PROJECT_ROOT/log"
LOGFILE="$LOG_DIR/search_rules.sh.log"

function logger_info() {
    # echo "INFO: $1" >&2
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}


cd "$PROJECT_ROOT" || exit 1

DEFAULT_QUERY=".py pre # EXAMPLE:"
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"

MAPS_DIR="${1:-${MAPS_DIR:-config/maps}}"

echo "Line 54:" $MAPS_DIR

if [[ $MAPS_DIR == /* || $MAPS_DIR == ./* || $MAPS_DIR == ~/* || $MAPS_DIR == "$HOME"/* || $MAPS_DIR == ~*  ]]; then
  : # ok
else
  MAPS_DIR="./$MAPS_DIR"
fi

echo "Line 64:" $MAPS_DIR

HISTORY_FILE="$HOME/.search_rules_history"

# 2. EDITOR FALLBACK LOGIC (Korrigierte Bash-Version deines Backups)
get_preferred_editor() {
    # Suche nach Linux- oder Windows-Executables (kompatibel mit Git Bash/WSL)
    if command -v kate >/dev/null 2>&1; then echo "kate"; return; fi
    if command -v code >/dev/null 2>&1; then echo "code"; return; fi
    if command -v nano >/dev/null 2>&1; then echo "nano"; return; fi
    if command -v notepad.exe >/dev/null 2>&1; then echo "notepad.exe"; return; fi
    echo "vi" # Absoluter Linux-Standard-Fallback
}
PREFERRED_EDITOR=$(get_preferred_editor)

logger_info "Initializing search_rules.sh..."


# MAPS_DIR_DISPLAY=MAPS_DIR
MAPS_DIR="${MAPS_DIR/#\~/$HOME}"

#

if [[ ! -d "$MAPS_DIR" ]]; then
    echo "MAPS_DIR '$MAPS_DIR' dont exist" >&2
    sleep 5
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
#

LANG_TAG="${2:-}" # Optionaler zweiter Parameter (z.B. "de")

SELECTED_LINE=$(grep --color=never -rnH -I --include="${SEARCH_FILES_FILTER:-*}" . "$MAPS_DIR" | \
    fzf --history="$HISTORY_FILE" \
        --query="$INITIAL_QUERY" \
        --header="Enter: Edit | Ctrl+G: GitHub | Ctrl+A: Kopiere Vorschau | Ctrl+X: Kopiere Zeile" \
        --delimiter=":" \
        --bind="ctrl-z:previous-history" \
        --bind="ctrl-y:next-history" \
        --bind="ctrl-backspace:backward-kill-word" \
        --bind="ctrl-g:execute-silent(f={1}; rel=\${f#\$PROJECT_ROOT/}; systemd-run --user --collect --quiet xdg-open \"\$REPO_URL/\$rel#L{2}\")" \
        --bind='ctrl-x:execute-silent(echo {3..} | xclip -selection clipboard)' \
        --bind='ctrl-a:execute-silent(awk -v t={2} "BEGIN {t=t+0} NR>t-5 && NR<t+5 {print \$0}" {1} | xclip -selection clipboard)' \
        --preview-window="up:50%" \
        --preview='awk -v t={2} "BEGIN {t=t+0} NR>t-5 && NR<t+5 {printf \"%s%4d: %s\n\", (NR==t ? \">\" : \" \"), NR, \$0}" {1}' \
)
# xdg-open

# 5. EXECUTION (Robustes Öffnen) #
if [ -n "$SELECTED_LINE" ]; then
    FILE_PATH="$(echo "$SELECTED_LINE" | cut -d: -f1)"
    LINE_NUM=$(echo "$SELECTED_LINE" | cut -d: -f2)

    # Prüfen, ob es ein PDF ist (Groß-/Kleinschreibung ignorieren)
    if [[ "${FILE_PATH,,}" == *.pdf ]]; then
        xdg-open "$FILE_PATH" > /dev/null 2>&1 &
    else
        # Normale Editor-Logik
        case $PREFERRED_EDITOR in
            kate) nohup kate "$FILE_PATH" --line "$LINE_NUM" > /dev/null 2>&1 & ;;
            code) code --goto "$FILE_PATH:$LINE_NUM" ;;
            *) $PREFERRED_EDITOR "$FILE_PATH" & disown ;;
        esac
    fi
    exit 0
fi


