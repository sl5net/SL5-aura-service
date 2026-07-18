#!/bin/bash
#
# setup/manjaro_arch_setup.sh
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

sudo pacman -S --noconfirm python python-pip

eval $(python3 scripts/py/setup_config.py)
echo "LANG 1: $SELECTED_LANG | LANG 2: $SECOND_LANG | EXCLUDE_LANGUAGES: $EXCLUDE_LANGUAGES"

echo ""
echo "--- Setup for Manjaro/Arch is complete! ---"
echo ""

echo "Optional: If you are running Wayland (e.g. KDE Plasma 6, CachyOS),"
echo "  'dotool' is REQUIRED for system-wide text input."
echo "  On X11 dotool is optional but recommended for better compatibility."
echo "  Install with:"

echo "  yay -S dotool"
echo "  sudo gpasswd -a \$USER input"
echo "  echo 'KERNEL==\"uinput\", GROUP=\"input\", MODE=\"0660\", OPTIONS+=\"static_node=uinput\"' | sudo tee /etc/udev/rules.d/80-dotool.rules"
echo "  sudo udevadm control --reload-rules && sudo udevadm trigger"
echo "  (Re-login required after group change)"
echo "  Then set x11_input_method_OVERRIDE = 'dotool' in config/settings_local.py"
echo ""
echo "To start Aura:"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""















SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---

set -e

echo "--- Starting STT Setup for Manjaro/Arch Linux ---"

# setup/manjaro_arch_setup.sh
# --- 1. System Dependencies ---
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
    echo "    -> Installing a modern JDK to satisfy the requirement..."
    sudo pacman -S --noconfirm --needed jdk-openjdk
fi
echo "--> Installing other core dependencies..."
sudo pacman -S --noconfirm --needed \
    inotify-tools wget unzip portaudio xdotool

sudo pacman -S --needed sdl2 sdl2_mixer sdl2_ttf sdl2_image

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

# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files..."
# THIS IS THE KEY CHANGE. We call the Python script and pass the current
# working directory (which is the project root) as an argument.
# This one command replaces all old 'mkdir' and 'touch' commands for the project structure.
python3 "scripts/py/func/create_required_folders.py" "$(pwd)"


# ==============================================================================
# --- 4.1. Download and Extract Required Components ---
# This block intelligently handles downloads and extractions.
echo "--> Checking for required components (LanguageTool, Vosk-Models)..."
source "$(dirname "${BASH_SOURCE[0]}")/download_and_extract_helper.sh"
# ==============================================================================



# After: show preview and ask for confirmation (default: no)
echo "The script can optionally run a full system upgrade (pacman -Syu)."
echo "This may download and install many packages (kernel, libs, etc.)."

# Use native bash read with timeout to avoid python stdin EOF error
read -t 8 -p "Run full system upgrade now? (y/N) [Auto N in 8s]: " read_upgrade
read_upgrade=${read_upgrade:-n}

DOWNLOAD_REQUIRED=false


if [[ "$read_upgrade" =~ ^[Yy]$ ]]; then
    echo "Running system upgrade (this may be large)..."
    sudo pacman -Syu
else
    echo "Skipping full system upgrade. You can run 'sudo pacman -Syu' later."
fi