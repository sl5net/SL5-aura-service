#!/usr/bin/env bash
# Utility script to automatically restructure search_rules helper scripts into func/ subdirectories.

set -euo pipefail

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
BASE_DIR="$SL5NET_AURA_PROJECT_ROOT/scripts/search_rules"

echo "Creating func/ directory structure..."
mkdir -p "$BASE_DIR/func/common"
mkdir -p "$BASE_DIR/func/linux"

echo "Moving helper scripts..."
[ -f "$BASE_DIR/get_ignore_flag.sh" ] && mv "$BASE_DIR/get_ignore_flag.sh" "$BASE_DIR/func/common/"
[ -f "$BASE_DIR/get_one_per_file_flag.sh" ] && mv "$BASE_DIR/get_one_per_file_flag.sh" "$BASE_DIR/func/common/"
[ -f "$BASE_DIR/ensure_single_instance.sh" ] && mv "$BASE_DIR/ensure_single_instance.sh" "$BASE_DIR/func/linux/"
[ -f "$BASE_DIR/get_active_window_title.sh" ] && mv "$BASE_DIR/get_active_window_title.sh" "$BASE_DIR/func/linux/"

echo "Updating sourcing paths in run_rule.sh..."
RUN_RULE="$BASE_DIR/run_rule.sh"
if [ -f "$RUN_RULE" ]; then
    sed -i 's|source "$SCRIPT_DIR/get_active_window_title.sh"|source "$SCRIPT_DIR/func/linux/get_active_window_title.sh"|g' "$RUN_RULE"
    sed -i 's|source "$SCRIPT_DIR/get_one_per_file_flag.sh"|source "$SCRIPT_DIR/func/common/get_one_per_file_flag.sh"|g' "$RUN_RULE"
    sed -i 's|source "$SCRIPT_DIR/ensure_single_instance.sh"|source "$SCRIPT_DIR/func/linux/ensure_single_instance.sh"|g' "$RUN_RULE"
    sed -i 's|source "$SCRIPT_DIR/get_ignore_flag.sh"|source "$SCRIPT_DIR/func/common/get_ignore_flag.sh"|g' "$RUN_RULE"
fi

echo "Migration completed successfully."
