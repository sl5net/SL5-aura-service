#!/usr/bin/env bash
# Helper script to fetch and export AURA_ACTIVE_WINDOW_TITLE if not set.

SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

get_active_window_title() {
    if [ -z "${AURA_ACTIVE_WINDOW_TITLE:-}" ]; then
        AURA_ACTIVE_WINDOW_TITLE=$(PYTHONPATH="$SL5NET_AURA_PROJECT_ROOT" python3 -c "from scripts.py.func.get_active_window_title import get_active_window_title_safe; print(get_active_window_title_safe())" 2>/dev/null)
        export AURA_ACTIVE_WINDOW_TITLE
    fi
}

get_active_window_title "$@"
