#!/bin/bash
# scripts/search_rules/run_rule.sh

####

source "$(dirname "${BASH_SOURCE[0]}")/search_helpers.sh"
cd "$PROJECT_ROOT" || exit 1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/sl5net/SL5-aura-service/blob/master"

export SCRIPT_DIR
export PROJECT_ROOT
export REPO_URL

FILT=$(echo "${SEARCH_FILES_FILTER:-*}" | sed 's/|/ --glob=/g; s/^/--glob=/')
export FILT

mkdir -p "$PROJECT_ROOT/data/_search_rules_state"

REAL="${REAL:-1}"
M_DIR="${1:-${MAPS_DIR:-config/maps}}"
M_DIR="${M_DIR/#\~/$HOME}"

if [ -z "${AURA_ACTIVE_WINDOW_TITLE:-}" ]; then
  AURA_ACTIVE_WINDOW_TITLE=$(python3 -c "
  import sys
  sys.path.insert(0, '$PROJECT_ROOT')
  from scripts.py.func.get_active_window_title import get_active_window_title_safe
  print(get_active_window_title_safe())
  " 2>/dev/null)
  export AURA_ACTIVE_WINDOW_TITLE
fi

H_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_history"
PROOT_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_proot"
[ -f "$PROOT_STATE_FILE" ] || echo "$PROJECT_ROOT/config/maps" > "$PROOT_STATE_FILE"

GITIGNORE_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_respect_gitignore"
[ -f "$GITIGNORE_STATE_FILE" ] || echo "0" > "$GITIGNORE_STATE_FILE"
#
#ONE_PER_FILE_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_one_per_file"
#[ -f "$ONE_PER_FILE_STATE_FILE" ] || echo "0" > "$ONE_PER_FILE_STATE_FILE"

ONE_PER_FILE_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_one_per_file"
[ -f "$ONE_PER_FILE_STATE_FILE" ] || echo "0" > "$ONE_PER_FILE_STATE_FILE"

SINGLE_GUI_STATE_FILE="$PROJECT_ROOT/data/_search_rules_state/.search_rules_single_gui"
[ -f "$SINGLE_GUI_STATE_FILE" ] || echo "1" > "$SINGLE_GUI_STATE_FILE"

get_one_per_file_flag() {
    cat "$ONE_PER_FILE_STATE_FILE" 2>/dev/null || echo "0"
}

get_single_gui_flag() {
    cat "$SINGLE_GUI_STATE_FILE" 2>/dev/null || echo "1"
}

if [ "${1:-}" != "--load-full" ] && [ "${1:-}" != "--load-scoped" ]; then
    if [ "$(get_single_gui_flag)" = "1" ]; then
        MY_PID=$$
        for pid in $(pgrep -f "run_rule.sh"); do
            if [ "$pid" -ne "$MY_PID" ] && [ "$pid" -ne "$BASHPID" ] && [ "$pid" -ne "$PPID" ]; then
                if ! pgrep -P "$MY_PID" 2>/dev/null | grep -q "^${pid}$"; then
                    kill -9 "$pid" 2>/dev/null || true
                fi
            fi
        done
    fi
fi

get_ignore_flag() {
    local respect
    respect=$(cat "$GITIGNORE_STATE_FILE" 2>/dev/null)
    if [ "$respect" = "1" ]; then
        echo ""
    else
        echo "--no-ignore"
    fi
}

cp "$H_FILE" "$H_FILE.bak"

# Deduplicate
tac "$H_FILE" | awk '!seen[$0]++' | tac > "$H_FILE.tmp" && mv "$H_FILE.tmp" "$H_FILE"

IQ=".py pre # EXAMPLE:"

[ -s "$H_FILE" ] && IQ=$(tail -n 1 "$H_FILE")

AWK_SCRIPT='{
    full_path = $1;
    line = $2;
    content = substr($0, index($0, ":" line ":") + length(line) + 2);
    gsub(/^[ \t]+/, "", content);
    if (length(content) == 0) next;
    short_path = full_path;

    gsub(proot, "⬟", short_path);
    gsub(/\/de-DE\//, "🇩🇪", short_path);
    gsub(/\/en-US\//, "🇬🇧", short_path);
    gsub(/config\/maps\//, "🗺️", short_path);
    gsub(/plugins\//, "🧩", short_path);
    if (one_per_file == "1") {
        if (full_path == prev_full_path) next;
    }    gsub(/FUZZY_MAP_pre\.py/, "⚙️", short_path);
    gsub(/FUZZY_MAP\.py/, "📄", short_path);
    gsub(/PUNCTUATION_MAP\.py/, "※", short_path);
    if (use_ditto == "1") {
        if (full_path == prev_full_path_ditto) {
            ditto_count++;
        } else {
            ditto_count = 0;
        }

        if (ditto_count >= 10) {
            display_path = short_path;
            ditto_count = 0;
        } else if (full_path == prev_full_path) {
            display_path = "〃";
        } else {
            display_path = short_path;
        }
        prev_full_path = full_path;
    } else {
        display_path = short_path;
    }

    display = display_path ":" line " | " content;
    print display "\t" full_path "\t" line;
}'

get_scoped_search_input() {
    local scope_dir
    scope_dir=$(cat "$PROOT_STATE_FILE" 2>/dev/null)
    [ -z "$scope_dir" ] || [ ! -d "$scope_dir" ] && scope_dir="$PROJECT_ROOT/config/maps"
    rg -nH $(get_ignore_flag) $FILT "^" "$scope_dir" | sort -t: -k1,1 -k2,2n | awk -F: -v proot="$PROJECT_ROOT" -v use_ditto="1" -v one_per_file="$(get_one_per_file_flag)" "$AWK_SCRIPT"
}


if [ "${1:-}" = "--load-full" ]; then
    FULL_ROOT=$(cat "$PROOT_STATE_FILE" 2>/dev/null)
    [ -z "$FULL_ROOT" ] || [ ! -d "$FULL_ROOT" ] && FULL_ROOT="$PROJECT_ROOT/config/maps"
    rg -nH $(get_ignore_flag) $FILT "^" "$FULL_ROOT" | sort -t: -k1,1 -k2,2n | awk -F: -v proot="$PROJECT_ROOT" -v use_ditto="0" -v one_per_file="$(get_one_per_file_flag)" "$AWK_SCRIPT"
    exit 0
fi


if [ "${1:-}" = "--load-scoped" ]; then
    get_scoped_search_input
    exit 0
fi

RESTART_MARKER="/tmp/.search_rules_restart_$$"
rm -f "$RESTART_MARKER"
CURRENT_QUERY="$IQ"
while true; do
    ONE_PER_FILE_STATE=$(get_one_per_file_flag)

if [ "$ONE_PER_FILE_STATE" = "1" ]; then
        ALT_F_ACTION="transform:
            bash \$SCRIPT_DIR/toggle_one_per_file.sh
            echo restart > $RESTART_MARKER
            echo 'abort'"
    else
        ALT_F_ACTION="transform:
            echo {q} > ${RESTART_MARKER}.saved_query
            echo \"\" > ${RESTART_MARKER}.query
            bash \$SCRIPT_DIR/toggle_one_per_file.sh
            echo restart > $RESTART_MARKER
            echo 'abort'"
    fi

    if [ -n "$CURRENT_QUERY" ]; then
        INIT_INPUT=$(bash "$SCRIPT_DIR/run_rule.sh" --load-full)
        DITO_STATE="0"
        SORT_OPT=""
    else
        INIT_INPUT=$(get_scoped_search_input)
        DITO_STATE="1"
        SORT_OPT="--no-sort"
    fi
    echo "$DITO_STATE" > "$PROJECT_ROOT/data/_search_rules_state/.search_rules_ditto"
    F_OUT=$(echo "$INIT_INPUT" | \
        fzf --print-query \
            --no-hscroll \
            --layout=reverse \
            $SORT_OPT \
            --delimiter=$'\t' \
            --bind="change:transform:
                q={q}
                if [ -n \"\$q\" ] && [ \"$DITO_STATE\" = \"1\" ]; then
                    echo \"\$q\" > ${RESTART_MARKER}.query
                    echo restart > $RESTART_MARKER
                    echo 'abort'
                elif [ -z \"\$q\" ] && [ \"$DITO_STATE\" = \"0\" ]; then
                    echo \"\" > ${RESTART_MARKER}.query
                    echo restart > $RESTART_MARKER
                    echo 'abort'
                fi" \
            --bind="alt-g:execute-silent(echo restart > $RESTART_MARKER)+clear-query+abort" \
            --bind="alt-f:$ALT_F_ACTION" \
            --bind="alt-i:execute-silent(bash \$SCRIPT_DIR/toggle_gitignore.sh; echo restart > $RESTART_MARKER)+abort" \
            --bind="alt-u:execute-silent(bash \$SCRIPT_DIR/toggle_single_gui.sh; echo restart > $RESTART_MARKER)+abort" \
            --bind="right-click:execute-silent(bash \$SCRIPT_DIR/proot_control.sh up \$PROJECT_ROOT/config/maps; echo restart > $RESTART_MARKER)+abort" \
            --bind="double-click:execute-silent(bash \$SCRIPT_DIR/proot_control.sh set \$PROJECT_ROOT/config/maps \"\$(dirname \$(dirname \$(cat \$PROJECT_ROOT/data/_search_rules_state/.search_rules_last_path)))\"; echo restart > $RESTART_MARKER)+clear-query+abort" \
            --bind="alt-r:execute-silent(bash \$SCRIPT_DIR/proot_control.sh reset \$PROJECT_ROOT/config/maps; echo restart > $RESTART_MARKER)+abort" \
            --history="$H_FILE" --query="$CURRENT_QUERY" \
            --with-nth=1 \
            --header="Caller:${AURA_ACTIVE_WINDOW_TITLE:0:3} |Enter: EXAMPLE / Ctrl+R: prompt | Ctrl+E: Edit | Alt+G: Ditto | Alt+F: 1/File | 2xClick: Set | RClick: Up | Alt+R: Reset | F1: Legend"  \
            --bind="f1:execute-silent(bash \$SCRIPT_DIR/toggle_legend.sh)+refresh-preview" \
            --bind="ctrl-z:previous-history" \
            --bind="ctrl-y:next-history" \
            --bind="ctrl-backspace:backward-kill-word" \
            --bind="ctrl-delete:kill-word" \
            --bind="ctrl-left:backward-word" \
            --bind="ctrl-right:forward-word" \
            --bind="ctrl-up:up+up+up+up+up" \
            --bind="ctrl-down:down+down+down+down+down" \
            --bind="home:beginning-of-line" \
            --bind="end:end-of-line" \
            --bind="ctrl-g:execute-silent(f={2}; rel=\${f#\$PROJECT_ROOT/}; systemd-run --user --collect --quiet xdg-open \"\$REPO_URL/\$rel#L{3}\")" \
            --expect="ctrl-e,ctrl-r" \
            --preview='python3 '"$SCRIPT_DIR"'/preview_rule.py {2} {3}' \
    )

    if [ -f "$RESTART_MARKER" ]; then
        rm -f "$RESTART_MARKER"

        if [ -s "${RESTART_MARKER}.saved_query" ]; then
            SAVED_QUERY=$(cat "${RESTART_MARKER}.saved_query")
            rm -f "${RESTART_MARKER}.saved_query"
        fi

        ONE_PER_FILE_STATE=$(get_one_per_file_flag)
        if [ "$ONE_PER_FILE_STATE" = "0" ] && [ -n "$SAVED_QUERY" ]; then
            CURRENT_QUERY="$SAVED_QUERY"
            SAVED_QUERY=""
        elif [ -f "${RESTART_MARKER}.query" ]; then
            CURRENT_QUERY=$(cat "${RESTART_MARKER}.query" 2>/dev/null)
            rm -f "${RESTART_MARKER}.query"
        fi

        continue
    fi
    break
done
rm -f "$RESTART_MARKER"
[[ -z "$F_OUT" ]] && exit 0
QUERY_TYPED=$(echo "$F_OUT" | sed -n '1p')
KEY=$(echo "$F_OUT" | sed -n '2p')

SEL=$(echo "$F_OUT" | sed -n '3p')
if [[ -n "$SEL" ]]; then
    F_PATH="$(echo "$SEL" | cut -f2)"
    L_NUM="$(echo "$SEL" | cut -f3)"
else
    F_PATH=""
    L_NUM=""
fi

logger_info "DBG typed='$QUERY_TYPED' key='$KEY' sel='$SEL'"

if [[ -z "$KEY" || "$KEY" = "ctrl-r" ]]; then
    logger_info "43: KEY=$KEY"
    QUERY=""
    if [[ -z "$KEY" && -n "$SEL" ]]; then
        logger_info "50: Enter pressed -> use"
        logger_info "$F_PATH:$L_NUM"
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
    logger_info "178: ctrl-e entered editor='$PREFERRED_EDITOR' path='$F_PATH' line='$L_NUM'"
    if [[ "$PREFERRED_EDITOR" = "cudatext" ]]; then
      nohup "$PREFERRED_EDITOR" "$F_PATH@$L_NUM" >> "$LOGFILE" 2>&1 &
    else
      nohup "$PREFERRED_EDITOR" "$F_PATH" --line="$L_NUM" >> "$LOGFILE" 2>&1 &
    fi
    logger_info "185: spawned pid=$!"
fi
