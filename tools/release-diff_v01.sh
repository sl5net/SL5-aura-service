#!/bin/bash
# =============================================================================
# release-diff.sh — Zeigt alle Änderungen seit dem letzten Release/Tag
# Optimiert für LLM-Konsum (kompakt, strukturiert, kein Rauschen)
# =============================================================================

set -euo pipefail

# --- Konfiguration -----------------------------------------------------------
MAX_LINES_PER_FILE=80   # Kürzt sehr große Diffs pro Datei
CONTEXT_LINES=0         # Kontextzeilen um Änderungen (0 = nur Änderungen)

# --- Farben (werden deaktiviert wenn kein Terminal) --------------------------
if [ -t 1 ]; then
  BOLD="\033[1m"; CYAN="\033[36m"; GREEN="\033[32m"
  RED="\033[31m"; YELLOW="\033[33m"; RESET="\033[0m"
else
  BOLD=""; CYAN=""; GREEN=""; RED=""; YELLOW=""; RESET=""
fi

# --- Letzten Tag/Release finden ----------------------------------------------
find_last_release() {
  # 1. Explizit übergebener Startpunkt
  if [ -n "${FROM_REF:-}" ]; then
    echo "$FROM_REF"
    return
  fi
  # 2. Letzter semantischer Tag (v1.2.3 oder 1.2.3)
  local last_tag
  last_tag=$(git tag --sort=-version:refname | grep -E '^v?[0-9]+\.[0-9]+' | head -1 || true)
  if [ -n "$last_tag" ]; then
    echo "$last_tag"
    return
  fi
  # 3. Letzter beliebiger Tag
  last_tag=$(git describe --tags --abbrev=0 2>/dev/null || true)
  if [ -n "$last_tag" ]; then
    echo "$last_tag"
    return
  fi
  # 4. Fallback: erster Commit
  git rev-list --max-parents=0 HEAD
}

