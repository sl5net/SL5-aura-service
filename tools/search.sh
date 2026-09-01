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

# do_search() Version: 1.9.'26 10:58 Tue
#do_search() {
#  local cur_pat="$1"
#  (git ls-files "$PREFIX" && git ls-files --others --exclude-standard -- "$PREFIX") | \
#    grep -Ev "$EXCLUDE_PAT" | \
#    while IFS= read -r f; do
#      [ -f "$f" ] && grep $GREP_FLAGS -E "$cur_pat" "$f" 2>/dev/null || true
#    done
#}

EXCLUDE_FILE_PAT='[^/]*(backup|BACKUP|draft)'

# Before: 1.9.'26 11:51 Tue
#ALL_FILES=$( (git ls-files "$PREFIX" && git ls-files --others --exclude-standard -- "$PREFIX") | grep -Ev "$EXCLUDE_PAT" || true )

get_matched_files() {
  local target_prefix="$1"
  (git ls-files "$target_prefix" && git ls-files --others --exclude-standard -- "$target_prefix") | grep -Ev "$EXCLUDE_PAT" || true
}

ALL_FILES=$(get_matched_files "$PREFIX")

if [ -z "$ALL_FILES" ] && [ ! -e "$PREFIX" ] && [[ "$PREFIX" != *"*"* ]]; then
  ALL_FILES=$(get_matched_files "$PREFIX*")
fi

if [ -z "$ALL_FILES" ]; then
  echo "Hint: No files matched path prefix '$PREFIX'. Ensure it is a valid directory or pattern (e.g. '$PREFIX*')." >&2
fi

EXCLUDED_COUNT=0

if [ -n "$ALL_FILES" ]; then
  EXCLUDED_COUNT=$(printf '%s\n' "$ALL_FILES" | grep -iE "$EXCLUDE_FILE_PAT" -c || true)
fi

if [ "$EXCLUDED_COUNT" -gt 0 ]; then
  echo "Excluded $EXCLUDED_COUNT backup/draft file(s) from search." >&2
fi

TARGET_FILES=$( [ -n "$ALL_FILES" ] && printf '%s\n' "$ALL_FILES" | grep -viE "$EXCLUDE_FILE_PAT" || true )



do_search() {
  local cur_pat="$1"
  printf '%s\n' "$TARGET_FILES" | \
    while IFS= read -r f; do
      [ -n "$f" ] && [ -f "$f" ] && grep $GREP_FLAGS -E "$cur_pat" "$f" 2>/dev/null || true
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


if [ "$count" -gt 29 ] && [[ "$GREP_FLAGS" != *"-w"* && "$PATTERN" != *"\\b"* ]]; then
  REFINED_PATTERN="\\b${PATTERN}\\b"






#  refined_matches=$(do_search "$REFINED_PATTERN" | head -n 201)
  refined_matches=$( { do_search "$REFINED_PATTERN" | head -n 201; } || true )
  refined_count=$(echo -n "$refined_matches" | grep -c '^' || true)

#  echo 22222222222222222222222222222222222222222222222
#
#   refined_matches=$(do_search "$REFINED_PATTERN" | grep -v '^\s*#' | head -n 201)
#   echo 33333333333333333333333333333333333333333333333333333
#   refined_count=$(printf '%s' "$refined_matches" | grep -c '^' || true)



  echo "⚠️⚠️Results exceeded 29 lines. Automatically refining pattern with word boundaries: '$REFINED_PATTERN'..." >&2




  if [ "$refined_count" -gt 0 ]; then
    matches="$refined_matches"
    count="$refined_count"
#  else 
#    echo 1111111111111111111111111
#    exit 
  fi
fi

#echo 444444444444444444444444444444444444444444444
if [ "$count" -gt 29 ]; then
#  echo 5555555555555555555555555555555555555
  echo "Results still exceed 29 lines. Truncating output to top 29 matches:" >&2
  echo "$matches" | head -n 29
else
  echo "count = $count" 
#  echo 6666666666666666666666666666666666666666666666666666666666
  echo "$matches"
  if [ "$count" -eq 1 ]; then
    match_file=$(echo "$matches" | cut -d: -f1)
    echo "grep -n -C 5 \"$PATTERN\" '$match_file'"
  fi
fi
echo '___________________________________________'

