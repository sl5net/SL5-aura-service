# run this setup from project folder
# setup/ubuntu_setup.sh

#!/bin/bash
set -e

echo "Starting setup for Debian/Ubuntu..."

echo "1. Updating package list and installing system dependencies..."
sudo apt-get update
sudo apt-get install -y inotify-tools openjdk-21-jre-headless wget unzip libportaudio2

# the new ubunto(3.7.'25 18:55 Thu) wants:
sudo apt install python3.12-venv

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
  wget -qO- https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip | unzip -q - -d models/
fi

if [ ! -d "models/vosk-model-de-0.21" ]; then
  echo "Downloading German Vosk model..."
  wget -qO- https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip | unzip -q - -d models/
fi

touch config/__init__.py
touch config/languagetool_server/__init__.py

echo "Setup for Ubuntu complete."

