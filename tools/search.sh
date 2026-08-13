#!/usr/bin/env bash
# Repository-wide search tool filtering ignored and deleted files with regex support.
# - MANDATORY SEARCH RULE: Always use the repository search script instead of custom grep commands:
#   tools/search.sh "search_string" [optional_path_prefix]
#   Options available: -i (case-insensitive), -E (regex), -w (whole word).

set -euo pipefail

GREP_FLAGS="-Hn"
INCLUDE_DOC_SOURCES=false

while [[ $# -gt 0 && "$1" == -* ]]; do
  case "$1" in
    -i|--ignore-case) GREP_FLAGS="$GREP_FLAGS -i" ;;
    -E|--extended-regexp) GREP_FLAGS="$GREP_FLAGS -E" ;;
    -w|--word-regexp) GREP_FLAGS="$GREP_FLAGS -w" ;;
    -a|--all|--include-doc-sources) INCLUDE_DOC_SOURCES=true ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

PATTERN="${1:?Provide search pattern or regex}"
PREFIX="${2:-.}"

clear
#echo "tools/search.sh '$PATTERN' # flags='$GREP_FLAGS' prefix='$PREFIX'" >&2
echo "tools/search.sh '$PATTERN' # flags='$GREP_FLAGS' prefix='$PREFIX' include_doc_sources='$INCLUDE_DOC_SOURCES'" >&2

EXCLUDE_PAT="\.i18n|/__pycache__/|/\.venv/|/venv/"
if [ "$INCLUDE_DOC_SOURCES" = "false" ]; then
  EXCLUDE_PAT="$EXCLUDE_PAT|doc_sources"
fi

do_search() {
  local cur_pat="$1"
  (git ls-files "$PREFIX" && git ls-files --others --exclude-standard -- "$PREFIX") | \
    grep -Ev "$EXCLUDE_PAT" | \
    while IFS= read -r f; do
      [ -f "$f" ] && grep $GREP_FLAGS -E "$cur_pat" "$f" 2>/dev/null || true
    done
}

matches=$(do_search "$PATTERN" | head -n 201)
count=$(echo -n "$matches" | grep -c '^' || true)

if [ "$count" -eq 0 ]; then
  echo "nothing found" >&2
  exit 0
fi

if [ "$count" -gt 200 ] && [[ "$GREP_FLAGS" != *"-w"* && "$PATTERN" != *"\\b"* ]]; then
  REFINED_PATTERN="\\b${PATTERN}\\b"
  echo "Results exceeded 200 lines. Automatically refining pattern with word boundaries: '$REFINED_PATTERN'..." >&2
  refined_matches=$(do_search "$REFINED_PATTERN" | head -n 201)
  refined_count=$(echo -n "$refined_matches" | grep -c '^' || true)
  if [ "$refined_count" -gt 0 ]; then
    matches="$refined_matches"
    count="$refined_count"
  fi
fi

if [ "$count" -gt 200 ]; then
  echo "Results still exceed 200 lines. Truncating output to top 200 matches:" >&2
  echo "$matches" | head -n 200
else
  echo "$matches"
fi
