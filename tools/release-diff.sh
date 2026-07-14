#!/bin/bash
# =============================================================================
# release-diff.sh — Code changes since the last release, LLM-optimized
# Version: 1.6.0
# Changelog:
#   1.6.0 - Name-only filter: specific file types show only the filename, not the diff
#            (md, txt, json, yaml, etc., generate a lot of noise in i18n projects)
#   1.5.0 - Fix: Exclusion via filename filter applied after the diff (pathspec was unreliable)
#   1.4.0 - Fix: Changed exclude pathspec from :! to :(exclude)
#   1.3.0 - Fixed subshell bug; deduplicated commits
#   1.2.0 - Filter flags: --keep-deleted, --keep-comments, --max-lines
#   1.0.0 - Initial version
# =============================================================================

echo '
Please wait for two messages:
1. The text of my last release (as a template for style and format)
2. The Git changes since the last release

Do not answer the following questions until you have received both:
1. Should a new release of sl5net Aura be created? (yes/no)
2. Which version number? (major/minor/patch according to SemVer)
3. Justification in 2-3 sentences

github sl5net/SL5-aura-service/releases/latest


IMPORTANT: Write the release text exclusively in English,
exactly like the template I sent you.

Always retain the following elements from the template:
- The slogan: _Ultra-Fast. Private. Self-Learning. Aura._
- Keep the support block (Star, Share, Donate) with Ko-fi and Stripe links unchanged
- Keep the "Full Changelog" link at the end (update version numbers only)

'

MAX_LINES_PER_FILE=40
SKIP_DELETED=true
SKIP_COMMENTS=true
NO_DIFF=false


# Dateien die komplett übersprungen werden
EXCLUDE_REGEX='\.(lock|min\.js|min\.css|map|pyc|pyo|snap|svg|png|jpg|jpeg|gif|ico|woff|woff2|ttf|eot|csv|tsv|xlsx|pb\.go|pb\.ts)$|^(dist|build|out|\.next|vendor|node_modules|__pycache__|migrations)/'
EXCLUDE_EXACT='package-lock.json|yarn.lock|pnpm-lock.yaml|go.sum|Pipfile.lock|poetry.lock|composer.lock'

# Dateien bei denen NUR der Dateiname gezeigt wird, kein Diff-Inhalt
# Gut für: .md in 20 Sprachen, config-files, translations etc.
NAME_ONLY_REGEX='\.(md|txt|rst|po|pot|json|yml|toml|ini|cfg|conf|xml|html|htm|bat|ps1)$'

find_last_release() {
  if [ -n "${FROM_REF:-}" ]; then echo "$FROM_REF"; return; fi
  git fetch --tags --quiet 2>/dev/null || true
  local t
  # Nach Commit-Datum sortieren, nicht nach Versionsnummer
  t=$(git tag --sort=-creatordate | grep -E '^v?[0-9]+\.[0-9]+' | head -1 || true)
  [ -n "$t" ] && echo "$t" && return
  git rev-list --max-parents=0 HEAD
}

is_excluded_file() {
  echo "$1" | grep -qE "$EXCLUDE_REGEX" && return 0
  echo "$1" | grep -qE "$EXCLUDE_EXACT"  && return 0
  return 1
}

is_name_only_file() {
  echo "$1" | grep -qE "$NAME_ONLY_REGEX"
}

usage() {
  cat <<EOF
Verwendung: $0 [OPTIONEN]

Optionen:
  --from <ref>        Start-Referenz. Standard: letzter Tag
  --to   <ref>        End-Referenz.   Standard: HEAD
  --max-lines <n>     Max. Zeilen pro Datei (0=unbegrenzt). Standard: $MAX_LINES_PER_FILE
  --keep-deleted      Gelöschte Zeilen (-) anzeigen
  --keep-comments     Kommentare und Imports nicht filtern
  --full-content      Alle Dateitypen mit vollem Diff (kein name-only)
  --help

Beispiele:
  $0
  $0 --from v1.3.0
  $0 --full-content --keep-deleted
  $0 > release-context.txt
EOF
}

