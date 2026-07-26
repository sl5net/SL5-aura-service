#!/usr/bin/env bash

# tools/tests/TEST_FILE4REPLACEMENT.sh:3

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUTSIDE_TEST_FILE="tools/tests/TEST_FILE4REPLACEMENT.txt"
echo "--- Creating on-the-fly test file: $OUTSIDE_TEST_FILE ---"
echo "Blumenkohl sagt hallo" > "$OUTSIDE_TEST_FILE"

SETTINGS_FILE="config/settings_local.py"
MAP_FILE="config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py"

echo "--- Enabling DEV_MODE_all_processing ---"
sed -i 's/^DEV_MODE_all_processing = 0/DEV_MODE_all_processing = 1/' "$SETTINGS_FILE"

echo "--- Clearing all log files in log/ ---"
find log/ -type f -name '*.log' -exec truncate -s 0 {} \;

echo "--- Current TEST_FILE4REPLACEMENT FUZZY_MAP_pre rules ---"
cat "$MAP_FILE"

echo "--- Test 1: Zebra (relative, '.' prefix, inside plugin dir) ---"
.venv/bin/python3 scripts/py/cli_client.py "Zebra" --lang de-DE || true

# ... (Bestehender Code bis Test 2) ...
echo "--- Test 2: Blumenkohl (absolute path, outside plugin dir) ---"
.venv/bin/python3 scripts/py/cli_client.py "Blumenkohl" --lang de-DE || true

echo "--- Test 3: Sandbox Catch-All with Sandbank ---"
# Dynamically append the catch-all rule to the active MAP_FILE
cat << 'EOF' >> "$MAP_FILE"

# Catch-All rule appended dynamically for testing
FUZZY_MAP_pre.append(
    (f'{str(__file__)}', r'^(.*)$', 10, {
        'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']
    })
)
EOF

# Run cli_client with unmatched word "Sandbank" (ignore expected raise Exception exit code)
.venv/bin/python3 scripts/py/cli_client.py "Sandbank" --lang de-DE || true

echo "--- Updated MAP_FILE rules after Test 3 ---"
cat "$MAP_FILE"

echo "--- Logs of collect_unmatched ---"
cat log/1_collect_unmatched_training.log 2>/dev/null || cat log/collect_unmatched.py.log 2>/dev/null || echo "No log found"

# Restore original MAP_FILE to keep git status clean
git checkout -- "$MAP_FILE"

echo "--- Disabling DEV_MODE_all_processing ---"
sed -i 's/^DEV_MODE_all_processing = 1/DEV_MODE_all_processing = 0/' "$SETTINGS_FILE"
echo "--- Done ---"

