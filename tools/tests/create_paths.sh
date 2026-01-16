#!/bin/bash

# Basis-Ordner erstellen
BASE_DIR="Path_Test_Zone"
mkdir -p "$BASE_DIR"

echo "=========================================================="
echo " Erstelle 10 Pfade mit steigender Länge..."
echo "=========================================================="

# Ein Block für die Ordnernamen (ca. 40 Zeichen)
# Format: 100er Schritte mit Unterstrichen wie gewünscht
BLOCK_NAME="100_110_120_130_140_150_160_170_180_190_200"

# Wir bauen 10 Test-Szenarien
for i in {1..10}
do
    # Wir bauen den Pfad dynamisch auf.
    # Bei i=1 gibt es 1 Ebene, bei i=10 gibt es 10 Ebenen.
    CURRENT_PATH="$BASE_DIR/Test_Case_$i"

    # Verschachtelung erzeugen
    for (( j=1; j<=i; j++ ))
    do
        # Ordnername: Ebene_Nummer + der lange Block
        CURRENT_PATH="$CURRENT_PATH/Level_${j}__${BLOCK_NAME}"
    done

    # Den Zielordner erstellen, wo du dein Programm reinkopieren sollst
    FINAL_PATH="$CURRENT_PATH/App_Paste_Here"
    mkdir -p "$FINAL_PATH"

    # Versuchen, den Windows-Pfad zu ermitteln (für korrekte Längenanzeige in Git Bash)
    if command -v cygpath >/dev/null; then
        WIN_PATH=$(cygpath -w "$(realpath "$FINAL_PATH")")
    else
        WIN_PATH=$(realpath "$FINAL_PATH")
    fi

    LEN=${#WIN_PATH}

    # Ausgabe formatieren
    if [ $LEN -gt 250 ]; then
        STATUS="⚠️ KRITISCH (>250)"
    else
        STATUS="✅ OK"
    fi

    echo "Nr. $i | Länge: $LEN Zeichen | $STATUS"
    echo "   Pfad: .../App_Paste_Here"
    echo "----------------------------------------------------------"
done

echo ""
echo "FERTIG! Kopiere deinen 'SL5...'-Inhalt in die verschiedenen 'App_Paste_Here' Ordner."
echo "Der Ordner 'Path_Test_Zone' liegt hier: $(pwd)/$BASE_DIR"
