#!/bin/bash
#
# setup/ubuntu_setup.sh
# Run this setup script from the project's root directory.
#

# Exit immediately if a command fails
set -e

echo "--- Starting STT Setup for Debian/Ubuntu ---"

# --- 1. System Dependencies ---
echo "--> Updating package list and installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    inotify-tools \
    openjdk-21-jre-headless \
    wget \
    unzip \
    libportaudio2 \
    xdotool \
    python3-venv

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

# --- 6. Completion ---
echo ""
echo "--- Setup for Ubuntu is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
