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
    # Get major version number
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

# --- 4. External Tools and Models ---
echo "--> Downloading external tools and models (if missing)..."

# Download and extract LanguageTool
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "    -> Downloading LanguageTool v${LT_VERSION}..."
  MAX_RETRIES=3
  RETRY_COUNT=0
  while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip -O languagetool.zip
    if [ $? -eq 0 ]; then
      # Download sucesful
      MIN_SIZE=240000000
      ACTUAL_SIZE=$(stat -c%s languagetool.zip)
      if [ $ACTUAL_SIZE -gt $MIN_SIZE ]; then
        echo "    -> size looks not bad"
        unzip -q languagetool.zip
        rm languagetool.zip
        break
      fi
      echo "    -> to small, retry..."
      RETRY_COUNT=$((RETRY_COUNT+1))
    else
      echo "    -> Download bad, retry..."
      RETRY_COUNT=$((RETRY_COUNT+1))
    fi
  done
  if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "    -> Download fehlgeschlagen, bitte überprüfen Sie Ihre Internetverbindung."
    exit 1
  fi
fi


# Download and extract LanguageTool
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "    -> Downloading LanguageTool v${LT_VERSION}..."
  wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip -O languagetool.zip

  # Überprüfen Sie die Größe des heruntergeladenen ZIP-Files
  MIN_SIZE=240000000
  ACTUAL_SIZE=$(stat -c%s languagetool.zip)
  if [ $ACTUAL_SIZE -lt $MIN_SIZE ]; then
    echo "    -> Fehlgeschlagen: Die Größe des heruntergeladenen ZIP-Files ist zu klein."
    rm languagetool.zip
    exit 1
  fi

  # Entpacken Sie das ZIP-File
  unzip -q languagetool.zip
  rm languagetool.zip
fi

echo "LanguageTool installation verified successfully."


























# Download and extract Vosk Models
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
echo "--- Setup for Manjaro/Arch is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
