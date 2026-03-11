#!/bin/bash
# =============================================================================
# release-diff.sh — Code-Änderungen seit letztem Release, LLM-optimiert
# Defaults: maximale Reduktion für minimalen Kontext
# =============================================================================

# --- Defaults (aggressiv gekürzt) --------------------------------------------
MAX_LINES_PER_FILE=40    # Pro Datei max. N Zeilen (0 = unbegrenzt)
SKIP_DELETED=true        # Gelöschte Zeilen (-) weglassen
SKIP_COMMENTS=true       # Kommentare & Import-Zeilen filtern

EXCLUDE_PATTERNS=(
  "*.lock" "package-lock.json" "yarn.lock" "pnpm-lock.yaml"
  "*.min.js" "*.min.css" "*.map"
  "dist/*" "build/*" "out/*" ".next/*"
  "*.generated.*" "*.pb.go" "*.pb.ts"
  "__pycache__/*" "*.pyc" "*.pyo"
  "*.svg" "*.png" "*.jpg" "*.jpeg" "*.gif" "*.ico" "*.woff*" "*.ttf"
  "*.csv" "*.tsv" "*.xlsx"
  "go.sum" "Pipfile.lock" "poetry.lock" "composer.lock"
  "*.snap"                  # Jest Snapshots
  "migrations/*"            # DB-Migrationen (oft sehr lang, wenig Signal)
  "vendor/*" "node_modules/*"
)

# --- Letzten Tag finden ------------------------------------------------------
find_last_release() {
  if [ -n "${FROM_REF:-}" ]; then echo "$FROM_REF"; return; fi
  local t
  t=$(git tag --sort=-version:refname | grep -E '^v?[0-9]+\.[0-9]+' | head -1 || true)
  [ -n "$t" ] && echo "$t" && return
  t=$(git describe --tags --abbrev=0 2>/dev/null || true)
  [ -n "$t" ] && echo "$t" && return
  git rev-list --max-parents=0 HEAD
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
  --help

Beispiele:
  $0                              # maximale Reduktion
  $0 --from v1.3.0
  $0 --keep-deleted --max-lines 0 # alles anzeigen
  $0 > release-context.txt        # für LLM-Prompt speichern
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)          FROM_REF="$2";           shift 2 ;;
    --to)            TO_REF="$2";             shift 2 ;;
    --max-lines)     MAX_LINES_PER_FILE="$2"; shift 2 ;;
    --keep-deleted)  SKIP_DELETED=false;      shift ;;
    --keep-comments) SKIP_COMMENTS=false;     shift ;;
    --help|-h)       usage; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

if ! git rev-parse --git-dir &>/dev/null; then
  echo "FEHLER: Kein Git-Repository gefunden." >&2; exit 1
fi

FROM_REF=$(find_last_release)
TO_REF="${TO_REF:-HEAD}"

# Exclude-Args für git diff
EXCLUDE_ARGS=()
for pat in "${EXCLUDE_PATTERNS[@]}"; do
  EXCLUDE_ARGS+=(":!${pat}")
done

# Ist eine Zeile reines Rauschen (Kommentar / Import)?
is_noise_line() {
  local c="$1"
  [[ "$c" =~ ^[[:space:]]*(#|//|/\*|\*|--) ]] && return 0
  [[ "$c" =~ ^[[:space:]]*(import |from |require\(|include |use |using ) ]] && return 0
  return 1
}

# === HEADER ==================================================================
echo "RELEASE DIFF REPORT"
echo "FROM: $FROM_REF  →  TO: $TO_REF"
echo "DATE: $(date '+%Y-%m-%d %H:%M')"
echo ""

# === COMMITS =================================================================
echo "=== COMMITS ==="
git log "${FROM_REF}..${TO_REF}" \
  --pretty=format:"[%h] %s (%an, %ar)" \
  --no-merges
echo ""
echo ""

# === DATEI-STATISTIK =========================================================
echo "=== GEÄNDERTE DATEIEN ==="
git diff "${FROM_REF}..${TO_REF}" --stat --no-color -- . "${EXCLUDE_ARGS[@]}"
echo ""

# === CODE-DIFF ===============================================================
echo "=== CODE ÄNDERUNGEN ==="

file_line_count=0
file_truncated=false

git diff -U0 --no-color "${FROM_REF}..${TO_REF}" -- . "${EXCLUDE_ARGS[@]}" \
| while IFS= read -r line; do

  # Neue Datei
  if [[ "$line" =~ ^\+\+\+\ b/(.+) ]]; then
    $file_truncated && echo "    ... (gekürzt nach ${MAX_LINES_PER_FILE} Zeilen)"
    echo ""
    echo "FILE: ${BASH_REMATCH[1]}"
    file_line_count=0
    file_truncated=false
    continue
  fi

  # Overhead-Zeilen überspringen
  [[ "$line" =~ ^(diff\ --git|index\ |---\ ) ]] && continue

  # Positions-Marker / Funktionsname
  if [[ "$line" =~ ^@@ ]]; then
    funcname=$(echo "$line" | awk -F'@@' '{print $3}' | xargs)
    [ -n "$funcname" ] && echo "  In $funcname:"
    continue
  fi

  # Zeilenlimit erreicht?
  if [ "$MAX_LINES_PER_FILE" -gt 0 ] && [ "$file_line_count" -ge "$MAX_LINES_PER_FILE" ]; then
    file_truncated=true
    continue
  fi

  # Hinzugefügte Zeilen
  if [[ "$line" =~ ^\+[^+] ]]; then
    content="${line:1}"
    [ -z "${content// }" ] && continue
    $SKIP_COMMENTS && is_noise_line "$content" && continue
    echo "    + $content"
    ((file_line_count++)) || true

  # Gelöschte Zeilen
  elif [[ "$line" =~ ^-[^-] ]]; then
    $SKIP_DELETED && continue
    content="${line:1}"
    [ -z "${content// }" ] && continue
    $SKIP_COMMENTS && is_noise_line "$content" && continue
    echo "    - $content"
    ((file_line_count++)) || true
  fi

done

echo ""
echo "=== ENDE ==="
