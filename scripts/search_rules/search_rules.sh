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



# SEARCH_CLOSE_ON_OPEN=False=$("$PYTHON_BIN" - <<'PY' 2>/dev/null || echo "True"

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
  # MAPS_DIR="$PROJECT_ROOT/$MAPS_DIR"
  MAPS_DIR="./$MAPS_DIR"
  cd "$PROJECT_ROOT" || exit 1
  echo "Line 63:" $MAPS_DIR " pwd: " $PWD
fi
#Aurora als Sourcecode
#  $PROJECT_ROOTOrange schwarz QuoteGraz Wort
# ./scripts/py/func  pwd:  /home/seeh/projects/py/STT
#Line 137: MAPS_DIR:  ./scripts/py/func  pwd:  /home/seeh/projects/py/STT
#/home/seeh/projects/py/STT/scripts/search_rules/search_rules.sh: Zeile 142: MAPS_DIR:: Kommando nicht gefundenOrange Rost

#


#




echo "Line 64:" $MAPS_DIR " pwd: " $PWD

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

export LANG="C.UTF-8"
export LC_ALL="C.UTF-8"
export PYTHONUTF8=1

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

echo "Line 137: MAPS_DIR: " $MAPS_DIR " pwd: " $PWD

# Line 54: scripts/py/func  pwd:  /home/seeh/projects/py/STT
# Line 137: MAPS_DIR:  ./scripts/py/func  pwd:  /home/seeh/projects/py/STT

# MAPS_DIR:  "scripts/py/func"

#Hurra zurückwerfenJura Quelltext







LANG_TAG="${2:-}"

