#!/bin/bash
# scripts/search_rules/search_rules.sh

# TODO 25.6.'26 17:33 Thu: use
# scripts/search_rules/search_helpers.sh

# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
#
# Make MAPS_DIR configurable via positional arg or environment variable
#
# Use parameter expansion so the script keeps its hard-coded default but
# allows overrides:
#
# - Priority: 1) first positional parameter ($1), 2) existing MAPS_DIR env var,
#   3) hard-coded default "$SL5NET_AURA_PROJECT_ROOT/config/maps".
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

# MAPS_DIR="$SL5NET_AURA_PROJECT_ROOT/config/maps"



# 1. PFADE & VARIABLEN
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SL5NET_AURA_PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"


LOG_DIR="$SL5NET_AURA_PROJECT_ROOT/log"
LOGFILE="$LOG_DIR/search_rules.sh.log"

function logger_info() {
    # echo "INFO: $1" >&2
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}


cd "$SL5NET_AURA_PROJECT_ROOT" || exit 1

# SEARCH_CLOSE_ON_OPEN = False=$("$PYTHON_BIN" - <<'PY' 2>/dev/null || echo "True"


SEARCH_CLOSE_ON_OPEN=$("$PYTHON_BIN" - <<'PY' 2>/dev/null || echo "True"
import sys, importlib
try:
    cfg = importlib.import_module("config.settings_local")
    val = getattr(cfg, "SEARCH_CLOSE_ON_OPEN = False", True)
except ImportError:
    val = True
print("True" if bool(val) else "False")
PY
)



DEFAULT_QUERY=".py pre # EXAMPLE:"
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"

MAPS_DIR="${1:-${MAPS_DIR:-config/maps}}"

echo "Line 54:" $MAPS_DIR " pwd: " $PWD

