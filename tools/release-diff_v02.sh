#!/bin/bash
# =============================================================================
# release-diff.sh — Zeigt alle Code-Änderungen seit dem letzten Release
# Optimiert für LLM-Konsum: echter Diff-Inhalt, kein Kontext-Rauschen
# =============================================================================

# --- Letzten Tag/Release finden ----------------------------------------------
find_last_release() {
  if [ -n "${FROM_REF:-}" ]; then echo "$FROM_REF"; return; fi

  local last_tag
  last_tag=$(git tag --sort=-version:refname | grep -E '^v?[0-9]+\.[0-9]+' | head -1 || true)
  if [ -n "$last_tag" ]; then echo "$last_tag"; return; fi

  last_tag=$(git describe --tags --abbrev=0 2>/dev/null || true)
  if [ -n "$last_tag" ]; then echo "$last_tag"; return; fi

  git rev-list --max-parents=0 HEAD
}

usage() {
  cat <<EOF
Verwendung: $0 [OPTIONEN]

Optionen:
  --from <ref>   Start-Referenz (Tag, Commit, Branch). Standard: letzter Tag
  --to   <ref>   End-Referenz. Standard: HEAD
  --help         Diese Hilfe

Beispiele:
  $0
  $0 --from v1.3.0
  $0 --from v1.3.0 --to v1.4.0
  $0 > release-context.txt      # In Datei für LLM-Prompt speichern
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)  FROM_REF="$2"; shift 2 ;;
    --to)    TO_REF="$2";   shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

# --- Git-Repo prüfen ---------------------------------------------------------
if ! git rev-parse --git-dir &>/dev/null; then
  echo "FEHLER: Kein Git-Repository gefunden." >&2
  exit 1
fi

FROM_REF=$(find_last_release)
TO_REF="${TO_REF:-HEAD}"

# === HEADER ==================================================================
echo "RELEASE DIFF REPORT"
echo "FROM: $FROM_REF"
echo "TO:   $TO_REF"
echo "DATE: $(date '+%Y-%m-%d %H:%M')"
echo ""

# === COMMIT-ÜBERSICHT ========================================================
echo "=== COMMITS ==="
git log "${FROM_REF}..${TO_REF}" \
  --pretty=format:"[%h] %s (%an, %ar)" \
  --no-merges
echo ""
echo ""

# === DATEI-STATISTIK =========================================================
echo "=== GEÄNDERTE DATEIEN ==="
git diff "${FROM_REF}..${TO_REF}" --stat --no-color
echo ""

# === ECHTER CODE-DIFF (wie das Original-Script, nur zwischen zwei Refs) ======
echo "=== CODE ÄNDERUNGEN ==="

git diff -U0 --no-color "${FROM_REF}..${TO_REF}" | while IFS= read -r line; do

  # Dateiname
  if [[ "$line" =~ ^\+\+\+\ b/(.+) ]]; then
    echo ""
    echo "FILE: ${BASH_REMATCH[1]}"

  # Positions-Marker: Funktionsname extrahieren falls vorhanden
  elif [[ "$line" =~ ^@@ ]]; then
    funcname=$(echo "$line" | awk -F'@@' '{print $3}' | xargs)
    if [ -n "$funcname" ]; then
      echo "  In $funcname:"
    fi

  # Hinzugefügte Zeilen
  elif [[ "$line" =~ ^\+[^+] ]]; then
    content="${line:1}"
    [ -n "${content// }" ] && echo "    + $content"

  # Gelöschte Zeilen
  elif [[ "$line" =~ ^-[^-] ]]; then
    content="${line:1}"
    [ -n "${content// }" ] && echo "    - $content"
  fi

done

echo ""
echo "=== ENDE ==="
