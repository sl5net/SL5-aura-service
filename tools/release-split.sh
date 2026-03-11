#!/bin/bash
# =============================================================================
# release-split.sh — Teilt release-diff Output in Copy-Paste Häppchen
# Version: 1.0.0
# Workflow:
#   1. ./release-diff.sh > diff.txt
#   2. ./release-split.sh diff.txt
#   3. Häppchen 1-N einzeln in Claude kopieren, Zusammenfassungen sammeln
#   4. Alle Zusammenfassungen zusammen in Claude für finale Release Notes
# =============================================================================

CHUNK_SIZE=1000
INPUT_FILE="${1:-}"
OUTPUT_DIR="${2:-./release-chunks}"

usage() {
  cat <<EOF
Verwendung: $0 <diff-file> [output-dir]

  diff-file    Output von release-diff.sh
  output-dir   Zielordner für Häppchen. Standard: ./release-chunks

Beispiel:
  ./release-diff.sh > diff.txt
  ./release-split.sh diff.txt
  # Dann chunk_01.txt, chunk_02.txt ... einzeln in Claude kopieren
EOF
}

if [ -z "$INPUT_FILE" ] || [ "$INPUT_FILE" = "--help" ]; then
  usage; exit 0
fi

if [ ! -f "$INPUT_FILE" ]; then
  echo "FEHLER: Datei nicht gefunden: $INPUT_FILE" >&2; exit 1
fi

mkdir -p "$OUTPUT_DIR"

TOTAL_LINES=$(wc -l < "$INPUT_FILE")
NUM_CHUNKS=$(( (TOTAL_LINES + CHUNK_SIZE - 1) / CHUNK_SIZE ))

echo "Gesamt: $TOTAL_LINES Zeilen → $NUM_CHUNKS Häppchen à $CHUNK_SIZE Zeilen"
echo "Output: $OUTPUT_DIR/"
echo ""

# Prompt-Prefix für jedes Häppchen
CHUNK_PROMPT_PREFIX="Fasse die Änderungen in diesem Git-Diff Abschnitt kurz auf English zusammen.
Gruppiere nach: Neue Features, Bugfixes, Refactoring, Docs/Config.
Nur Stichpunkte, maximal 15 Punkte. Dies ist Abschnitt"

# Prompt für die finale Zusammenfassung — wird als letzte Datei gespeichert
FINAL_PROMPT="Erstelle aus diesen Teilzusammenfassungen professionelle Release Notes auf English:

- Kurzer Einleitungssatz was dieses Release bringt
- Abschnitte: ✨ Neue Features | 🐛 Bugfixes | ♻️ Refactoring | 📝 Docs & Config
- Duplikate zusammenfassen
- Unwichtiges weglassen (WIP, Tippfehler-Commits, reine Import-Umzüge)

=== HIER DIE GESAMMELTEN TEILZUSAMMENFASSUNGEN EINFÜGEN ==="

chunk_num=1
start_line=1

while [ $start_line -le $TOTAL_LINES ]; do
  end_line=$(( start_line + CHUNK_SIZE - 1 ))
  [ $end_line -gt $TOTAL_LINES ] && end_line=$TOTAL_LINES

  outfile=$(printf "%s/chunk_%02d_of_%02d.txt" "$OUTPUT_DIR" "$chunk_num" "$NUM_CHUNKS")

  {
    echo "$CHUNK_PROMPT_PREFIX $chunk_num von $NUM_CHUNKS:"
    echo ""
    sed -n "${start_line},${end_line}p" "$INPUT_FILE"
  } > "$outfile"

  echo "  ✓ $outfile  (Zeilen $start_line–$end_line)"

  start_line=$(( end_line + 1 ))
  chunk_num=$(( chunk_num + 1 ))
done

# Finale Anleitung als letzte Datei
final_file="$OUTPUT_DIR/chunk_FINAL_prompt.txt"
echo "$FINAL_PROMPT" > "$final_file"

echo ""
echo "=================================================="
echo "  ANLEITUNG:"
echo "=================================================="
echo ""
echo "  Schritt 1: Jede chunk_NN_of_${NUM_CHUNKS}.txt einzeln in Claude kopieren"
echo "             → Antwort (Zusammenfassung) irgendwo sammeln"
echo ""
echo "  Schritt 2: chunk_FINAL_prompt.txt öffnen"
echo "             → Alle Zusammenfassungen dort einfügen"
echo "             → In Claude kopieren → fertige Release Notes"
echo ""
echo "  Dateien in: $OUTPUT_DIR/"
ls "$OUTPUT_DIR/"
