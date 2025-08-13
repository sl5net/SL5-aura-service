#!/bin/bash
#
# setup/macos_setup.sh
# Run this setup script from the project's root directory.
#

should_remove_zips_after_unpack=true

# --- Make script location-independent ---
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
set -e
echo "--- Starting STT Setup for macOS ---"
# setup/macos_setup.sh
# --- 1. System Dependencies ---
if ! command -v brew &> /dev/null; then
    echo "ERROR: Homebrew not found. Please install it from https://brew.sh"
    exit 1
fi
echo "--> Checking for a compatible Java version (>=17)..."

JAVA_OK=0
if command -v java &> /dev/null; then
    VERSION=$(java -version 2>&1 | awk -F'[."]' '/version/ {print $2}')
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
    echo "    -> Installing a modern JDK via Homebrew..."
    brew install openjdk
fi
echo "--> Installing other core dependencies..."
brew install fswatch wget unzip portaudio


# --- 2. Python Virtual Environment ---
# We check if the venv directory exists before creating it.
if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    python3 -m venv .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# --- 3. Python Requirements ---
echo "--> Preparing requirements for macOS..."
# The macOS equivalent, 'fswatch', is already installed via Homebrew.
sed -i.bak '/inotify-tools/d' requirements.txt
echo "--> Installing Python requirements into the virtual environment..."
if ! ./.venv/bin/pip install -r requirements.txt; then
    echo "ERROR: Failed to install requirements. Trying to fix other common version issues..."
    # Example: Fix vosk version, then retry
    sed -i.bak 's/vosk==0.3.45/vosk/' requirements.txt
    # We run the command again after the potential fixes
    ./.venv/bin/pip install -r requirements.txt
fi
# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files..."
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


# --- 6. Completion ---
echo ""
echo "--- Setup for macOS is complete! ---"
echo ""
echo "IMPORTANT NEXT STEPS:"
echo ""
echo "1. Configure Java PATH:"
echo "   To make Java available, you may need to add it to your shell's PATH."
echo "   Run this command in your terminal:"
echo '   export PATH="$(brew --prefix openjdk@21)/bin:$PATH"'
echo "   (Consider adding this line to your ~/.zshrc or ~/.bash_profile file to make it permanent)."
echo ""
echo "2. Activate Environment and Run:"
echo "   To start the application, use the following commands:"
echo "   source .venv/bin/activate"
echo "   ./scripts/restart_venv_and_run-server.sh"
echo ""
echo "3. Potential macOS Permissions:"
echo "   The 'xdotool' utility may require you to grant Accessibility permissions"
echo "   to your Terminal app in 'System Settings -> Privacy & Security -> Accessibility'."
echo ""