FULL_CONTENT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)          FROM_REF="$2";           shift 2 ;;
    --to)            TO_REF="$2";             shift 2 ;;
    --max-lines)     MAX_LINES_PER_FILE="$2"; shift 2 ;;
    --keep-deleted)  SKIP_DELETED=false;      shift ;;
    --keep-comments) SKIP_COMMENTS=false;     shift ;;
    --full-content)  FULL_CONTENT=true;       shift ;;
    --no-diff)       NO_DIFF=true;            shift ;;
    --help|-h)       usage; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if ! git rev-parse --git-dir &>/dev/null; then
  echo "FEHLER: Kein Git-Repository gefunden." >&2; exit 1
fi

FROM_REF=$(find_last_release)
TO_REF="${TO_REF:-HEAD}"


# Auto no-diff bei vielen Commits
AUTO_NO_DIFF_THRESHOLD=20
if [ "$NO_DIFF" = false ]; then
  AUTO_COMMIT_COUNT=$(git log "${FROM_REF}..${TO_REF}" --no-merges --oneline | wc -l)
  if [ "$AUTO_COMMIT_COUNT" -gt "$AUTO_NO_DIFF_THRESHOLD" ]; then
    NO_DIFF=true
    echo "# INFO: $AUTO_COMMIT_COUNT Commits gefunden → --no-diff automatisch aktiviert" >&2
  fi
fi









# === RELEASE-EMPFEHLUNG ======================================================
echo "=== RELEASE-EMPFEHLUNG ==="

COMMIT_COUNT=$(git log "${FROM_REF}..${TO_REF}" --no-merges --pretty="%s" | wc -l)
CHANGED_FILES=$(git diff "${FROM_REF}..${TO_REF}" --name-only | grep -vE "$EXCLUDE_REGEX" | grep -vE "$EXCLUDE_EXACT" | wc -l)
LAST_RELEASE_DAYS=$(( ( $(date +%s) - $(git log -1 --format=%ct "${FROM_REF}") ) / 86400 ))

RECOMMEND="JA"
REASON=""
SEMVER="patch"

# Zu wenig passiert
if [ "$COMMIT_COUNT" -lt 2 ]; then
  RECOMMEND="NEIN"
  REASON="Nur $COMMIT_COUNT Commit(s) seit letztem Release."
elif [ "$CHANGED_FILES" -lt 3 ]; then
  RECOMMEND="NEIN"
  REASON="Nur $CHANGED_FILES relevante Datei(en) geändert."
elif [ "$LAST_RELEASE_DAYS" -lt 1 ]; then
  RECOMMEND="NEIN"
  REASON="Letztes Release war heute."
fi

# SemVer aus Conventional Commits
if git log "${FROM_REF}..${TO_REF}" --no-merges --pretty="%s" | grep -qiE "BREAKING|BREAKING CHANGE"; then
  SEMVER="MAJOR"
elif git log "${FROM_REF}..${TO_REF}" --no-merges --pretty="%s" | grep -qiE "^feat"; then
  SEMVER="minor"
fi

# Nur Docs/Config?
CODE_FILES=$(git diff "${FROM_REF}..${TO_REF}" --name-only \
  | grep -vE "$EXCLUDE_REGEX" \
  | grep -vE "$EXCLUDE_EXACT" \
  | grep -vE "$NAME_ONLY_REGEX" \
  | wc -l)
if [ "$CODE_FILES" -eq 0 ] && [ "$RECOMMEND" = "JA" ]; then
  SEMVER="patch"
  REASON="Nur Docs/Config geändert, kein echter Code."
fi

echo "  Commits since release : $COMMIT_COUNT"
echo "  Changed files         : $CHANGED_FILES (of which code: $CODE_FILES)"
echo "  Days since release    : $LAST_RELEASE_DAYS"
echo ""
echo "  Recommendation        : $RECOMMEND"

[ -n "$REASON" ] && echo "  Grund       : $REASON"


if [ "$RECOMMEND" = "JA" ]; then
  echo "  SemVer-Typ  : $SEMVER"
  echo ""
echo "--- LLM PROMPT ---"
echo "1. Should a new release be created? (yes/no)"
echo "2. Which version number? (major/minor/patch according to SemVer)"
echo "3. Reason in 2-3 sentences"
  echo "------------------"
