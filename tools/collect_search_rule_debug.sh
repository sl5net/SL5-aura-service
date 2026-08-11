#!/usr/bin/env bash
set -uo pipefail

OUTPUT_FILE="log/collect_search_rule_debug.log"
mkdir -p "$(dirname "$OUTPUT_FILE")"

safe_cat() {
    local file_path="$1"
    echo "=== $file_path ==="
    if [ -f "$file_path" ]; then
        cat "$file_path"
    else
        echo "FILE NOT FOUND: $file_path"
    fi
    echo ""
}

{
    safe_cat "scripts/search_rules/run_rule.sh"
    safe_cat "scripts/search_rules/func/common/preview_rule.py"
    safe_cat "scripts/search_rules/func/common/toggle_gitignore.sh"
    safe_cat "scripts/search_rules/func/common/toggle_legend.sh"
    safe_cat "scripts/search_rules/func/common/toggle_one_per_file.sh"
    safe_cat "scripts/search_rules/func/common/toggle_single_gui.sh"
    safe_cat "scripts/search_rules/func/common/get_ignore_flag.sh"
    safe_cat "scripts/search_rules/func/common/get_one_per_file_flag.sh"

    echo "=== search: ALT_F_ACTION in scripts/search_rules ==="
    tools/search.sh "ALT_F_ACTION" scripts/search_rules
    echo ""

    echo "=== search: icon_f in scripts/search_rules ==="
    tools/search.sh "icon_f" scripts/search_rules
    echo ""

    echo "=== search: status legend symbol source ==="
    tools/search.sh "≣" scripts/search_rules
    echo ""

} > "$OUTPUT_FILE" 2>&1

echo "Report written to $OUTPUT_FILE"
