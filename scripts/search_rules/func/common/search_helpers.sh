#!/bin/bash
# scripts/search_rules/search_helpers.sh
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"
HELPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SL5NET_AURA_PROJECT_ROOT="${SL5NET_AURA_PROJECT_ROOT:-$(cd "$HELPER_DIR/../.." && pwd)}"
mkdir -p "$SL5NET_AURA_PROJECT_ROOT/log"
LOGFILE="$SL5NET_AURA_PROJECT_ROOT/log/$(basename "$0").log"

logger_info() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOGFILE"
}

get_preferred_editor() {
    for c in cudatext kate code xed gedit subl nano vi; do
        if command -v "$c" >/dev/null 2>&1; then echo "$c"; return; fi
    done
}
PREFERRED_EDITOR=$(get_preferred_editor)

open_github() {
    local url="$REPO_URL/${1#$SL5NET_AURA_PROJECT_ROOT/}#L$2"
    logger_info "Opening GitHub: $url"
    xdg-open "$url"
}
export -f open_github

