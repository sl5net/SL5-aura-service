#!/bin/bash
#
# setup/manjaro_arch_setup.sh
# Run this setup script from the project's root directory.
#


# --- Make script location-independent ---
# This block ensures the script can be run from any directory.
# It finds the project root directory and changes into it.
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---



# Exit immediately if a command fails
set -e

echo "--- Starting STT Setup for Manjaro/Arch Linux ---"

# setup/manjaro_arch_setup.sh

# --- 1. System Dependencies ---
echo "--> Checking for a compatible Java version (>=17)..."

JAVA_OK=0
if command -v java &> /dev/null; then
    # Get major version (handle Java 8 and 9+)
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
    echo "    -> Installing a modern JDK to satisfy the requirement..."
    sudo pacman -S --noconfirm --needed jdk-openjdk
fi

echo "--> Installing other core dependencies..."
sudo pacman -S --noconfirm --needed \
    inotify-tools wget unzip portaudio xdotool



# --- 2. Python Virtual Environment ---
# We check if the venv directory exists before creating it.
if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    python3 -m venv .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# --- 3. Python Requirements ---
# We call pip from the venv directly. This is more robust than sourcing 'activate'.
echo "--> Installing Python requirements into the virtual environment..."
./.venv/bin/pip install -r requirements.txt





# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files..."
# THIS IS THE KEY CHANGE. We call the Python script and pass the current
# working directory (which is the project root) as an argument.
# This one command replaces all old 'mkdir' and 'touch' commands for the project structure.
python3 "scripts/py/func/create_required_folders.py" "$(pwd)"


# --- 5. External Tools and Models ---
echo "--> Downloading external tools and models from project GitHub Releases..."

# Define URLs and checksums for all assets
RELEASE_URL_BASE="https://github.com/sl5net/Vosk-System-Listener/releases/download/v0.2.0.1"

LT_ZIP="LanguageTool-6.6.zip"
LT_URL="${RELEASE_URL_BASE}/${LT_ZIP}"
LT_SHA256="53600506b399bb5ffe1e4c8dec794fd378212f14aaf38ccef9b6f89314d11631"
LT_DIR="LanguageTool-6.6"

EN_MODEL_ZIP="vosk-model-en-us-0.22.zip"
EN_MODEL_URL="${RELEASE_URL_BASE}/${EN_MODEL_ZIP}"
EN_MODEL_SHA256="d410847b53faf1850f2bb99fb7a08adcb49dd236dcba66615397fe57a3cf68f5"
EN_MODEL_DIR="models/vosk-model-en-us-0.22"

DE_MODEL_ZIP="vosk-model-de-0.21.zip"
DE_MODEL_URL="${RELEASE_URL_BASE}/${DE_MODEL_ZIP}"
DE_MODEL_SHA256="fb45a53025a50830b16bcda94146f90e22166501bb3693b009cabed796dbaaa0"
DE_MODEL_DIR="models/vosk-model-de-0.21"

# --- Download and Verify Function ---
# A reusable function to keep the code DRY (Don't Repeat Yourself)
# --- Download and Verify Function ---
download_and_verify() {
    local url=$1
    local zip_file=$2
    local expected_sha256=$3
    local extract_dir=$4
    local final_dir_check=$5
    local max_retries=3
    local retry_count=0
    local sha_cmd=""

    # Determine the correct sha256 command for the system
    if command -v sha256sum &> /dev/null; then
        sha_cmd="sha256sum"
    elif command -v shasum &> /dev/null; then
        sha_cmd="shasum -a 256"
    else
        echo "    -> FATAL: Could not find 'sha256sum' or 'shasum' command. Cannot verify downloads."
        exit 1
    fi

    echo "    -> Using '$sha_cmd' for checksum verification."

    if [ ! -d "$final_dir_check" ]; then
        while [ $retry_count -lt $max_retries ]; do
            echo "    -> Attempting to download $(basename $zip_file) (Attempt $((retry_count + 1))).."
            curl -L -s "$url" -o "$zip_file"

            echo "    -> Verifying checksum for $(basename $zip_file)..."
            # The corrected line uses the $sha_cmd variable
            if echo "$expected_sha256  $zip_file" | $sha_cmd --check --status; then
                echo "    -> Checksum OK. Extracting..."
                unzip -q "$zip_file" -d "$extract_dir"
                echo "    -> Cleaning up $(basename $zip_file)..."
                rm "$zip_file"
                return 0 # Success
            else
                echo "    -> WARNING: Checksum mismatch for $(basename $zip_file)!"
                echo "       Expected: $expected_sha256"
                rm "$zip_file" # Clean up the corrupted download
                retry_count=$((retry_count + 1))
                if [ $retry_count -lt $max_retries ]; then
                    echo "    -> Retrying in 2 seconds..."
                    sleep 2
                fi
            fi
        done

        echo "    -> FATAL: Failed to download and verify $(basename $zip_file) after $max_retries attempts."
        exit 1
    else
        echo "    -> $(basename $final_dir_check) already exists. Skipping."
    fi
}


# --- Execute Downloads ---
download_and_verify "$LT_URL" "$LT_ZIP" "$LT_SHA256" "." "$LT_DIR"
download_and_verify "$EN_MODEL_URL" "models/$EN_MODEL_ZIP" "$EN_MODEL_SHA256" "models/" "$EN_MODEL_DIR"
download_and_verify "$DE_MODEL_URL" "models/$DE_MODEL_ZIP" "$DE_MODEL_SHA256" "models/" "$DE_MODEL_DIR"








source "$(dirname "${BASH_SOURCE[0]}")/get_lang.sh"

# --- 5. Project Configuration ---
# Ensures Python can treat 'config' directories as packages.
echo "--> Creating Python package markers (__init__.py)..."
touch config/__init__.py
touch config/languagetool_server/__init__.py



CONFIG_FILE="$HOME/.config/sl5-stt/config.toml"
mkdir -p "$(dirname "$CONFIG_FILE")"
echo "[paths]" > "$CONFIG_FILE"
echo "project_root = \"$(pwd)\"" >> "$CONFIG_FILE"


# --- 6. Completion ---
echo ""
echo "--- Setup for Manjaro/Arch is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
