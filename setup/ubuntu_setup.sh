#!/bin/bash
#
# setup/ubuntu_setup.sh
# Run this setup script from the project's root directory.
#

SCRIPT_NAME=$(basename "$0")
# Check if the script is run from the project root.
# This check is more robust than changing directory.
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: Please run this script from the project's root directory."
    echo ""
    echo "cd .. ; ./setup/$SCRIPT_NAME"
    exit 1
fi

sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv

eval $(python3 scripts/py/setup_config.py)
echo "LANG 1: $SELECTED_LANG | LANG 2: $SECOND_LANG | EXCLUDE_LANGUAGES: $EXCLUDE_LANGUAGES"

# --- Make script location-independent ---
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---

set -e



echo "--- Starting STT Setup for Debian/Ubuntu ---"

sudo apt-get update -y

sudo add-apt-repository universe -y
sudo apt install pkg-config libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype-dev -y



# setup/ubuntu_setup.sh
# --- 1. System Dependencies ---
# (This section remains unchanged)
echo "--> Checking for a compatible Java version (>=17)..."
JAVA_OK=0
if command -v java &> /dev/null; then
    VERSION=$(java -version 2>&1 | awk -F[\".] '/version/ {print ($2 == "1") ? $3 : $2}')
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
    echo "    -> Installing a modern JDK (>=17)..."
    sudo apt-get update && sudo apt-get install -y openjdk-21-jdk
fi
echo "--> Installing other core dependencies..."
sudo apt-get install -y \
    inotify-tools wget unzip portaudio19-dev python3-pip \
    ffmpeg libnotify-bin xclip xvfb

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

# ==============================================================================
# --- 5. Download and Extract Required Components ---
# This block intelligently handles downloads and extractions.
# ==============================================================================
echo "--> Checking for required components (LanguageTool, Vosk-Models)..."
# --- Download/Extract block ---
source "$SCRIPT_DIR/download_and_extract_helper.sh"
# ==============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"


# --- Install fzf (Fuzzy Finder) ---
if ! command -v fzf &> /dev/null; then
    echo "[INFO] fzf not found. Installing..."
    # We use apt for simplicity in the setup script
    sudo apt-get update && sudo apt-get install -y fzf

    # Optional: If you want the latest version with full shell bindings:
    # git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    # ~/.fzf/install --all
else
    echo "[INFO] fzf is already installed."
fi






# --- 5. Project Configuration ---
# Ensures Python can treat 'config' directories as packages.
echo "--> Creating Python package markers (__init__.py)..."
touch config/__init__.py
touch config/languagetool_server/__init__.py

# --- User-Specific Configuration ---
# This part is about user config, so it's fine for it to stay here.
CONFIG_FILE="$HOME/.config/sl5-stt/config.toml"
echo "--> Ensuring user config file exists at $CONFIG_FILE..."
mkdir -p "$(dirname "$CONFIG_FILE")"
# Only write the file if it doesn't exist to avoid overwriting user settings
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[paths]" > "$CONFIG_FILE"
    echo "project_root = \"$(pwd)\"" >> "$CONFIG_FILE"
fi



# --- dotool setup ---
if ! command -v dotool &> /dev/null; then
    echo "--> Installing dotool..."
    sudo apt-get install -y dotool || echo "WARNING: dotool not in apt repos. Install manually. See docs/LINUX_WAYLAND_dotool.md"
fi
sudo usermod -aG input $USER
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
echo "NOTE: Re-login required for input group to take effect."
echo "See docs/LINUX_WAYLAND_dotool.md for details."

# --- Automatisches Setzen des Standard-Modells ---
echo "--> Configuring default model in config/model_name.txt..."
if [ "$CI" == "true" ]; then
    echo "vosk-model-small-en-us-0.15" > config/model_name.txt
elif [ "$SELECTED_LANG" == "de" ]; then
    echo "vosk-model-de-0.21" > config/model_name.txt
else
    echo "Please set a vosk-model in config/model_name.txt e.g. vosk-model-en-us-0.22 and check https://alphacephei.com/vosk/models"
fi


# --- 6. Completion ---
echo ""
echo "--- Setup for Ubuntu is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""