if [[ $MAPS_DIR == /* || $MAPS_DIR == ./* || $MAPS_DIR == ~/* || $MAPS_DIR == "$HOME"/* || $MAPS_DIR == ~*  ]]; then
  : # okOhh sowas guckenvoran SchwarzkopfAura schwarz
else
  # MAPS_DIR="$SL5NET_AURA_PROJECT_ROOT/$MAPS_DIR"
  MAPS_DIR="./$MAPS_DIR"
  cd "$SL5NET_AURA_PROJECT_ROOT" || exit 1
  echo "Line 63:" $MAPS_DIR " pwd: " $PWD
fi
#Aurora als Sourcecode
#  $PROJECT_ROOTOrange schwarz QuoteGraz Wort
# ./scripts/py/func  pwd:  /home/bob/projects/py/STT
#Line 137: MAPS_DIR:  ./scripts/py/func  pwd:  /home/bob/projects/py/STT
#/home/bob/projects/py/STT/scripts/search_rules/search_rules.sh: Zeile 142: MAPS_DIR:: Kommando nicht gefundenOrange Rost

#


#




echo "Line 64:" $MAPS_DIR " pwd: " $PWD

HISTORY_FILE="$SL5NET_AURA_PROJECT_ROOT/data/_search_rules_state/.search_rules_history"

# 2. EDITOR FALLBACK LOGIC (Korrigierte Bash-Version deines Backups)
get_preferred_editor() {
    if command -v kate >/dev/null 2>&1; then echo "kate"; return; fi
    if command -v code >/dev/null 2>&1; then echo "code"; return; fi
    if command -v nano >/dev/null 2>&1; then echo "nano"; return; fi
    if command -v notepad.exe >/dev/null 2>&1; then echo "notepad.exe"; return; fi
    echo "vi" # Absoluter Linux-Standard-Fallback
}
PREFERRED_EDITOR=$(get_preferred_editor)

logger_info "Initializing search_rules.sh…"


# MAPS_DIR_DISPLAY=MAPS_DIR
MAPS_DIR="${MAPS_DIR/#\~/$HOME}"

#

if [[ ! -d "$MAPS_DIR" ]]; then
    echo "MAPS_DIR '$MAPS_DIR' dont exist" >&2
    sleep 5
    exit 1
fi

export SL5NET_AURA_PROJECT_ROOT
export REPO_URL
logger_info "Editor configured: $PREFERRED_EDITOR"
logger_info "Project root: $SL5NET_AURA_PROJECT_ROOT"
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
logger_info "Starting interactive search…"
# -----------------------------------------------------------------------------
# GITHUB OPEN (exported function for execute-silent)
# -----------------------------------------------------------------------------
open_github() {
    local file_path="$1"
    local line_num="$2"
    local rel="${file_path#$SL5NET_AURA_PROJECT_ROOT/}"
    local url="$REPO_URL/$rel#L$line_num"
    logger_info "Opening GitHub: $url"
    xdg-open "$url"
}
export -f open_github

echo "Line 137: MAPS_DIR: " $MAPS_DIR " pwd: " $PWD







LANG_TAG="${2:-}" # Optionaler zweiter Parameter (z.B. "de")

while true; do
SELECTED_LINE=$(grep --color=never -rnH -I $(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --include=/g; s/^/--include=/') . "$MAPS_DIR" | \
    fzf --history="$HISTORY_FILE" \
        --query="$INITIAL_QUERY" \
        --header="Caller:??? | Enter: Edit | Ctrl+G: GitHub | Ctrl+A: Kopiere Vorschau | Ctrl+X: Kopiere Zeile" \
        --delimiter=":" \
        --bind="ctrl-z:previous-history" \
        --bind="ctrl-y:next-history" \
        --bind="ctrl-backspace:backward-kill-word" \
        --bind="ctrl-delete:kill-word" \
        --bind="ctrl-left:backward-word" \
        --bind="ctrl-right:forward-word" \
        --bind="home:beginning-of-line" \
        --bind="end:end-of-line" \
        --bind="ctrl-g:execute-silent(f={1}; rel=\${f#\$SL5NET_AURA_PROJECT_ROOT/}; systemd-run --user --collect --quiet xdg-open \"\$REPO_URL/\$rel#L{2}\")" \
        --bind='ctrl-x:execute-silent(echo {3..} | xclip -selection clipboard)' \
        --bind='ctrl-a:execute-silent(awk -v t={2} "BEGIN {t=t+0} NR>t-5 && NR<t+5 {print \$0}" {1} | xclip -selection clipboard)' \
        --preview-window="up:50%" \
        --preview='awk -v t={2} "BEGIN {t=t+0} NR>t-5 && NR<t+5 {printf \"%s%4d: %s\n\", (NR==t ? \">\" : \" \"), NR, \$0}" {1}' \
)
# xdg-openzoran suche ducken

# 5. EXECUTION (Robustes Öffnen) #
if [ -n "$SELECTED_LINE" ]; then
    FILE_PATH="$(echo "$SELECTED_LINE" | cut -d: -f1)"
    RAW_LINE_NUM="$(echo "$SELECTED_LINE" | cut -d: -f2)"
    if [[ "$RAW_LINE_NUM" =~ ^[0-9]+$ ]]; then
        LINE_NUM="$RAW_LINE_NUM"
    else
        LINE_NUM=""
    fi

    if [[ "$FILE_PATH" != /* && -f "$SL5NET_AURA_PROJECT_ROOT/$FILE_PATH" ]]; then
        FILE_PATH="$SL5NET_AURA_PROJECT_ROOT/$FILE_PATH"
    fi

    EXT="${FILE_PATH##*.}"
    EXT="${EXT,,}"
    BIN_EXTS="pdf png jpg jpeg gif webp mp4 mp3 zip tar gz 7z"
    # Text-Format ?
    MIME_TYPE=$(file --mime-type -b "$FILE_PATH" 2>/dev/null || echo "text/plain")
    echo "160: MIME_TYPE=$MIME_TYPE "
    if [[ " $BIN_EXTS " =~ " $EXT " ]] || [[ "$MIME_TYPE" != text/* && "$MIME_TYPE" != "application/x-empty" && "$MIME_TYPE" != "cannot open"* ]]; then
        # Binary format (PDF, images, etc.) -> system default
        echo "xdg-open $FILE_PATH > /dev/null 2>&1 &"
        xdg-open "$FILE_PATH" > /dev/null 2>&1 &
        sleep 8

    else
        # Standard editor dispatching logic
        case $PREFERRED_EDITOR in
            cudatext)
                if [ -n "$LINE_NUM" ]; then
                    nohup "$PREFERRED_EDITOR" "$FILE_PATH@$LINE_NUM" > /dev/null 2>&1 &
                else
                    nohup "$PREFERRED_EDITOR" "$FILE_PATH" > /dev/null 2>&1 &
                fi
                ;;
            xed|gedit)
                if [ -n "$LINE_NUM" ]; then
                    nohup "$PREFERRED_EDITOR" "$FILE_PATH" "+$LINE_NUM" > /dev/null 2>&1 &
                else
                    nohup "$PREFERRED_EDITOR" "$FILE_PATH" > /dev/null 2>&1 &
                fi
                ;;
            code)
                if [ -n "$LINE_NUM" ]; then
                    nohup code -g "$FILE_PATH:$LINE_NUM" > /dev/null 2>&1 &
                else
                    nohup code "$FILE_PATH" > /dev/null 2>&1 &
                fi
                ;;
            kate)
                if [ -n "$LINE_NUM" ]; then
                    nohup kate "$FILE_PATH" --line "$LINE_NUM" > /dev/null 2>&1 &
                else
                    nohup kate "$FILE_PATH" > /dev/null 2>&1 &
                fi
                ;;
            *)
                nohup "$PREFERRED_EDITOR" "$FILE_PATH" > /dev/null 2>&1 &
                ;;
        esac        
    fi
    # exit 0

    # PDF ?
    # if [[ "${FILE_PATH,,}" == *.pdf ]]; then

    if [ "$SEARCH_CLOSE_ON_OPEN" = "True" ]; then
        exit 0
    fi

else
    exit 0
fi

done