while true; do
# Wir starten fzf mit --expect, damit wir verschiedene Tasten abfangen können
FZF_OUTPUT=$(grep --color=never -rnH -I $(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --include=/g; s/^/--include=/') . "$MAPS_DIR" | \
    fzf --print-query \
        --history="$HISTORY_FILE" \
        --query="$INITIAL_QUERY" \
        --header="Enter: Run Selected | Ctrl+R: Run Raw Typed | Ctrl+E: Open in Editor | Ctrl+G: GitHub | Ctrl+A: Kopiere Vorschau | Ctrl+X: Kopiere Zeile" \
        --delimiter=":" \
        --expect="ctrl-e,ctrl-r" \
        --bind="ctrl-z:previous-history" \
        --bind="ctrl-y:next-history" \
        --bind="ctrl-backspace:backward-kill-word" \
        --bind="ctrl-delete:kill-word" \
        --bind="ctrl-left:backward-word" \
        --bind="ctrl-right:forward-word" \
        --bind="home:beginning-of-line" \
        --bind="end:end-of-line" \
        --bind="ctrl-g:execute-silent(f={1}; rel=\${f#\$PROJECT_ROOT/}; systemd-run --user --collect --quiet xdg-open \"\$REPO_URL/\$rel#L{2}\")" \
        --bind='ctrl-x:execute-silent(echo {3..} | xclip -selection clipboard)' \
        --bind='ctrl-a:execute-silent(python3 '"$SCRIPT_DIR"'/preview_rule.py {1} {2} | xclip -selection clipboard)' \
        --preview-window="up:50%" \
        --preview='python3 '"$SCRIPT_DIR"'/preview_rule.py {1} {2}' \
)

# Wenn fzf abgebrochen wurde (ESC)
if [ -z "$FZF_OUTPUT" ]; then
    exit 0
fi

# fzf gibt bei --expect zuerst die gedrückte Taste aus, danach das ausgewählte Element
QUERY_TYPED=$(echo "$FZF_OUTPUT" | sed -n '1p')
KEY=$(echo "$FZF_OUTPUT" | sed -n '2p')
SELECTED_LINE=$(echo "$FZF_OUTPUT" | sed -n '3p')

# DEBUG-Einträge für das Logfile:
logger_info "DEBUG: KEY='$KEY' QUERY_TYPED='$QUERY_TYPED'"
logger_info "DEBUG_RAW: '$FZF_OUTPUT'"

if [ "$KEY" = "ctrl-r" ] && [ -n "$QUERY_TYPED" ]; then
    logger_info "Executing raw typed query via native python: $QUERY_TYPED"
    setsid "$PROJECT_ROOT/.venv/bin/python3" "$SCRIPT_DIR/run_palette_command.py" "$QUERY_TYPED" >/dev/null 2>&1 &
    exit 0
elif [ -z "$KEY" ] && [ -n "$SELECTED_LINE" ]; then
    FILE_PATH="$(echo "$SELECTED_LINE" | cut -d: -f1)"
    LINE_NUM=$(echo "$SELECTED_LINE" | cut -d: -f2)
    QUERY=$(python3 "$SCRIPT_DIR/preview_rule.py" --extract "$FILE_PATH" "$LINE_NUM")

    if [ -n "$QUERY" ]; then
        logger_info "Executing selected rule via native python: $QUERY"
        setsid "$PROJECT_ROOT/.venv/bin/python3" "$SCRIPT_DIR/run_palette_command.py" "$QUERY" >/dev/null 2>&1 &
        exit 0
    fi
fi

if [ -z "$SELECTED_LINE" ]; then
    exit 0
fi

FILE_PATH="$(echo "$SELECTED_LINE" | cut -d: -f1)"
LINE_NUM=$(echo "$SELECTED_LINE" | cut -d: -f2)


# --- AKTION 1: ENTER GEdrückt -> REGEL AUSFÜHREN ---
if [ -z "$KEY" ]; then
    # Extrahiere den Trigger-Begriff mit unserem Python-Skript
    QUERY=$(python3 "$SCRIPT_DIR/preview_rule.py" --extract "$FILE_PATH" "$LINE_NUM")

    if [ -n "$QUERY" ]; then
        logger_info "Executing rule via detached setsid into tts_output: s \"$QUERY\""

        # Variablen exportieren, damit sie in der neuen setsid-Shell verfügbar sind
        export QUERY
        export LOGFILE

        # setsid startet eine komplett neue Session im Hintergrund, wodurch konsole sofort schließt!

        systemd-run --user --collect --quiet \
            -E LOGFILE="$LOGFILE" -E QUERY="$QUERY" \
            bash -c '
            export PYTHONUTF8=1 LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8
            logger_info() { echo "$(date "+%Y-%m-%d %H:%M:%S") - $1" >> "$LOGFILE"; }
            OUTPUT=$(zsh -i -c "s \"$QUERY\"" 2>&1)
            logger_info "RAW: $OUTPUT"
            CLEAN_OUTPUT=$(echo "$OUTPUT" | tail -n 1)
            echo "$CLEAN_OUTPUT" > "/tmp/sl5_aura/tts_output/tts_output_fzf_$$.txt"
        '

        # Terminal-Popup sofort beenden
        exit 0
    else
        logger_info "No '# EXAMPLE:' found to execute. Falling back to editor."
        echo "No '# EXAMPLE:' found. Opening in editor instead..."
        KEY="ctrl-e"
        sleep 1
    fi
fi

# --- AKTION 2: CTRL+E GEdrückt -> EDITOR ÖFFNEN (Ihr Original-Code) ---
if [ "$KEY" = "ctrl-e" ]; then
    EXT="${FILE_PATH##*.}"
    EXT="${EXT,,}"
    BIN_EXTS="pdf png jpg jpeg gif webp mp4 mp3 zip tar gz 7z"

    MIME_TYPE=$(file --mime-type -b "$FILE_PATH")
    echo "MIME_TYPE=$MIME_TYPE "

    logger_info "Editing file: $FILE_PATH at line $LINE_NUM"

    if [[ " $BIN_EXTS " =~ " $EXT " ]] || [[ "$MIME_TYPE" != text/* && "$MIME_TYPE" != "application/x-empty" ]]; then
        xdg-open "$FILE_PATH" > /dev/null 2>&1 &
        sleep 8
    else
        case $PREFERRED_EDITOR in
            kate) nohup kate "$FILE_PATH" --line "$LINE_NUM" > /dev/null 2>&1 & ;;
            code) code --goto "$FILE_PATH:$LINE_NUM" ;;
            *) $PREFERRED_EDITOR "$FILE_PATH" & disown ;;
        esac
    fi
fi

if [ "$SEARCH_CLOSE_ON_OPEN" = "True" ]; then
    exit 0
fi

done
