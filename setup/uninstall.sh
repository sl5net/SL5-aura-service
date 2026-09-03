#!/usr/bin/env bash
set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Ensure python3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 is required to run the uninstaller." >&2
    exit 1
fi

chmod +x "$PROJECT_ROOT/scripts/py/uninstall.py"
python3 "$PROJECT_ROOT/scripts/py/uninstall.py" "$@"