fi


# === HEADER ==================================================================
echo "RELEASE DIFF REPORT"
echo "FROM: $FROM_REF  ->  TO: $TO_REF"
echo "DATE: $(date '+%Y-%m-%d %H:%M')"
echo ""

# === COMMITS (dedupliziert) ==================================================
echo "=== COMMITS ==="
git log "${FROM_REF}..${TO_REF}" \
  --pretty=format:"%s" \
  --no-merges \
  | sort | uniq -c | sort -rn \
  | awk '{count=$1; $1=""; msg=substr($0,2); printf "  [x%d] %s\n", count, msg}'
echo ""
echo ""

# === FILE STATISTICS =========================================================
echo "=== CHANGED FILES ==="

git diff "${FROM_REF}..${TO_REF}" --name-only | while IFS= read -r f; do
  is_excluded_file "$f" && continue
  if ! $FULL_CONTENT && is_name_only_file "$f"; then
    echo "  [name-only] $f"
  else
    echo "  $f"
  fi
done
echo ""

# === CODE-DIFF ===============================================================
if $NO_DIFF; then
  exit 0
fi

TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT

git diff -U0 --no-color "${FROM_REF}..${TO_REF}" > "$TMPFILE"

file_line_count=0
file_truncated=false
skip_current_file=false
name_only_current=false
current_file=""

while IFS= read -r line; do

  # Neue Datei erkennen
  if [[ "$line" =~ ^\+\+\+\ b/(.+) ]]; then
    $file_truncated && echo "    ... (gekuerzt nach ${MAX_LINES_PER_FILE} Zeilen)"
    current_file="${BASH_REMATCH[1]}"
    file_line_count=0
    file_truncated=false
    name_only_current=false

    if is_excluded_file "$current_file"; then
      skip_current_file=true
    else
      skip_current_file=false
      echo ""
      if ! $FULL_CONTENT && is_name_only_file "$current_file"; then
        name_only_current=true
        echo "FILE: $current_file  [nur Name, kein Diff]"
      else
        echo "FILE: $current_file"
      fi
    fi
    continue
  fi

  # Overhead & name-only Dateien überspringen
  [[ "$line" =~ ^(diff\ --git|index\ |---\ ) ]] && continue
  $skip_current_file && continue
  $name_only_current && continue

  # Positions-Marker / Funktionsname
  if [[ "$line" =~ ^@@ ]]; then
    funcname=$(echo "$line" | awk -F'@@' '{print $3}' | xargs)
    [ -n "$funcname" ] && echo "  In $funcname:"
    continue
  fi

  # Zeilenlimit
  if [ "$MAX_LINES_PER_FILE" -gt 0 ] && [ "$file_line_count" -ge "$MAX_LINES_PER_FILE" ]; then
    file_truncated=true
    continue
  fi

  # Hinzugefügte Zeilen
  if [[ "$line" =~ ^\+[^+] ]]; then
    content="${line:1}"
    [ -z "${content// }" ] && continue
    if $SKIP_COMMENTS; then
      [[ "$content" =~ ^[[:space:]]*(#|//|/\*|\*|--) ]] && continue
      [[ "$content" =~ ^[[:space:]]*(import |from |require\(|include |use |using ) ]] && continue
    fi
    echo "    + $content"
    ((file_line_count++)) || true

  # Gelöschte Zeilen
  elif [[ "$line" =~ ^-[^-] ]]; then
    $SKIP_DELETED && continue
    content="${line:1}"
    [ -z "${content// }" ] && continue
    if $SKIP_COMMENTS; then
      [[ "$content" =~ ^[[:space:]]*(#|//|/\*|\*|--) ]] && continue
      [[ "$content" =~ ^[[:space:]]*(import |from |require\(|include |use |using ) ]] && continue
    fi
    echo "    - $content"
    ((file_line_count++)) || true
  fi

done < "$TMPFILE"

$file_truncated && echo "    ... (gekuerzt nach ${MAX_LINES_PER_FILE} Zeilen)"
echo ""
echo "=== ENDE ==="
