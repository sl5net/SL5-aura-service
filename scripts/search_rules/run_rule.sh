#!/bin/bash
# scripts/search_rules/run_rule.sh
source "$(dirname "${BASH_SOURCE[0]}")/search_helpers.sh"
cd "$PROJECT_ROOT" || exit 1

REAL="${REAL:-1}"
M_DIR="${1:-${MAPS_DIR:-config/maps}}"
M_DIR="${M_DIR/#\~/$HOME}"
[[ ! -d "$M_DIR" ]] && exit 1

# Capture window title BEFORE fzf starts
AURA_ACTIVE_WINDOW_TITLE=$(python3 -c "
import sys
sys.path.insert(0, '$PROJECT_ROOT')
from scripts.py.func.get_active_window_title import get_active_window_title_safe
print(get_active_window_title_safe())
" 2>/dev/null)
export AURA_ACTIVE_WINDOW_TITLE

H_FILE="$HOME/.search_rules_history"

cp "$H_FILE" "$H_FILE.bak"

# Deduplicate
tac "$H_FILE" | awk '!seen[$0]++' | tac > "$H_FILE.tmp" && mv "$H_FILE.tmp" "$H_FILE"

IQ=".py pre # EXAMPLE:"
[ -s "$H_FILE" ] && IQ=$(tail -n 1 "$H_FILE")

# Define the AWK script in a variable to prevent Bash command-substitution parenthesis parsing bugs
AWK_SCRIPT='{
    full_path = $1;
    line = $2;
    content = substr($0, index($0, ":" line ":") + length(line) + 2);
    gsub(/^[ \t]+/, "", content);
    short_path = full_path;

    while (match(short_path, /\/[a-z]{2}-[A-Z]{2}\//)) {
        lang_letter = substr(short_path, RSTART + 1, 1);
        short_path = substr(short_path, 1, RSTART) lang_letter "…/" substr(short_path, RSTART + RLENGTH);
    }
    if (length(short_path) > 40) {
        short_path = "…" substr(short_path, length(short_path) - 38);
    }

    gsub(/FUZZY_MAP_pre\.py/, "…", short_path);

    # Align the path and line to 45 characters, then append the rule content
    display = sprintf("%-45s | %s", short_path ":" line, content);
    # Print tab-separated fields for fzf
    print display "\t" full_path "\t" line;
#    print display " " full_path " " line;

}'

#

while true; do
FILT=$(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --include=/g; s/^/--include=/')

if [[ "$REAL" == "1" ]]; then
    MAP_FILES=$(python3 "$SCRIPT_DIR/filter_maps_by_reality.py" --lang-only "$M_DIR")
    if [[ -z "$MAP_FILES" ]]; then
        logger_info "REAL=1: No map files match current language"
        exit 1
    fi
#    SEARCH_INPUT=$(echo "$MAP_FILES" | tr '\n' '\0' | xargs -0 grep -irnH -I $FILT .)
#    SEARCH_INPUT=$(echo "$MAP_FILES" | rg --null -n --files | xargs -0 rg -n "$FILT")
    SEARCH_INPUT=$(echo "$MAP_FILES" | tr '\n' '\0' | xargs -0 rg -nH "^")
else
    SEARCH_INPUT=$(grep -irnH -I $FILT . "$M_DIR")
fi

F_OUT=$(echo "$SEARCH_INPUT" | awk -F: "$AWK_SCRIPT" | \
    fzf --print-query \
        --delimiter=$'\t' \
        --history="$H_FILE" --query="$IQ" \
        --header="Enter/Ctrl+R: Run | Ctrl+E: Edit" \
        --with-nth=1 \
        --bind="ctrl-z:previous-history" \
        --bind="ctrl-y:next-history" \
        --bind="ctrl-backspace:backward-kill-word" \
        --bind="ctrl-delete:kill-word" \
        --bind="ctrl-left:backward-word" \
        --bind="ctrl-right:forward-word" \
        --bind="home:beginning-of-line" \
        --bind="end:end-of-line" \
        --expect="ctrl-e,ctrl-r" \
        --preview='python3 '"$SCRIPT_DIR"'/preview_rule.py {2} {3}' \
)
[[ -z "$F_OUT" ]] && exit 0
QUERY_TYPED=$(echo "$F_OUT" | sed -n '1p')
#QUERY_TYPED=$(echo "$F_OUT" | sed -n '1p' | tr -d '\r')
KEY=$(echo "$F_OUT" | sed -n '2p')
#SEL=$(echo "$F_OUT" | sed -n '3p') # 15.7.'26 08:40 Wed
#SEL=$(echo "$F_OUT" | sed -n '3p' | tr -d '\r')

SEL=$(echo "$F_OUT" | sed -n '3p')
if [[ -n "$SEL" ]]; then
    F_PATH="$(echo "$SEL" | cut -f2)"
    L_NUM="$(echo "$SEL" | cut -f3)"
else
    F_PATH=""
    L_NUM=""
fi

logger_info "DBG typed='$QUERY_TYPED' key='$KEY' sel='$SEL'"

SEL=$(echo "$F_OUT" | sed -n '3p')
logger_info "41: DBG typed='$QUERY_TYPED' key='$KEY' sel='$SEL'"
if [[ -z "$KEY" || "$KEY" = "ctrl-r" ]]; then
    logger_info "43: KEY=$KEY"
    QUERY=""
    if [[ -z "$KEY" && -n "$SEL" ]]; then

#        F_PATH="$(echo "$SEL" | cut -d: -f1)"
#        L_NUM="$(echo "$SEL" | cut -d: -f2)"
#        logger_info "50: Enter pressed -> use"

        # F_PATH and L_NUM are already correctly extracted globally above
        logger_info "50: Enter pressed -> use"
        logger_info "$F_PATH:$L_NUM"

        # scripts/search_rules/run_rule.sh:49
        QUERY=$(python3 "$SCRIPT_DIR/preview_rule.py" --extract "$F_PATH" "$L_NUM")
        logger_info "python3 '$SCRIPT_DIR/preview_rule.py' --extract '$F_PATH' '$L_NUM'"
        logger_info "56: DBG extract='$QUERY'"

    fi
    if [[ -z "$QUERY" ]]; then
        logger_info "55: Ctrl+R pressed use typed query (QUERY_TYPED)"
        QUERY="$QUERY_TYPED"
    fi


    logger_info "65: final_query='$QUERY' py_exists=$(test -f "$PROJECT_ROOT/.venv/bin/python3" && echo yes || echo NO)"
    if [[ -n "$QUERY" ]]; then
        logger_info "67: Executing: $QUERY"

        run_palette_path="$PROJECT_ROOT/scripts/search_rules/run_palette_command.py"
        python3_path="$PROJECT_ROOT/.venv/bin/python3"

        logger_info " "
        logger_info " "
        logger_info " "
        logger_info "$python3_path $run_palette_path '$QUERY'"
        logger_info " "
        logger_info " "
        logger_info " "

        nohup "$python3_path" "$run_palette_path" "$QUERY" >> "$LOGFILE" 2>&1 &
        BG_PID=$!
        disown $BG_PID
        logger_info "72: DBG spawned pid=$BG_PID"
        exit 0
    fi
    logger_info "75: no query to execute"

    exit 0
fi




if [[ "$KEY" = "ctrl-e" && -n "$SEL" ]]; then
#    F_PATH="$(echo "$SEL" | cut -f3)"
#    L_NUM="$(echo "$SEL" | cut -f2)"
    # F_PATH and L_NUM are already correctly extracted globally above
    (nohup kate "$F_PATH" --line "$L_NUM" >/dev/null 2>&1 & disown || $PREFERRED_EDITOR "$F_PATH" & disown)
fi
done
