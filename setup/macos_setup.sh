#!/bin/bash
# setup/macos_setup.sh
set -e

echo "Starting setup for macOS..."

echo "1. Checking for Homebrew and installing dependencies..."
if ! command -v brew &> /dev/null; then
    echo "ERROR: Homebrew not found."
    echo "Please install Homebrew first by running:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
fi

# fswatch is the macOS equivalent of inotifywait
brew install fswatch openjdk@21 wget

echo "2. Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "3. Installing Python requirements..."
pip install -r requirements.txt

echo "4. Downloading external tools and models..."
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "Downloading LanguageTool..."
  wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip
  unzip -q LanguageTool-${LT_VERSION}.zip
  rm LanguageTool-${LT_VERSION}.zip
fi

mkdir -p models
if [ ! -d "models/vosk-model-en-us-0.22" ]; then
  echo "Downloading English Vosk model..."
  wget -qO- https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip | unzip -q -d models/
fi

if [ ! -d "models/vosk-model-de-0.21" ]; then
  echo "Downloading German Vosk model..."
  wget -qO- https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip | unzip -q -d models/
fi

echo "Setup for macOS complete."
echo
echo "IMPORTANT: To make Java available, you may need to add it to your PATH."
echo "Run this command:"
echo 'export PATH="$(brew --prefix openjdk@21)/bin:$PATH"'
echo "Consider adding it to your ~/.zshrc or ~/.bash_profile file."
