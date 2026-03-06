#!/usr/bin/env bash
# move_translations.sh  v1.3
#
# Verschiebt übersetzte Markdown-Dateien in .i18n Unterordner.
# Beispiel: README-de.md       → README.i18n/README-de.md
#           advanced-scripting-kolang.md → advanced-scripting.i18n/advanced-scripting-kolang.md
#
# Regel: BASENAME-IRGENDWAS.md ist eine Übersetzung wenn BASENAME.md
#        im selben Verzeichnis existiert. Es wird der LÄNGSTE mögliche
#        Basename gesucht (wichtig für Dateien wie advanced-scripting-de.md).
#
# Verwendung:
#   ./move_translations.sh [VERZEICHNIS]        # Dry-run (Standard)
#   ./move_translations.sh [VERZEICHNIS] --run  # Wirklich ausführen

VERSION="1.3"

set -euo pipefail

ROOT_DIR="${1:-.}"
DRY_RUN=true

for arg in "$@"; do
    [[ "$arg" == "--run" ]] && DRY_RUN=false
done

# ── Farben ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

COUNT_MOVED=0
COUNT_ALREADY=0

echo ""
echo -e "  ${BOLD}move_translations.sh  v${VERSION}${RESET}"
echo ""
if $DRY_RUN; then
    echo -e "${YELLOW}${BOLD}╔══════════════════════════════════════════════╗${RESET}"
    echo -e "${YELLOW}${BOLD}║         DRY-RUN  (keine Änderungen)          ║${RESET}"
    echo -e "${YELLOW}${BOLD}╚══════════════════════════════════════════════╝${RESET}"
    echo -e "${YELLOW}  → Mit --run wirklich ausführen${RESET}"
else
    echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════╗${RESET}"
    echo -e "${GREEN}${BOLD}║     LIVE-RUN  (Dateien werden verschoben)    ║${RESET}"
    echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════╝${RESET}"
fi
echo -e "  Wurzelverzeichnis: ${CYAN}$(realpath "$ROOT_DIR")${RESET}"
echo ""

# ── Hauptschleife ─────────────────────────────────────────────────────────────
while IFS= read -r filepath; do

    filedir="$(dirname "$filepath")"
    filename="$(basename "$filepath")"
    name_no_ext="${filename%.md}"

    # Muss einen Bindestrich enthalten
    [[ "$name_no_ext" != *-* ]] && continue

    # Suche den LÄNGSTEN Basename für den eine Basis-Datei existiert.
    # Beispiel: "advanced-scripting-kolang"
    #   → prüfe "advanced-scripting" → advanced-scripting.md existiert? ✓ → nehmen
    #   → (würde nicht weiter suchen)
    # Beispiel: "README-ptlang"
    #   → prüfe "README" → README.md existiert? ✓ → nehmen
    remainder="$name_no_ext"
    basename_part=""
    found_base=""

    while [[ "$remainder" == *-* ]]; do
        candidate="${remainder%-*}"   # alles bis zum LETZTEN Bindestrich
        base_file="${filedir}/${candidate}.md"
        if [[ -f "$base_file" ]]; then
            basename_part="$candidate"
            found_base="$base_file"
            break
        fi
        remainder="$candidate"
    done

    # Keine Basis-Datei gefunden → überspringen
    [[ -z "$basename_part" ]] && continue

    # Nicht die Basis-Datei selbst verschieben
    [[ "$filepath" -ef "$found_base" ]] && continue

    # Ziel-Pfad
    i18n_dir="${filedir}/${basename_part}.i18n"
    target="${i18n_dir}/${filename}"

    # Schon am Zielort?
    if [[ -f "$target" ]] && [[ "$filepath" -ef "$target" ]]; then
        ((COUNT_ALREADY++)) || true
        continue
    fi

    echo -e "  ${GREEN}✓${RESET} ${CYAN}${filepath#"$ROOT_DIR"/}${RESET}"
    echo -e "      → ${target#"$ROOT_DIR"/}"

    if ! $DRY_RUN; then
        mkdir -p "$i18n_dir"
        mv "$filepath" "$target"
    fi

    ((COUNT_MOVED++)) || true

done < <(
    # Ordner die mit '.' beginnen oder nicht mit Buchstabe beginnen → ignorieren
    find "$ROOT_DIR" -mindepth 1 \
        -type d \( -name ".*" -o -not -name "[a-zA-Z]*" \) -prune \
        -o -type f -name "*.md" -print
)

# ── Zusammenfassung ───────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
if $DRY_RUN; then
    echo -e "  ${YELLOW}Würde verschoben:${RESET}  ${BOLD}${COUNT_MOVED}${RESET} Datei(en)"
else
    echo -e "  ${GREEN}Verschoben:${RESET}        ${BOLD}${COUNT_MOVED}${RESET} Datei(en)"
fi
echo -e "  Bereits korrekt:   ${COUNT_ALREADY} Datei(en)"
echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""

if $DRY_RUN && [[ $COUNT_MOVED -gt 0 ]]; then
    echo -e "${YELLOW}  → Zum Ausführen:${RESET} $0 ${ROOT_DIR} --run"
    echo ""
fi
