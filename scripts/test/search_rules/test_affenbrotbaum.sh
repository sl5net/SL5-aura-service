#!/bin/bash
clear
# scripts/search_rules/test_affenbrotbaum.sh
# Diagnostic test suite for the "Affenbrotbaum" fzf matching issue.
# Extend this script with additional tests as the investigation continues.
#
# Usage:
#   bash scripts/search_rules/test_affenbrotbaum.sh              -> run all automated tests
#   bash scripts/search_rules/test_affenbrotbaum.sh --prep-t7     -> clear log, print manual instructions
#   bash scripts/search_rules/test_affenbrotbaum.sh --check-t7    -> parse log after manual run

source "$(dirname "${BASH_SOURCE[0]}")/search_helpers.sh"
cd "$PROJECT_ROOT" || exit 1

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGFILE="$PROJECT_ROOT/log/test_affenbrotbaum.sh.log"
mkdir -p "$PROJECT_ROOT/log"

TARGET_FILE="$PROJECT_ROOT/config/maps/_privat/job/bewerbung/de-DE/FUZZY_MAP_pre.py"
NEEDLE="aff"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}

pass_fail() {
    local test_name="$1"
    local count="$2"
    local detail="$3"
    if [ "$count" -gt 0 ]; then
        echo "[PASS] $test_name (matches=$count)"
        log "PASS $test_name matches=$count detail=$detail"
    else
        echo "[FAIL] $test_name (matches=$count)"
        log "FAIL $test_name matches=$count detail=$detail"
    fi
}

run_automated_tests() {
    log "=== Automated test run started ==="

    T1=$(rg -c -F "$NEEDLE" "$TARGET_FILE" 2>/dev/null)
    T1=${T1:-0}
    pass_fail "T1_rg_direct_file" "$T1" "target=$TARGET_FILE"

    FULL_OUT=$(bash "$SCRIPT_DIR/run_rule.sh" --load-full 2>/dev/null)
    T2=$(echo "$FULL_OUT" | grep -cF "$NEEDLE")
    pass_fail "T2_load_full_pipeline" "$T2" "mode=load-full"

    SCOPED_OUT=$(bash "$SCRIPT_DIR/run_rule.sh" --load-scoped 2>/dev/null)
    T3=$(echo "$SCOPED_OUT" | grep -cF "$NEEDLE")
    pass_fail "T3_load_scoped_pipeline" "$T3" "proot=$(cat "$HOME/.search_rules_proot" 2>/dev/null)"

    T4=$(echo "$FULL_OUT" | fzf --delimiter=$'\t' --with-nth=1 --filter="$NEEDLE" 2>/dev/null | wc -l)
    pass_fail "T4_fzf_filter_on_full_output" "$T4" "mode=non-interactive-filter"

    T4B=$(echo "$FULL_OUT" | fzf --delimiter=$'\t' --with-nth=1 --filter="$NEEDLE" 2>/dev/null | grep -cF "$TARGET_FILE")
    pass_fail "T4b_fzf_filter_contains_target_line" "$T4B" "target=$TARGET_FILE"

    T5=$(echo -e "EXAMPLE: $NEEDLE" | fzf --filter="$NEEDLE" 2>/dev/null | wc -l)
    pass_fail "T5_fzf_filter_minimal_line" "$T5" "mode=synthetic-single-line"

    H_FILE="$HOME/.search_rules_history"
    LAST_IQ=$(tail -n 1 "$H_FILE" 2>/dev/null)
    if [ -z "$LAST_IQ" ]; then
        echo "[PASS] T6_history_query_empty (matches=1)"
        log "PASS T6_history_query_empty last_iq='(empty)'"
    else
        echo "[INFO] T6_history_query_empty last_iq='$LAST_IQ'"
        log "INFO T6_history_query_empty last_iq='$LAST_IQ'"
    fi

    echo "[INFO] T7_interactive: run '--prep-t7' then test manually, then '--check-t7'"
    log "=== Automated test run finished ==="
    echo "Full log: log/test_affenbrotbaum.sh.log"
}

prep_t7() {
    : > "$LOGFILE"
    log "=== T7 prep: log cleared, waiting for manual interactive run ==="
    echo "[INFO] Log cleared. Now run:"
    echo "  AFFEN_DEBUG=1 bash scripts/search_rules/run_rule.sh"
    echo "Type '$NEEDLE' character by character, then press Esc."
    echo "Then run: bash scripts/search_rules/test_affenbrotbaum.sh --check-t7"
}

check_t7() {
    if [ ! -s "$LOGFILE" ]; then
        echo "[FAIL] T7_interactive_log_empty (matches=0)"
        return
    fi
    T7_COUNT=$(grep -c "live_query=" "$LOGFILE")
    pass_fail "T7_interactive_query_events_logged" "$T7_COUNT" "events=$T7_COUNT"

    T7_LAST=$(grep "live_query=" "$LOGFILE" | tail -1)
    echo "[INFO] T7_last_query_event: $T7_LAST"

    T7_MATCH=$(grep "live_query='$NEEDLE'" "$LOGFILE" | tail -1)
    if [ -n "$T7_MATCH" ]; then
        echo "[PASS] T7b_exact_needle_query_found: $T7_MATCH"
    else
        echo "[FAIL] T7b_exact_needle_query_found (no exact match logged)"
    fi
}

case "${1:-}" in
    --prep-t7) prep_t7 ;;
    --check-t7) check_t7 ;;
    *) run_automated_tests ;;
esac
