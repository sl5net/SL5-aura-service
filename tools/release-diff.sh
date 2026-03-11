#!/bin/bash
# =============================================================================
# release-diff.sh — Code-Änderungen seit letztem Release, LLM-optimiert
# Version: 1.6.0
# Changelog:
#   1.6.0 - Name-only Filter: bestimmte Dateitypen zeigen nur Dateiname, kein Diff
#            (md, txt, json, yaml etc. erzeugen viel Rauschen bei i18n-Projekten)
#   1.5.0 - Fix: Exclude via Dateiname-Filter nach dem Diff (pathspec war unzuverlässig)
#   1.4.0 - Fix: Exclude-Pathspec von :! zu :(exclude) geändert
#   1.3.0 - Subshell-Bug gefixt; Commits dedupliziert
#   1.2.0 - Filter-Flags: --keep-deleted, --keep-comments, --max-lines
#   1.0.0 - Initiale Version
# =============================================================================

MAX_LINES_PER_FILE=40
SKIP_DELETED=true
SKIP_COMMENTS=true

# Dateien die komplett übersprungen werden
EXCLUDE_REGEX='\.(lock|min\.js|min\.css|map|pyc|pyo|snap|svg|png|jpg|jpeg|gif|ico|woff|woff2|ttf|eot|csv|tsv|xlsx|pb\.go|pb\.ts)$|^(dist|build|out|\.next|vendor|node_modules|__pycache__|migrations)/'
EXCLUDE_EXACT='package-lock.json|yarn.lock|pnpm-lock.yaml|go.sum|Pipfile.lock|poetry.lock|composer.lock'

# Dateien bei denen NUR der Dateiname gezeigt wird, kein Diff-Inhalt
# Gut für: .md in 20 Sprachen, config-files, translations etc.
NAME_ONLY_REGEX='\.(md|txt|rst|po|pot|json|yaml|yml|toml|ini|cfg|conf|xml|html|htm|bat|ps1|sh)$'

find_last_release() {
  if [ -n "${FROM_REF:-}" ]; then echo "$FROM_REF"; return; fi
  local t
  t=$(git tag --sort=-version:refname | grep -E '^v?[0-9]+\.[0-9]+' | head -1 || true)
  [ -n "$t" ] && echo "$t" && return
  t=$(git describe --tags --abbrev=0 2>/dev/null || true)
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
    --help|-h)       usage; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if ! git rev-parse --git-dir &>/dev/null; then
  echo "FEHLER: Kein Git-Repository gefunden." >&2; exit 1
fi

FROM_REF=$(find_last_release)
TO_REF="${TO_REF:-HEAD}"

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

# === DATEI-STATISTIK =========================================================
echo "=== GEÄNDERTE DATEIEN ==="
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
echo "=== CODE ÄNDERUNGEN ==="

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
