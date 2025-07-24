#!/bin/bash
# file: update.sh
# Description: Downloads the latest version and updates the application for Linux/macOS.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
REPO_URL="https://github.com/sl5net/Vosk-System-Listener/archive/refs/heads/master.zip"
INSTALL_DIR="$(cd "$(dirname "$0")/.." && pwd)" # Absolute path to project root
TEMP_DIR=$(mktemp -d)

# --- Colors for output ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# --- Cleanup function ---
# This will be called on script exit, ensuring the temp dir is always removed.
trap 'rm -rf "$TEMP_DIR"' EXIT

# --- Main Script ---
echo -e "${GREEN}--- SL5 Dictation Updater for Linux/macOS ---${NC}"

# 1. Check for required dependencies
for cmd in curl unzip rsync; do
  if ! command -v $cmd &> /dev/null; then
    echo -e "${RED}FATAL: Required command '$cmd' is not installed.${NC}"
    echo "Please install it using your system's package manager (e.g., 'sudo apt install $cmd')."
    exit 1
  fi
done

echo "This will download the latest version and replace all application files."
echo "Your personal settings in 'config/settings_local.py' will be saved."
read -p "Press Enter to continue or CTRL+C to cancel"

# 2. Backup local settings
LOCAL_SETTINGS="$INSTALL_DIR/config/settings_local.py"
if [ -f "$LOCAL_SETTINGS" ]; then
  echo -e "${GREEN}INFO: Backing up your local settings...${NC}"
  cp "$LOCAL_SETTINGS" "$TEMP_DIR/settings_local.py.bak"
fi

# 3. Download the latest version
ZIP_PATH="$TEMP_DIR/latest.zip"
echo "INFO: Downloading latest version from GitHub..."
curl -L -s -o "$ZIP_PATH" "$REPO_URL"

# 4. Extract the archive
echo "INFO: Extracting update..."
unzip -q "$ZIP_PATH" -d "$TEMP_DIR"
EXTRACTED_DIR="$TEMP_DIR/Vosk-System-Listener-master"

# 5. Restore local settings into the new version
if [ -f "$TEMP_DIR/settings_local.py.bak" ]; then
  echo -e "${GREEN}INFO: Restoring your local settings...${NC}"
  cp "$TEMP_DIR/settings_local.py.bak" "$EXTRACTED_DIR/config/"
fi

# 6. Use rsync to move the new files into the installation directory
echo "INFO: Finalizing update..."
rsync -a --remove-source-files "$EXTRACTED_DIR/" "$INSTALL_DIR/"

echo -e "\n${GREEN}--- Update Complete ---${NC}"
echo "You can now restart the application."
