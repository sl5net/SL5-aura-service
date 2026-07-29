#### /usr/bin/env bash

deprecated

we use now python3 for this 29.7.'26 19:28 Wed


# tools/tests/TEST_Catch-All.sh

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

SETTINGS_FILE_TRAP="config/settings_local.py"
MAP_FILE_TRAP="config/maps/plugins/TEST/FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py"
cleanup() {
    git checkout -- "$MAP_FILE_TRAP" 2>/dev/null || true
    sed -i 's/^DEV_MODE_all_processing = 1/DEV_MODE_all_processing = 0/' "$SETTINGS_FILE_TRAP" 2>/dev/null || true
}
trap cleanup EXIT

echo "--- Enabling DEV_MODE_all_processing ---"



SETTINGS_FILE="config/settings_local.py"
MAP_FILE="config/maps/plugins/TEST/FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py"

sed -i 's/^DEV_MODE_all_processing = 0/DEV_MODE_all_processing = 1/' "$SETTINGS_FILE"

echo "--- Clearing all log files in log/ ---"
find log/ -type f -name '*.log' -exec truncate -s 0 {} \;

echo "--- Current TEST_Catch-All FUZZY_MAP_pre rules ---"
cat "$MAP_FILE"

echo "--- Test 1: Sandbox Catch-All with Sandbank ---"
# Dynamically append the catch-all rule to the active MAP_FILE


echo "--- Test 1: Sandbox Catch-All with Sandbank ---"
# Insert the catch-all rule as the last element INSIDE the FUZZY_MAP_pre list literal,
# since get_fuzzy_map_entries.py (AST-based) only parses entries that are
# part of the FUZZY_MAP_pre = [...] literal itself, not later .append() calls.
python3 - "$MAP_FILE" << 'PYEOF'
import sys
from pathlib import Path

map_file = Path(sys.argv[1])
content = map_file.read_text(encoding="utf-8")

catch_all_entry = (
    "    (f'{str(__file__)}', r'^(.*)$', 10, {\n"
    "        'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' "
    "/ '1_collect_unmatched_training' / 'collect_unmatched.py']\n"
    "    })\n"
)

idx = content.rfind("]")
if idx == -1:
    raise SystemExit("ERROR: no closing ']' found for FUZZY_MAP_pre list")

new_content = (
    content[:idx].rstrip().rstrip(",") + ",\n"
    "    # Catch-All rule inserted for testing\n"
    + catch_all_entry
    + content[idx:]
)

map_file.write_text(new_content, encoding="utf-8")
PYEOF

# Run cli_client with unmatched word "Sandbank" (ignore expected raise Exception exit code)
.venv/bin/python3 scripts/py/cli_client.py "Sandbank" --lang de-DE || true

echo "--- Updated MAP_FILE rules after Test 3 ---"
cat "$MAP_FILE"

echo "--- Logs of collect_unmatched (service_start.log, since collect_unmatched.py's"
echo "    own log() currently writes to the root logger, not its own FileHandler) ---"
SERVICE_LOG="log/service_start.log"
if [ ! -f "$SERVICE_LOG" ] || [ ! -s "$SERVICE_LOG" ]; then
    echo "INCONCLUSIVE: $SERVICE_LOG is missing or empty -> request likely never reached the plugin."
else
#    RAW_VALUE=$(grep "file_rule_path:" "$SERVICE_LOG" | tail -n 1 | sed 's/^.*file_rule_path: //')

    RAW_VALUE=$(grep "file_rule_path:" "$SERVICE_LOG" | tail -n 1 | sed 's/^.*file_rule_path: //' || true)

    if [ -z "$RAW_VALUE" ]; then
        echo "INCONCLUSIVE: no 'file_rule_path:' entry found in $SERVICE_LOG."
    elif [ -f "$RAW_VALUE" ]; then
        echo "OK: file_rule_path is a valid, existing file path: $RAW_VALUE"
    else
        echo "BUG CONFIRMED: file_rule_path is NOT a valid existing file path."
        echo "Logged value (first 120 chars): ${RAW_VALUE:0:120}"
        echo "-> resolve_file_replacement() may be applied before run_on_match_exec(),"
        echo "   OR the path resolution logic changed the expected value."
        echo "   Check: scripts/py/func/process_text_in_background.py:2303"
        echo "   and: scripts/py/func/process_text_in_background.py:2546"
    fi
fi




echo "--- Done ---"

