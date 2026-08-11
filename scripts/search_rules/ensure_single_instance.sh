#!/usr/bin/env bash
# Helper script to enforce a single running instance of run_rule.sh when SINGLE_GUI mode is active.

SINGLE_GUI_STATE_FILE="${SINGLE_GUI_STATE_FILE:-/tmp/aura_single_gui_state}"

get_single_gui_flag() {
    cat "$SINGLE_GUI_STATE_FILE" 2>/dev/null || echo "1"
}

ensure_single_instance() {
    local mode="${1:-}"
    if [ "$mode" != "--load-full" ] && [ "$mode" != "--load-scoped" ]; then
        if [ "$(get_single_gui_flag)" = "1" ]; then
            local my_pid=$$
            local pid
            for pid in $(pgrep -f "run_rule.sh"); do
                if [ "$pid" -ne "$my_pid" ] && [ "$pid" -ne "$BASHPID" ] && [ "$pid" -ne "$PPID" ]; then
                    if ! pgrep -P "$my_pid" 2>/dev/null | grep -q "^${pid}$"; then
                        kill -9 "$pid" 2>/dev/null || true
                    fi
                fi
            done
        fi
    fi
}

ensure_single_instance "$@"
