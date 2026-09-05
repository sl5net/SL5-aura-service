#!/usr/bin/env bash
# Repository-wide search tool filtering ignored and deleted files with regex support.
# - MANDATORY SEARCH RULE: Always use the repository search script instead of custom grep commands:
#   tools/search.sh "search_string" [optional_path_prefix]
#   Options available: -i (case-insensitive), -E (regex), -w (whole word).

clear

set -euo pipefail

ORIG_ARGS=("$@")

GREP_FLAGS="-Hn"

MATCH_FLAGS=""
INCLUDE_DOC_SOURCES=false
ignore_comments=true
SEARCH_EXT="py"
ALL_EXT=false

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
  -e, --ext <ext>            Filter by specific file extension (default: py)
  --all-ext                  Search all file extensions
  -c, --include-comments     Also show matches that only occur in comments
                              (default: comment-only matches, e.g. shebang
                              lines, are stripped and hidden)
Examples:
  tools/search.sh "def execute" scripts
  tools/search.sh "TODO" . -i
  tools/search.sh "class \w+Error" . -E
  tools/search.sh "bin/bash" scripts -e sh
  tools/search.sh "pattern" . --all-ext
  tools/search.sh "bin/bash" scripts -e sh -c
USAGE
}

# Options and positional args (PATTERN, PATH_PREFIX) may appear in any order,
# e.g. both `search.sh -i "TODO" .` and `search.sh "TODO" . -i` must work.
# We scan every argument instead of stopping at the first non-flag token,
# collecting positionals separately from flags.
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    -i|--ignore-case) GREP_FLAGS="$GREP_FLAGS -i"; MATCH_FLAGS="$MATCH_FLAGS -i" ;;
    -E|--extended-regexp) GREP_FLAGS="$GREP_FLAGS -E"; MATCH_FLAGS="$MATCH_FLAGS -E" ;;
    -w|--word-regexp) GREP_FLAGS="$GREP_FLAGS -w"; MATCH_FLAGS="$MATCH_FLAGS -w" ;;
    -a|--all|--include-doc-sources) INCLUDE_DOC_SOURCES=true ;;
    -e|--ext) SEARCH_EXT="${2:?Provide extension for -e/--ext}"; shift ;;
    --all-ext) ALL_EXT=true ;;
    -c|--include-comments) ignore_comments=false ;;
    -h|--help) show_usage; exit 0 ;;
    --) shift
        while [[ $# -gt 0 ]]; do POSITIONAL+=("$1"); shift; done
        break
        ;;
    -*) echo "Unknown option: $1" >&2; exit 1 ;;
    *) POSITIONAL+=("$1") ;;
  esac
  shift
done

PATTERN="${POSITIONAL[0]:?Provide search pattern or regex. Use -h for help.}"
PREFIX="${POSITIONAL[1]:-.}"

clear
echo "$0 $(printf '%q ' "${ORIG_ARGS[@]}")" >&2
echo "→ pattern='$PATTERN' prefix='$PREFIX' flags='$GREP_FLAGS' ext='$SEARCH_EXT' all_ext='$ALL_EXT' comments='$([ "$ignore_comments" = "true" ] && echo ignored || echo included)' include_doc_sources='$INCLUDE_DOC_SOURCES' [help: -h]" >&2

#echo "→ pattern='$PATTERN' prefix='$PREFIX' flags='$GREP_FLAGS' ext='$SEARCH_EXT' all_ext='$ALL_EXT' ignore_comments='$ignore_comments' include_doc_sources='$INCLUDE_DOC_SOURCES' [help: -h]" >&2

EXCLUDE_PAT="\.i18n|/__pycache__/|/\.venv/|/venv/"
if [ "$INCLUDE_DOC_SOURCES" = "false" ]; then
  EXCLUDE_PAT="$EXCLUDE_PAT|doc_sources"
fi

EXCLUDE_FILE_PAT='[^/]*(backup|BACKUP|draft)'

get_matched_files() {
  local target_prefix="$1"
  (git ls-files "$target_prefix" && git ls-files --others --exclude-standard -- "$target_prefix") | \
    grep -Ev "$EXCLUDE_PAT" || true
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
if [ "$ALL_EXT" = "false" ] && [ -n "$TARGET_FILES" ]; then
  TARGET_FILES=$(printf '%s\n' "$TARGET_FILES" | grep -E "\.${SEARCH_EXT}$" || true)
fi

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
  | { grep $MATCH_FLAGS -E -- "$PATTERN" || true; } \
  | { head -n 201; } || true )
else
  matches=$( { do_search "$PATTERN" | head -n 201; } || true )
fi

count=$(echo -n "$matches" | grep -c '^' || true)

if [ "$count" -eq 0 ]; then
  echo "nothing found" >&2
  exit 0
fi

if [ "$count" -gt 29 ] && [[ "$GREP_FLAGS" != *"-w"* && "$PATTERN" != *"\\b"* ]]; then
  REFINED_PATTERN="\\b${PATTERN}\\b"

  refined_matches=$( { do_search "$REFINED_PATTERN" | head -n 201; } || true )
  refined_count=$(echo -n "$refined_matches" | grep -c '^' || true)

  echo "⚠️⚠️Results exceeded 29 lines. Automatically refining pattern with word boundaries: '$REFINED_PATTERN'..." >&2

  if [ "$refined_count" -gt 0 ]; then
    matches="$refined_matches"
    count="$refined_count"
  fi
fi

if [ "$count" -gt 29 ]; then
  echo "Results still exceed 29 lines. Truncating output to top 29 matches:" >&2
  echo "$matches" | head -n 29
else
  echo "count = $count"
  echo "$matches"
  if [ "$count" -eq 1 ]; then
    match_file=$(echo "$matches" | cut -d: -f1)
    echo "grep -n -C 5 \"$PATTERN\" '$match_file'"
  fi
fi
echo '___________________________________________'
