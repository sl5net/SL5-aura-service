#!/bin/bash
#
# setup/manjaro_arch_setup.sh
# Run this setup script from the project's root directory.
#

SCRIPT_NAME=$(basename "$0")
# Check if the script is run from the project root.
# This check is more robust than changing directory.
if [ ! -f "scripts/infra/requirements/requirements.txt" ]; then
    echo "ERROR: Please run this script from the project's root directory."
    echo ""
    echo "cd .. ; ./setup/$SCRIPT_NAME"
    exit 1
fi

sudo pacman -S --noconfirm --needed base-devel python python-pip uv

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

SL5NET_AURA_PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$SL5NET_AURA_PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---

set -e

echo "--- Starting STT Setup for Manjaro/Arch Linux ---"

# --- Python Virtual Environment ---
if [ ! -d ".venv" ]; then
    echo "--> Creating Python 3.12 virtual environment in './.venv'"
    uv venv --python 3.12 .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

eval "$(./.venv/bin/python scripts/py/setup_config.py 2>/dev/null || python3 scripts/py/setup_config.py)"
echo "LANG 1: $SELECTED_LANG | LANG 2: $SECOND_LANG | EXCLUDE_LANGUAGES: $EXCLUDE_LANGUAGES"
  

# setup/manjaro_arch_setup.sh
# --- 1. System Dependencies ---
echo "--> Checking for a compatible Java version (>=17)…"

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
    echo "    -> Installing a modern JDK to satisfy the requirement…"
    sudo pacman -S --noconfirm --needed jdk-openjdk
fi
echo "--> Installing other core dependencies…"
sudo pacman -S --noconfirm --needed \
    inotify-tools wget unzip portaudio xdotool

sudo pacman -S --noconfirm --needed sdl2 sdl2_mixer sdl2_ttf sdl2_image


# --- 3. Python Requirements ---
echo "--> Installing Python requirements into the virtual environment"
uv pip install --python .venv/bin/python -r scripts/infra/requirements/requirements.txt
# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files…"
# THIS IS THE KEY CHANGE. We call the Python script and pass the current
# working directory (which is the project root) as an argument.
# This one command replaces all old 'mkdir' and 'touch' commands for the project structure.

./.venv/bin/python "scripts/py/func/create_required_folders.py" "$(pwd)"


# ==============================================================================
# --- 4.1. Download and Extract Required Components ---
# This block intelligently handles downloads and extractions.
echo "--> Checking for required components (LanguageTool, Vosk-Models)…"
source "$(dirname "${BASH_SOURCE[0]}")/helper/download_and_extract_helper.sh"
if [ -f "$(dirname "${BASH_SOURCE[0]}")/helper/install_cudatext.sh" ]; then
    echo "--> Installing CudaText and plugins"
    bash "$(dirname "${BASH_SOURCE[0]}")/helper/install_cudatext.sh"
fi
# ==============================================================================

# --- Configure default model ---
echo "--> Configuring default model in config/model_name.txt…"
if [ "${CI:-}" = "true" ]; then
    echo "vosk-model-small-en-us-0.15" > config/model_name.txt
elif [ "${SELECTED_LANG:-}" = "de" ]; then
    echo "vosk-model-de-0.21" > config/model_name.txt
else
    echo "Please set a vosk-model in config/model_name.txt e.g. vosk-model-en-us-0.22 and check https://alphacephei.com/vosk/models"
fi



# After: show preview and ask for confirmation (default: no)
echo "The script can optionally run a full system upgrade (pacman -Syu)."
echo "This may download and install many packages (kernel, libs, etc.)."

# Use native bash read with timeout to avoid python stdin EOF error
read_upgrade="n"
if [ -t 0 ]; then
    read -t 8 -p "Run full system upgrade now? (y/N) [Auto N in 8s]: " read_upgrade || true
fi
read_upgrade=${read_upgrade:-n}


if [[ "$read_upgrade" =~ ^[Yy]$ ]]; then
    echo "Running system upgrade (this may be large)…"
    sudo pacman -Syu
else
    echo "Skipping full system upgrade. You can run 'sudo pacman -Syu' later."
fi
