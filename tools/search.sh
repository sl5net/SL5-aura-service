#!/usr/bin/env bash
# Repository-wide search tool filtering ignored and deleted files with regex support.
# - MANDATORY SEARCH RULE: Always use the repository search script instead of custom grep commands:
#   tools/search.sh "search_string" [optional_path_prefix]
#   Options available: -i (case-insensitive), -E (regex), -w (whole word).

set -euo pipefail

GREP_FLAGS="-Hn"

while [[ $# -gt 0 && "$1" == -* ]]; do
  case "$1" in
    -i|--ignore-case) GREP_FLAGS="$GREP_FLAGS -i" ;;
    -E|--extended-regexp) GREP_FLAGS="$GREP_FLAGS -E" ;;
    -w|--word-regexp) GREP_FLAGS="$GREP_FLAGS -w" ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

PATTERN="${1:?Provide search pattern or regex}"
PREFIX="${2:-.}"

(git ls-files "$PREFIX" && git ls-files --others --exclude-standard -- "$PREFIX") | \
  grep -Ev "\.i18n|/__pycache__/|/\.venv/|/venv/|doc_sources" | \
  while IFS= read -r f; do
    [ -f "$f" ] && grep $GREP_FLAGS -E "$PATTERN" "$f" 2>/dev/null || true
  done
