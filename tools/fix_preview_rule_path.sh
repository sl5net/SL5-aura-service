#!/usr/bin/env bash
# Utility script to investigate and fix duplicated path references to preview_rule.py in search_rules scripts.

set -euo pipefail

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SEARCH_RULES_DIR="$SL5NET_AURA_PROJECT_ROOT/scripts/search_rules"

echo "=== 1. Checking physical location of preview_rule.py ==="
REAL_PATH=""
if [ -f "$SEARCH_RULES_DIR/func/common/preview_rule.py" ]; then
    REAL_PATH="func/common/preview_rule.py"
    echo "Found at: $SEARCH_RULES_DIR/func/common/preview_rule.py"
elif [ -f "$SEARCH_RULES_DIR/preview_rule.py" ]; then
    REAL_PATH="preview_rule.py"
    echo "Found at: $SEARCH_RULES_DIR/preview_rule.py"
else
    echo "ERROR: preview_rule.py not found in expected locations!"
    exit 1
fi

echo "=== 2. Investigating references in run_rule.sh ==="
grep -n "preview_rule.py" "$SEARCH_RULES_DIR/run_rule.sh" || true

echo "=== 3. Fixing duplicated path segments in run_rule.sh ==="
# Remove any repeated func/common segments
sed -i 's|\(func/common/\)\+|func/common/|g' "$SEARCH_RULES_DIR/run_rule.sh"

# Ensure reference matches actual file location
if [ "$REAL_PATH" = "func/common/preview_rule.py" ]; then
    sed -i 's|\([^\/]\|^\|\$SCRIPT_DIR\/\)preview_rule\.py|\1func/common/preview_rule.py|g' "$SEARCH_RULES_DIR/run_rule.sh"
    sed -i 's|func/common/func/common/|func/common/|g' "$SEARCH_RULES_DIR/run_rule.sh"
fi

echo "=== 4. Verifying fixed references in run_rule.sh ==="
grep -n "preview_rule.py" "$SEARCH_RULES_DIR/run_rule.sh"

echo "Fix applied successfully."
