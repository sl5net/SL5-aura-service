#!/bin/bash
#
# setup/ubuntu_setup.sh
# Run this setup script from the project's root directory.
#

# --- Make script location-independent ---
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---

set -e

echo "--- Starting STT Setup for Debian/Ubuntu ---"

# --- 1. System Dependencies ---
# (This section remains unchanged)
echo "--> Checking for a compatible Java version (>=17)..."
JAVA_OK=0
if command -v java &> /dev/null; then
    VERSION=$(java -version 2>&1 | awk -F'[."]' '/version/ {print $2}')
    if [ "$VERSION" -ge 17 ]; then
        echo "    -> Found compatible Java version $VERSION. OK."
        JAVA_OK=1
    fi
fi
if [ "$JAVA_OK" -eq 0 ]; then
    echo "    -> Installing a modern JDK (>=17)..."
    sudo apt-get update && sudo apt-get install -y openjdk-21-jdk
fi
echo "--> Installing other core dependencies..."
sudo apt-get install -y \
    inotify-tools wget unzip portaudio19-dev python3-pip

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
download_and_verify() {
    local url=$1
    local zip_file=$2
    local expected_sha256=$3
    local extract_dir=$4
    local final_dir_check=$5

    if [ ! -d "$final_dir_check" ]; then
        echo "    -> Downloading $(basename $zip_file)..."
        curl -L "$url" -o "$zip_file"

        echo "    -> Verifying checksum for $(basename $zip_file)..."
        # Use a robust checksum command that works on most systems
        if echo "$expected_sha256  $zip_file" | sha256sum --check --status; then
            echo "    -> Checksum OK. Extracting..."
            # Unzip to the specified directory, creating it if necessary
            unzip -q "$zip_file" -d "$extract_dir"
            echo "    -> Cleaning up $(basename $zip_file)..."
            rm "$zip_file"
        else
            echo "    -> FATAL: Checksum mismatch for $(basename $zip_file)!"
            echo "       Expected: $expected_sha256"
            # Clean up the corrupted download
            rm "$zip_file"
            exit 1
        fi
    else
        echo "    -> $(basename $final_dir_check) already exists. Skipping."
    fi
}

# --- Execute Downloads ---
download_and_verify "$LT_URL" "$LT_ZIP" "$LT_SHA256" "." "$LT_DIR"
download_and_verify "$EN_MODEL_URL" "models/$EN_MODEL_ZIP" "$EN_MODEL_SHA256" "models/" "$EN_MODEL_DIR"
download_and_verify "$DE_MODEL_URL" "models/$DE_MODEL_ZIP" "$DE_MODEL_SHA256" "models/" "$DE_MODEL_DIR"

# --- 6. User-Specific Configuration ---
# This part is about user config, so it's fine for it to stay here.
CONFIG_FILE="$HOME/.config/sl5-stt/config.toml"
echo "--> Ensuring user config file exists at $CONFIG_FILE..."
mkdir -p "$(dirname "$CONFIG_FILE")"
# Only write the file if it doesn't exist to avoid overwriting user settings
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[paths]" > "$CONFIG_FILE"
    echo "project_root = \"$(pwd)\"" >> "$CONFIG_FILE"
fi

# --- 7. Completion ---
echo ""
echo "--- Setup for Ubuntu is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
