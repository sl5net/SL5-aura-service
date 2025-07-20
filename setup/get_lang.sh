#!/bin/bash

set -e

# --- Detect language code from arguments or environment ---
# 1. Try first argument
# 2. Then try $LANG (system locale)
# 3. Default to 'en-us' if all else fails

# Function to normalize LANG to a Vosk-compatible code
get_lang_code() {
    case "$1" in
        en_US*|en*) echo "en-us" ;;
        es_*)       echo "es" ;;
        de_*)       echo "de" ;;
        fr_*)       echo "fr" ;;
        ru_*)       echo "ru" ;;
        zh_*)       echo "cn" ;;
        *)          echo "en-us" ;;  # default fallback
    esac
}

# Extract language code from env if not passed as $1
RAW_LANG="${1:-$(get_lang_code "$LANG")}"
LANG_CODE="${RAW_LANG,,}"  # convert to lowercase (bash >= 4)
MODEL_VERSION="${2:-0.22}"

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_DIR="$SCRIPT_DIR/../models"
MODEL_NAME="vosk-model-${LANG_CODE}-${MODEL_VERSION}"
MODEL_PATH="${MODEL_DIR}/${MODEL_NAME}"
MODEL_URL="https://alphacephei.com/vosk/models/${MODEL_NAME}.zip"

# Create model directory
mkdir -p "$MODEL_DIR"

# Check and download if not present
if [ ! -d "$MODEL_PATH" ]; then
  echo "-> Downloading Vosk model for '${LANG_CODE}'..."
  wget "$MODEL_URL" -O "${MODEL_DIR}/model.zip"
  unzip -q "${MODEL_DIR}/model.zip" -d "$MODEL_DIR"
  rm "${MODEL_DIR}/model.zip"
else
  echo "-> Model '${MODEL_NAME}' already exists."
fi
