#!/bin/bash
set -e

echo "Ensuring system dependencies are installed..."
sudo pacman -S --noconfirm --needed inotify-tools openjdk-21-jre-headless wget unzip

echo "Creating Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Checking for LanguageTool..."
LT_VERSION="6.6"
if [ ! -d "LanguageTool-${LT_VERSION}" ]; then
  echo "Downloading LanguageTool..."
  wget https://languagetool.org/download/LanguageTool-${LT_VERSION}.zip
  unzip LanguageTool-${LT_VERSION}.zip
  rm LanguageTool-${LT_VERSION}.zip
fi

echo "Checking for Vosk models..."
mkdir -p models

if [ ! -d "models/vosk-model-en-us-0.22" ]; then
  echo "Downloading English Vosk model..."
  wget -P models/ https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
  unzip models/vosk-model-en-us-0.22.zip -d models/
  rm models/vosk-model-en-us-0.22.zip
fi

if [ ! -d "models/vosk-model-de-0.21" ]; then
  echo "Downloading German Vosk model..."
  wget -P models/ https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip
  unzip models/vosk-model-de-0.21.zip -d models/
  rm models/vosk-model-de-0.21.zip
fi

echo "Setup complete."
