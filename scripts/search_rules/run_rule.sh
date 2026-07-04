#!/bin/bash
# scripts/search_rules/run_rule.sh
source "$(dirname "${BASH_SOURCE[0]}")/search_helpers.sh"
cd "$PROJECT_ROOT" || exit 1

M_DIR="${1:-${MAPS_DIR:-config/maps}}"
M_DIR="${M_DIR/#\~/$HOME}"
[[ ! -d "$M_DIR" ]] && exit 1
H_FILE="$HOME/.search_rules_history"
IQ=".py pre # EXAMPLE:"
[ -s "$H_FILE" ] && IQ=$(tail -n 1 "$H_FILE")

while true; do
FILT=$(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --include=/g; s/^/--include=/')
F_OUT=$(grep -rnH -I $FILT . "$M_DIR" | \
    fzf --print-query \
        --history="$H_FILE" --query="$IQ" \
        --header="Enter/Ctrl+R: Run | Ctrl+E: Edit" --delimiter=":" \
        --bind="ctrl-z:previous-history" \
        --bind="ctrl-y:next-history" \
        --bind="ctrl-backspace:backward-kill-word" \
        --bind="ctrl-delete:kill-word" \
        --bind="ctrl-left:backward-word" \
        --bind="ctrl-right:forward-word" \
        --bind="home:beginning-of-line" \
        --bind="end:end-of-line" \
        --expect="ctrl-e,ctrl-r" \
        --preview='python3 '"$SCRIPT_DIR"'/preview_rule.py {1} {2}' \
)
[[ -z "$F_OUT" ]] && exit 0
QUERY_TYPED=$(echo "$F_OUT" | sed -n '1p')
#QUERY_TYPED=$(echo "$F_OUT" | sed -n '1p' | tr -d '\r')
KEY=$(echo "$F_OUT" | sed -n '2p')
SEL=$(echo "$F_OUT" | sed -n '3p')
#SEL=$(echo "$F_OUT" | sed -n '3p' | tr -d '\r')
logger_info "DBG typed='$QUERY_TYPED' key='$KEY' sel='$SEL'"


# NEW 25.6.'26 16:10 Thu
SEL=$(echo "$F_OUT" | sed -n '3p')
logger_info "41: DBG typed='$QUERY_TYPED' key='$KEY' sel='$SEL'"
if [[ -z "$KEY" || "$KEY" = "ctrl-r" ]]; then
    logger_info "43: KEY=$KEY"
    QUERY=""
    if [[ -z "$KEY" && -n "$SEL" ]]; then

        F_PATH="$(echo "$SEL" | cut -d: -f1)"
        L_NUM="$(echo "$SEL" | cut -d: -f2)"

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
    F_PATH="$(echo "$SEL" | cut -d: -f1)"
    L_NUM="$(echo "$SEL" | cut -d: -f2)"
    (nohup kate "$F_PATH" --line "$L_NUM" >/dev/null 2>&1 & disown || $PREFERRED_EDITOR "$F_PATH" & disown)
fi
done
