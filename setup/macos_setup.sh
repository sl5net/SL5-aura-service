#!/bin/bash
set -e

# --- Make script location-independent ---
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"
echo "--> Running setup from project root: $(pwd)"

echo "--- Starting STT Setup for macOS ---"

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
    fi
fi

if [ "$JAVA_OK" -eq 0 ]; then
    echo "    -> Installing a modern JDK via Homebrew..."
    brew install openjdk
fi

echo "--> Installing other core dependencies..."
brew install fswatch wget unzip portaudio xdotool



# --- 2. Python Virtual Environment ---
# We check if the venv directory exists before creating it.
if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    python3 -m venv .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# --- 3. Python Requirements ---
echo "--> Installing Python requirements into the virtual environment..."
if ! ./.venv/bin/pip install -r requirements.txt; then
    echo "ERROR: Failed to install requirements. Trying to fix common version issues..."
    # Example: Fix vosk version, then retry
    sed -i.bak 's/vosk==0.3.45/vosk/' requirements.txt
    ./.venv/bin/pip install -r requirements.txt
fi

# --- 4. External Tools and Models ---
echo "--> Downloading external tools and models (if missing)..."

# Download and extract LanguageTool
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "    -> Downloading LanguageTool v${LT_VERSION}..."
  wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip -O languagetool.zip
  unzip -q languagetool.zip
  rm languagetool.zip
fi

# Download and extract Vosk Models (using the more robust two-step method)
mkdir -p models
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
