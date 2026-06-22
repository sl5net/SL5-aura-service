#!/bin/bash

if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
  tmp_dir='C:/tmp'
else
  tmp_dir='/tmp'
fi


SOURCE_DIR="/home/seeh/projects/py/STT/config/maps"


TARGET_DIR="/tmp/sl5_aura/zip_backup"
TARGET_DIR="/home/seeh/projects/py/zip_backup/"

PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

#PROJECT_ROOT="(realpath"(realpath"(tr -d '\r' < "$tmp_dir/sl5_aura/sl5net_aura_project_root")")"

TARGET_DIR="$(realpath "$PROJECT_ROOT/../zip_backup")"
# ----------------------

if [ ! -d "$SOURCE_DIR" ]; then
    echo "error:  '$SOURCE_DIR' SOURCE_DIR not existiert."
    exit 1
fi

mkdir -p "$TARGET_DIR"

SOURCE_DIR=$(realpath "$SOURCE_DIR")
TARGET_DIR=$(realpath "$TARGET_DIR")

echo "start copy..."
echo "s: $SOURCE_DIR"
echo "t: $TARGET_DIR"

cd "$SOURCE_DIR" || exit 1

# Erläuterung der Parameter:
# -type f: Nur Dateien finden (keine Ordner direkt)
# -iname "*.zip": Sucht nach .zip-Dateien (Groß-/Kleinschreibung wird ignoriert)
# --parents: Kopiert die Datei inklusive ihres relativen Pfads in das Zielverzeichnis
find . -type f -iname "*.zip" -exec cp --parents -v {} "$TARGET_DIR" \;

echo "finised"

