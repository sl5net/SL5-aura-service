#!/bin/bash
# setup/suse_setup.sh
# Run this setup script from the project's root directory.

SCRIPT_NAME=$(basename "$0")
# Check if the script is run from the project root.
# This check is more robust than changing directory.
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: Please run this script from the project's root directory."
    echo ""
    echo "cd .. ; ./setup/$SCRIPT_NAME"
    exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
#cd "$PROJECT_ROOT"

should_remove_zips_after_unpack=true


echo "--- Starting STT Setup for openSUSE ---"
# --- End of location-independent block ---

set -e

# --- 1. System Dependencies ---
# (This section remains unchanged)
echo "--> Checking for a compatible Java version (>=17)..."
JAVA_OK=0
if command -v java &> /dev/null; then
    VERSION=$(java -version 2>&1 | awk -F[\".] '/version/ {print ($2 == "1") ? $3 : $2}')
    if [ "$VERSION" -ge 17 ]; then
        echo "    -> Found compatible Java version $VERSION. OK."
        JAVA_OK=1
    else
        echo "    -> Found Java version $VERSION, but we need >=17."
    fi
else
    echo "    -> No Java executable found."
fi




if [ "$JAVA_OK" -eq 0 ]; then
    echo "    -> Installing a modern JDK (>=17)..."
    # SUSE CHANGE: Use zypper instead of apt
    sudo zypper refresh && sudo zypper -n install java-21-openjdk
fi
echo "--> Installing other core dependencies..."
# SUSE CHANGE: Use zypper and adjust package names
sudo zypper -n install \
    inotify-tools wget unzip portaudio-devel python3-pip


# --- 2. Python Virtual Environment ---
# (This section remains unchanged)
if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    python3 -m venv .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# --- 3. Python Requirements ---
# (This section remains unchanged)
echo "--> Installing Python requirements into the virtual environment..."
./.venv/bin/pip install -r requirements.txt

# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files..."
# THIS IS THE KEY CHANGE. We call the Python script and pass the current
# working directory (which is the project root) as an argument.
# This one command replaces all old 'mkdir' and 'touch' commands for the project structure.
python3 "scripts/py/func/create_required_folders.py" "$(pwd)"




# ==============================================================================
# --- 5. Download and Extract Required Components ---
# This block intelligently handles downloads and extractions.
# ==============================================================================

echo "--> Checking for required components (LanguageTool, Vosk-Models)..."

# --- Configuration ---
PREFIX="Z_"
# Format: "BaseName FinalDirName DestinationPath"
ARCHIVE_CONFIG=(
    "LanguageTool-6.6 LanguageTool-6.6 ."
    "vosk-model-en-us-0.22 vosk-model-en-us-0.22 ./models"
    "vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15 ./models"
    "vosk-model-de-0.21 vosk-model-de-0.21 ./models"
    "lid.176 lid.176.bin ./models"
)
DOWNLOAD_REQUIRED=false

# --- Phase 1: Check and attempt to restore from local ZIP cache ---
echo "    -> Phase 1: Checking and trying to restore from local cache..."
for config_line in "${ARCHIVE_CONFIG[@]}"; do
    read -r base_name final_name dest_path <<< "$config_line"
    target_path="$dest_path/$final_name"
    zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

    # If the component already exists, we're good for this one.
    if [ -e "$target_path" ]; then
        continue
    fi

    # The component is missing. Let's see if we can unzip it from a local cache.
    echo "    -> Missing: '$target_path'. Searching for '$zip_file'..."
    if [ -f "$zip_file" ]; then
        echo "    -> Found ZIP cache. Extracting '$zip_file'..."
        unzip -q "$zip_file" -d "$dest_path"
    else
        # The ZIP is not there. We MUST run the downloader.
        echo "    -> ZIP cache not found. A download is required."
        DOWNLOAD_REQUIRED=true
    fi
done

# --- Phase 2: Download if necessary ---
if [ "$DOWNLOAD_REQUIRED" = true ]; then
    echo "    -> Phase 2: Running Python downloader for missing components..."

    # Create the models directory before attempting to download files into it.
    mkdir -p ./models

    ./.venv/bin/python tools/download_all_packages.py
    echo "    -> Downloader finished. Retrying extraction..."

    # After downloading, we must re-check and extract anything that's still missing.
    for config_line in "${ARCHIVE_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"
        target_path="$dest_path/$final_name"
        zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

        if [ -e "$target_path" ]; then
            continue
        fi

        if [ -f "$zip_file" ]; then
            echo "    -> Extracting newly downloaded '$zip_file'..."
            unzip -q "$zip_file" -d "$dest_path"
        else
            echo "    -> FATAL: Downloader ran but '$zip_file' is still missing. Aborting."
            exit 1
        fi
    done
fi

echo "--> All components are present and correctly placed."

# ==============================================================================
# --- End of Download/Extract block ---
# ==============================================================================



source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"

# --- 5. Project Configuration ---
# Ensures Python can treat 'config' directories as packages.
echo "--> Creating Python package markers (__init__.py)..."
touch config/__init__.py
touch config/languagetool_server/__init__.py

# --- User-Specific Configuration ---
# This part is about user config, so it's fine for it to stay here.
CONFIG_FILE="$HOME/.config/sl5-stt/config.toml"
echo "--> Ensuring user config file exists at $CONFIG_FILE..."
mkdir -p "$(dirname "$CONFIG_FILE")"
# Only write the file if it doesn't exist to avoid overwriting user settings
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[paths]" > "$CONFIG_FILE"
    echo "project_root = \"$(pwd)\"" >> "$CONFIG_FILE"
fi

# --- 6. Completion ---
echo ""
echo "--- Setup for openSUSE is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
