#!/usr/bin/env bash

# tools/tests/TEST_FILE4REPLACEMENT.sh:3

set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

OUTSIDE_TEST_FILE="tools/tests/TEST_FILE4REPLACEMENT.txt"
echo "--- Creating on-the-fly test file: $OUTSIDE_TEST_FILE ---"
echo "Blumenkohl sagt hallo" > "$OUTSIDE_TEST_FILE"

SETTINGS_FILE="config/settings_local.py"
MAP_FILE="config/maps/plugins/TEST/FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py"

echo "--- Enabling DEV_MODE_all_processing ---"
sed -i 's/^DEV_MODE_all_processing = 0/DEV_MODE_all_processing = 1/' "$SETTINGS_FILE"

echo "--- Clearing all log files in log/ ---"
find log/ -type f -name '*.log' -exec truncate -s 0 {} \;

echo "--- Current TEST_FILE4REPLACEMENT FUZZY_MAP_pre rules ---"
cat "$MAP_FILE"

echo "--- Test 1: Zebra (relative, '.' prefix, inside plugin dir) ---"
.venv/bin/python3 scripts/py/cli_client.py "Zebra" --lang de-DE

echo "--- Test 2: Blumenkohl (absolute path, outside plugin dir) ---"
.venv/bin/python3 scripts/py/cli_client.py "Blumenkohl" --lang de-DE

echo "--- Disabling DEV_MODE_all_processing ---"
sed -i 's/^DEV_MODE_all_processing = 1/DEV_MODE_all_processing = 0/' "$SETTINGS_FILE"

echo "--- Done ---"
