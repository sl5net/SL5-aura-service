#!/bin/bash
#
# setup/macos_setup.sh
# Run this setup script from the project's root directory.
#

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

# --- 6. External Tools & Models (using the robust Python downloader) ---
echo "--> Downloading external tools and models via Python downloader..."

# Create the models directory before attempting to download files into it.
mkdir -p ./models

# Execute the downloader and let 'set -e' handle errors
echo "    -> Running Python downloader..."
./.venv/bin/python tools/download_all_packages.py

echo "    -> Python downloader completed successfully."

# --- Now, extract the downloaded archives ---
echo "--> Extracting downloaded archives..."

# THE FIX IS HERE: Define the prefix, just like in the PowerShell script
PREFIX="Z_"

# Define an array of archives to process
# Format: "ZipFileName FinalDirName DestinationPath"
ARCHIVE_CONFIG=(
    "LanguageTool-6.6.zip LanguageTool-6.6 ."
    "vosk-model-en-us-0.22.zip vosk-model-en-us-0.22 ./models"
    "vosk-model-small-en-us-0.15.zip vosk-model-small-en-us-0.15 ./models"
    "vosk-model-de-0.21.zip vosk-model-de-0.21 ./models"
    "lid.176.zip lid.176.bin ./models"
)

# Function to extract and clean up
expand_and_cleanup() {
    local zip_file=$1
    local expected_dir=$2
    local dest_path=$3

    # Check if final directory already exists
    if [ -d "$dest_path/$expected_dir" ]; then
        echo "    -> Directory '$expected_dir' already exists. Skipping."
        return
    fi

    # Check if the downloaded zip exists
    if [ ! -f "$zip_file" ]; then
        echo "    -> FATAL: Expected archive not found: '$zip_file'"
        exit 1
    fi

    echo "    -> Extracting $zip_file to $dest_path..."
    unzip -q "$zip_file" -d "$dest_path"

    # Clean up the zip file
    rm "$zip_file"
    echo "    -> Cleaned up ZIP file: $zip_file"
}

# Execute extraction for each archive
for config_line in "${BASE_CONFIG[@]}"; do
    # Read the space-separated values into variables
    read -r base_name dest_path <<< "$config_line"

    # CONSTRUCT THE FILENAMES, including the prefix for the zip file
    zip_file="${PREFIX}${base_name}.zip"
    expected_dir="${base_name}" # The final directory name has no prefix

    expand_and_cleanup "$zip_file" "$expected_dir" "$dest_path"
done

echo "    -> Extraction and cleanup successful."





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
