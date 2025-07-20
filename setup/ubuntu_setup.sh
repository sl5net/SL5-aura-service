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
echo "--> Downloading external tools and models (if missing)..."

# Download and extract LanguageTool
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "    -> Downloading LanguageTool v${LT_VERSION}..."
  wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip -O languagetool.zip
  unzip -q languagetool.zip
  rm languagetool.zip
fi

# Download and extract Vosk Models
# The Python script has already created the 'models' directory.
if [ ! -d "models/vosk-model-en-us-0.22" ]; then
  echo "    -> Downloading English Vosk model..."
  wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -O models/en.zip
  unzip -q models/en.zip -d models/
  rm models/en.zip
fi
if [ ! -d "models/vosk-model-de-0.21" ]; then
  echo "    -> Downloading German Vosk model..."
  wget https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip -O models/de.zip
  unzip -q models/de.zip -d models/
  rm models/de.zip
fi

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
