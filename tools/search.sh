#!/usr/bin/env bash
# Repository-wide search tool filtering ignored and deleted files with regex support.
# - MANDATORY SEARCH RULE: Always use the repository search script instead of custom grep commands:
#   tools/search.sh "search_string" [optional_path_prefix]
#   Options available: -i (case-insensitive), -E (regex), -w (whole word).

clear

set -euo pipefail

GREP_FLAGS="-Hn"
INCLUDE_DOC_SOURCES=false
ignore_comments=true 

show_usage() {
  cat <<'USAGE'
Usage: tools/search.sh PATTERN [PATH_PREFIX] [OPTIONS]
  PATTERN       Search string or regex pattern (required)
  PATH_PREFIX   Limit search to this path (default: '.')
Options:
  -i, --ignore-case          Case-insensitive search
  -E, --extended-regexp      Enable extended regex syntax
  -w, --word-regexp          Match whole words only
  -a, --all                  Include doc_sources directory (excluded by default)
Examples:
  tools/search.sh "def execute" scripts
  tools/search.sh "TODO" . -i
  tools/search.sh "class \w+Error" . -E
USAGE
}

while [[ $# -gt 0 && "$1" == -* ]]; do
  case "$1" in
    -i|--ignore-case) GREP_FLAGS="$GREP_FLAGS -i" ;;
    -E|--extended-regexp) GREP_FLAGS="$GREP_FLAGS -E" ;;
    -w|--word-regexp) GREP_FLAGS="$GREP_FLAGS -w" ;;
    -a|--all|--include-doc-sources) INCLUDE_DOC_SOURCES=true ;;
    -h|--help) show_usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

#PATTERN="${1:?Provide search pattern or regex}"

#if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
#  cat <<'USAGE'

show_usage() {
  cat <<'USAGE'
Usage: tools/search.sh PATTERN [PATH_PREFIX] [OPTIONS]

  PATTERN       Search string or regex pattern (required)
  PATH_PREFIX   Limit search to this path (default: '.')

Options:
  -i, --ignore-case          Case-insensitive search
  -E, --extended-regexp      Enable extended regex syntax
  -w, --word-regexp          Match whole words only
  -a, --all                  Include doc_sources directory (excluded by default)

Examples:
  tools/search.sh "def execute" scripts
  tools/search.sh "TODO" . -i
  tools/search.sh "class \w+Error" . -E
USAGE
}
PATTERN="${1:?Provide search pattern or regex. Use -h for help.}"

PREFIX="${2:-.}"

clear
#echo "tools/search.sh '$PATTERN' # flags='$GREP_FLAGS' prefix='$PREFIX'" >&2

echo "tools/search.sh '$PATTERN' # flags='$GREP_FLAGS' prefix='$PREFIX' [help: -h]  include_doc_sources='$INCLUDE_DOC_SOURCES'" >&2

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

if [ "$ignore_comments" = "true" ]; then  
  matches=$(do_search "$PATTERN" \
  | sed 's/[[:space:]]*#.*$//' \
  | { grep -E -- "$PATTERN" || true; } \
  | { head -n 201; } || true )  
else
# matches=$(do_search "$PATTERN" | head -n 201)
 matches=$( { do_search "$PATTERN" | head -n 201; } || true )
fi

count=$(echo -n "$matches" | grep -c '^' || true)

if [ "$count" -eq 0 ]; then
  echo "nothing found" >&2
  exit 0
fi


if [ "$count" -gt 200 ] && [[ "$GREP_FLAGS" != *"-w"* && "$PATTERN" != *"\\b"* ]]; then
  REFINED_PATTERN="\\b${PATTERN}\\b"






#  refined_matches=$(do_search "$REFINED_PATTERN" | head -n 201)
  refined_matches=$( { do_search "$REFINED_PATTERN" | head -n 201; } || true )
  refined_count=$(echo -n "$refined_matches" | grep -c '^' || true)

#  echo 22222222222222222222222222222222222222222222222
#
#   refined_matches=$(do_search "$REFINED_PATTERN" | grep -v '^\s*#' | head -n 201)
#   echo 33333333333333333333333333333333333333333333333333333
#   refined_count=$(printf '%s' "$refined_matches" | grep -c '^' || true)



  echo "⚠️⚠️Results exceeded 200 lines. Automatically refining pattern with word boundaries: '$REFINED_PATTERN'..." >&2




  if [ "$refined_count" -gt 0 ]; then
    matches="$refined_matches"
    count="$refined_count"
#  else 
#    echo 1111111111111111111111111
#    exit 
  fi
fi

#echo 444444444444444444444444444444444444444444444
if [ "$count" -gt 200 ]; then
#  echo 5555555555555555555555555555555555555
  echo "Results still exceed 200 lines. Truncating output to top 200 matches:" >&2
  echo "$matches" | head -n 200
else
  echo "count = $count" 
#  echo 6666666666666666666666666666666666666666666666666666666666
  echo "$matches"
fi
echo '___________________________________________'