# --- Hauptprogramm -----------------------------------------------------------
main() {
  # Git-Repo prüfen
  if ! git rev-parse --git-dir &>/dev/null; then
    echo "FEHLER: Kein Git-Repository gefunden." >&2
    exit 1
  fi

  local from_ref to_ref
  from_ref=$(find_last_release)
  to_ref="${TO_REF:-HEAD}"

  # === HEADER ================================================================
  echo ""
  echo -e "${BOLD}${CYAN}╔══════════════════════════════════════════════════════╗${RESET}"
  echo -e "${BOLD}${CYAN}║         RELEASE DIFF — LLM CONTEXT REPORT           ║${RESET}"
  echo -e "${BOLD}${CYAN}╚══════════════════════════════════════════════════════╝${RESET}"
  echo ""
  echo -e "${BOLD}FROM:${RESET} $from_ref"
  echo -e "${BOLD}TO:  ${RESET} $to_ref"
  echo -e "${BOLD}DATE:${RESET} $(date '+%Y-%m-%d %H:%M')"
  echo -e "${BOLD}REPO:${RESET} $(git remote get-url origin 2>/dev/null || echo '(lokal)')"
  echo ""

  # === COMMIT-ÜBERSICHT ======================================================
  echo -e "${BOLD}${YELLOW}━━━ COMMITS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  git log "${from_ref}..${to_ref}" \
    --pretty=format:"  [%h] %s  (%an, %ar)" \
    --no-merges
  echo ""
  echo ""

  # === DATEI-STATISTIK =======================================================
  echo -e "${BOLD}${YELLOW}━━━ GEÄNDERTE DATEIEN (Übersicht) ━━━━━━━━━━━━━━━━━━━━${RESET}"
  git diff "${from_ref}..${to_ref}" --stat --no-color | head -50
  echo ""

  # === STRUKTURIERTER DIFF ===================================================
  echo -e "${BOLD}${YELLOW}━━━ ÄNDERUNGEN IM DETAIL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

  # Alle geänderten Dateien ermitteln
  local changed_files
  changed_files=$(git diff "${from_ref}..${to_ref}" --name-only)

  if [ -z "$changed_files" ]; then
    echo "  (keine Änderungen)"
    echo ""
    exit 0
  fi

  # Pro Datei den kompakten Diff ausgeben
  while IFS= read -r filepath; do
    [ -z "$filepath" ] && continue

    echo ""
    echo -e "${BOLD}${CYAN}FILE: $filepath${RESET}"
    echo -e "${CYAN}$(printf '─%.0s' {1..60})${RESET}"

    # Status der Datei (added/deleted/modified/renamed)
    local status
    status=$(git diff "${from_ref}..${to_ref}" --name-status | grep -E $'[ \t]'"${filepath}"'$' | cut -f1 || true)
    case "${status:0:1}" in
      A) echo -e "  ${GREEN}[NEU]${RESET}" ;;
      D) echo -e "  ${RED}[GELÖSCHT]${RESET}" ;;
      R) echo -e "  ${YELLOW}[UMBENANNT]${RESET}" ;;
      M) echo -e "  [GEÄNDERT]" ;;
    esac

    # Diff der Datei, ohne Kontextzeilen
    local diff_output line_count
    diff_output=$(git diff "-U${CONTEXT_LINES}" --no-color \
      "${from_ref}..${to_ref}" -- "$filepath" 2>/dev/null || true)

    if [ -z "$diff_output" ]; then
      echo "  (kein Diff verfügbar)"
      continue
    fi

    line_count=0
    local truncated=false

    while IFS= read -r line; do
      # Header-Zeilen überspringen (--- / +++ / diff --git / index)
      [[ "$line" =~ ^(diff\ --git|index\ |---\ |\\+\\+\\+\ ) ]] && continue

      # Positions-Marker (@@ ... @@)
      if [[ "$line" =~ ^@@ ]]; then
        local ctx
        ctx=$(echo "$line" | sed 's/@@ [^@]* @@/@@/')
        # Funktionsname extrahieren falls vorhanden
        local funcname
        funcname=$(echo "$line" | awk -F'@@' '{print $3}' | xargs)
        if [ -n "$funcname" ]; then
          echo -e "  ${YELLOW}▸ ${funcname}${RESET}"
        fi
        continue
      fi

      # Zeilenlimit prüfen
      if [ "$line_count" -ge "$MAX_LINES_PER_FILE" ]; then
        truncated=true
        break
      fi

      # Hinzugefügte Zeilen
      if [[ "$line" =~ ^\+ ]]; then
        content="${line:1}"
        [ -z "${content// }" ] && continue   # leere Zeilen überspringen
        echo -e "  ${GREEN}+${RESET} ${content}"
        ((line_count++)) || true

      # Gelöschte Zeilen
      elif [[ "$line" =~ ^- ]]; then
        content="${line:1}"
        [ -z "${content// }" ] && continue
        echo -e "  ${RED}-${RESET} ${content}"
        ((line_count++)) || true
      fi

    done <<< "$diff_output"

    if $truncated; then
      local total
      total=$(echo "$diff_output" | grep -c '^[+-]' || true)
      echo -e "  ${YELLOW}… (${total} Zeilen gesamt, nach ${MAX_LINES_PER_FILE} abgeschnitten)${RESET}"
    fi

  done <<< "$changed_files"

  # === ZUSAMMENFASSUNG =======================================================
  echo ""
  echo -e "${BOLD}${YELLOW}━━━ ZUSAMMENFASSUNG ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

  local num_commits num_files insertions deletions
  num_commits=$(git rev-list --count "${from_ref}..${to_ref}" --no-merges)
  num_files=$(echo "$changed_files" | wc -l | xargs)

  local stat_line
  stat_line=$(git diff "${from_ref}..${to_ref}" --shortstat --no-color)
  insertions=$(echo "$stat_line" | grep -oE '[0-9]+ insertion' | grep -oE '[0-9]+' || echo 0)
  deletions=$(echo "$stat_line"  | grep -oE '[0-9]+ deletion'  | grep -oE '[0-9]+' || echo 0)

  echo "  Commits     : $num_commits"
  echo "  Dateien     : $num_files"
  echo -e "  Hinzugefügt : ${GREEN}+${insertions}${RESET}"
  echo -e "  Entfernt    : ${RED}-${deletions}${RESET}"
  echo ""
  echo -e "${BOLD}${CYAN}══ Ende des Reports ══════════════════════════════════${RESET}"
  echo ""
}

# --- CLI-Hilfe ---------------------------------------------------------------
usage() {
  cat <<EOF
Verwendung: $0 [OPTIONEN]

Optionen:
  --from <ref>    Start-Referenz (Tag, Commit, Branch). Standard: letzter Tag
  --to   <ref>    End-Referenz. Standard: HEAD
  --lines <n>     Max. Zeilen pro Datei. Standard: $MAX_LINES_PER_FILE
  --context <n>   Kontextzeilen. Standard: $CONTEXT_LINES
  --help          Diese Hilfe

Umgebungsvariablen:
  FROM_REF, TO_REF  (alternativ zu --from / --to)

Beispiele:
  $0
  $0 --from v1.3.0
  $0 --from v1.3.0 --to v1.4.0
  $0 --from main --to feature/my-branch
  $0 2>&1 | tee release-context.txt    # In Datei speichern
  $0 2>&1 | pbcopy                     # In Clipboard (macOS)
EOF
}

# --- Argumente parsen --------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)   FROM_REF="$2";         shift 2 ;;
    --to)     TO_REF="$2";           shift 2 ;;
    --lines)  MAX_LINES_PER_FILE="$2"; shift 2 ;;
    --context) CONTEXT_LINES="$2";   shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) echo "Unbekannte Option: $1" >&2; usage >&2; exit 1 ;;
  esac
done

main
