#!/bin/bash
set -e

# --- Bidirectional sync ---

SRC1="$HOME/.config/autokey/data/stt/autokey-scripts/"
SRC2="scripts/autokey-scripts/"

# Sync newer files from SRC1 to SRC2 
rsync -au --delete "$SRC1" "$SRC2"

# Sync newer files from SRC2  to SRC1
rsync -au --delete "$SRC2" "$SRC1"

# --- Existing pipreqs logic ---

# Check if pipreqs is available in the venv
if [ ! -x ".venv/bin/pipreqs" ]; then
    echo "pipreqs is not installed in .venv. Please run '.venv/bin/pip install pipreqs' inside your virtual environment."
    exit 1
fi

# Temporary directory for requirements generation
TMPDIR=".pipreqs_temp"
FILES=("aura_engine.py" "get_suggestions.py")

# Clean up any old temp dirs
rm -rf "$TMPDIR"
mkdir "$TMPDIR"

# Copy only the relevant files
for f in "${FILES[@]}"; do
    cp "$f" "$TMPDIR/"
done

# Generate scripts/infra/requirements/requirements.txt from only those files using pipreqs from the venv
.venv/bin/pipreqs "$TMPDIR" --force

# Replace the actual scripts/infra/requirements/requirements.txt
mv "$TMPDIR/requirements.txt" scripts/infra/requirements/requirements.txt

# Convert package names to lowercase
awk -F'==' '{print tolower($1) "==" $2}' scripts/infra/requirements/requirements.txt > scripts/infra/requirements/requirements.txt.tmp && mv scripts/infra/requirements/requirements.txt.tmp scripts/infra/requirements/requirements.txt

# Clean up temp directory
rm -rf "$TMPDIR"
