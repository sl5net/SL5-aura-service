#!/bin/bash
#
# setup/nixos_setup.sh
#
# ⚠️  EXPERIMENTAL — UNTESTED by the authors (we don't run NixOS).
#     Written by analogy with ubuntu_setup.sh. Please report what breaks!
#
# HOW TO USE:
#   1. Enter the Nix shell first:
#          nix-shell setup/shell.nix
#   2. Then run this script from the project root:
#          bash setup/nixos_setup.sh
#
# WHY two steps?
#   shell.nix makes C libraries (portaudio, alsa, etc.) visible to Python wheels.
#   This script does everything else: venv, pip, downloads, config.
#

SCRIPT_NAME=$(basename "$0")

# --- Sanity check: must be run from project root ---
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: Please run this script from the project's root directory."
    echo ""
    echo "  cd .. ; bash setup/$SCRIPT_NAME"
    exit 1
fi

# --- Sanity check: should be inside nix-shell ---
if [ -z "$IN_NIX_SHELL" ]; then
    echo "WARNING: \$IN_NIX_SHELL is not set. Are you inside 'nix-shell setup/shell.nix'?"
    echo "         Continuing anyway, but pip installs of C-extension packages may fail."
    echo ""
fi

set -e

# --- Make script location-independent ---
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"
echo "--> Running setup from project root: $(pwd)"

# --- Language config ---
eval $(python3 scripts/py/setup_config.py)
echo "LANG 1: $SELECTED_LANG | LANG 2: $SECOND_LANG | EXCLUDE_LANGUAGES: $EXCLUDE_LANGUAGES"

echo ""
echo "--- Starting STT Setup for NixOS ---"
echo "    (⚠️  Untested — please report issues!)"
echo ""

# ==============================================================================
# --- 1. System Dependencies ---
# On NixOS, system packages are managed via shell.nix (or configuration.nix).
# We check here that the critical ones are actually available at runtime,
# and give a helpful error if not.
# ==============================================================================

echo "--> Checking runtime dependencies provided by shell.nix..."

check_cmd() {
    if ! command -v "$1" &> /dev/null; then
        echo "    ERROR: '$1' not found. Make sure you are inside 'nix-shell setup/shell.nix'."
        echo "           If it is still missing, add it to buildInputs in shell.nix."
        exit 1
    else
        echo "    OK: $1"
    fi
}

check_cmd python3
check_cmd pip
check_cmd unzip
check_cmd wget
check_cmd ffmpeg
check_cmd fzf

# Java >= 17 check
echo "--> Checking for a compatible Java version (>=17)..."
JAVA_OK=0
if command -v java &> /dev/null; then
    VERSION=$(java -version 2>&1 | awk -F[\".] '/version/ {print ($2 == "1") ? $3 : $2}')
    if [ "$VERSION" -ge 17 ] 2>/dev/null; then
        echo "    -> Found compatible Java version $VERSION. OK."
        JAVA_OK=1
    else
        echo "    -> Found Java version $VERSION, but we need >=17."
    fi
else
    echo "    -> No Java executable found."
fi
if [ "$JAVA_OK" -eq 0 ]; then
    echo ""
    echo "    ERROR: Java >=17 is required but not available."
    echo "    Add it to shell.nix buildInputs:"
    echo "      jdk21"
    echo "    or install it system-wide in /etc/nixos/configuration.nix:"
    echo "      environment.systemPackages = with pkgs; [ jdk21 ];"
    echo ""
    exit 1
fi

# ==============================================================================
# --- 2. Python Virtual Environment ---
# On NixOS, we still use a venv so pip packages are isolated.
# The LD_LIBRARY_PATH set by shell.nix makes C extensions work inside the venv.
# ==============================================================================

if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    python3 -m venv .venv --system-site-packages
    # --system-site-packages is sometimes needed on NixOS so the venv can
    # find nixpkgs-provided libs. Remove it if it causes conflicts.
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# ==============================================================================
# --- 3. Python Requirements ---
# ==============================================================================

echo "--> Installing Python requirements into the virtual environment..."
./.venv/bin/pip install -r requirements.txt

# ==============================================================================
# --- 4. Project Structure ---
# ==============================================================================

echo "--> Setting up project directories and initial files..."
python3 "scripts/py/func/create_required_folders.py" "$(pwd)"

# ==============================================================================
# --- 5. Download and Extract Required Components ---
# (LanguageTool, Vosk models — identical logic to ubuntu_setup.sh)
# ==============================================================================

echo "--> Checking for required components (LanguageTool, Vosk-Models)..."

PREFIX="Z_"
ARCHIVE_CONFIG=(
    "LanguageTool-6.6 LanguageTool-6.6 ."
    "vosk-model-en-us-0.22 vosk-model-en-us-0.22 ./models"
    "vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15 ./models"
    "vosk-model-de-0.21 vosk-model-de-0.21 ./models"
    "lid.176 lid.176.bin ./models"
)
DOWNLOAD_REQUIRED=false

# --- Filter based on EXCLUDE_LANGUAGES ---
INSTALL_CONFIG=()
if [ -z "$EXCLUDE_LANGUAGES" ]; then
    INSTALL_CONFIG=("${ARCHIVE_CONFIG[@]}")
else
    for config_line in "${ARCHIVE_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"
        IS_MANDATORY=false
        IS_EXCLUDED=false

        if [[ "$base_name" == "LanguageTool-6.6" ]] || [[ "$base_name" == "lid.176" ]]; then
            IS_MANDATORY=true
        fi

        if [ "$EXCLUDE_LANGUAGES" == "all" ] && [ "$IS_MANDATORY" = false ]; then
            echo "    -> Excluding (all): $base_name"
            IS_EXCLUDED=true
        fi

        if [ "$IS_EXCLUDED" = false ]; then
            if [[ "$base_name" =~ vosk-model-de- ]] && [[ "$EXCLUDE_LANGUAGES" =~ de ]]; then
                echo "    -> Excluding (de): $base_name"; IS_EXCLUDED=true
            fi
            if [[ "$base_name" =~ vosk-model-en-us- ]] && [[ "$EXCLUDE_LANGUAGES" =~ en ]]; then
                echo "    -> Excluding (en): $base_name"; IS_EXCLUDED=true
            fi
            if [[ "$base_name" == "vosk-model-en-us-0.22" ]] && ([[ "$EXCLUDE_LANGUAGES" =~ en ]] || [[ "$CI" == "true" ]]); then
                echo "    -> Excluding large in CI (en): $base_name"; IS_EXCLUDED=true
            fi
        fi

        if [ "$IS_EXCLUDED" = false ]; then
            INSTALL_CONFIG+=("$config_line")
        fi
    done
fi

# --- Phase 1: restore from local ZIP cache ---
echo "    -> Phase 1: Checking and trying to restore from local cache..."
for config_line in "${INSTALL_CONFIG[@]}"; do
    read -r base_name final_name dest_path <<< "$config_line"
    target_path="$dest_path/$final_name"
    zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

    if [ -e "$target_path" ]; then continue; fi

    echo "    -> Missing: '$target_path'. Searching for '$zip_file'..."
    if [ -f "$zip_file" ]; then
        echo "    -> Found ZIP cache. Extracting '$zip_file'..."
        unzip -q "$zip_file" -d "$dest_path"
    else
        echo "    -> ZIP cache not found. A download is required."
        DOWNLOAD_REQUIRED=true
    fi
done

# --- Phase 2: download if necessary ---
if [ "$DOWNLOAD_REQUIRED" = true ]; then
    echo "    -> Phase 2: Running Python downloader for missing components..."
    mkdir -p ./models
    ./.venv/bin/python tools/download_all_packages.py --exclude "$EXCLUDE_LANGUAGES"
    echo "    -> Downloader finished. Retrying extraction..."

    for config_line in "${INSTALL_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"
        target_path="$dest_path/$final_name"
        zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

        if [ -e "$target_path" ]; then continue; fi

        if [ -f "$zip_file" ]; then
            echo "    -> Extracting newly downloaded '$zip_file'..."
            unzip -q "$zip_file" -d "$dest_path"
        else
            echo "    -> FATAL: Downloader ran but '$zip_file' is still missing. Aborting."
            exit 1
        fi
    done
fi

echo "--> All components are present and correctly placed."

# ==============================================================================
# --- 6. Language detection helper ---
# ==============================================================================

source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"

# ==============================================================================
# --- 7. dotool setup ---
# On NixOS, dotool must be installed via configuration.nix or home-manager.
# We cannot use apt or sudo here in the traditional sense.
# ==============================================================================

echo "--> Checking for dotool..."
if ! command -v dotool &> /dev/null; then
    echo ""
    echo "    WARNING: 'dotool' not found."
    echo "    On NixOS, install it via configuration.nix:"
    echo "      environment.systemPackages = with pkgs; [ dotool ];"
    echo "    or via home-manager. See docs/LINUX_WAYLAND_dotool.md for details."
    echo ""
    echo "    After installing dotool, also add yourself to the 'input' group:"
    echo "      users.users.<yourname>.extraGroups = [ \"input\" ];"
    echo "    and add this udev rule to configuration.nix:"
    echo '      services.udev.extraRules = '"'"'"'"'"'
    echo '        KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"'
    echo '      '"'"'"'"'"';'
    echo "    Then rebuild: sudo nixos-rebuild switch"
    echo "    A re-login is required for the group change to take effect."
    echo ""
else
    echo "    OK: dotool found."
fi

# ==============================================================================
# --- 8. Python package markers ---
# ==============================================================================

echo "--> Creating Python package markers (__init__.py)..."
touch config/__init__.py
touch config/languagetool_server/__init__.py

# ==============================================================================
# --- 9. User config file ---
# ==============================================================================

CONFIG_FILE="$HOME/.config/sl5-stt/config.toml"
echo "--> Ensuring user config file exists at $CONFIG_FILE..."
mkdir -p "$(dirname "$CONFIG_FILE")"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "[paths]" > "$CONFIG_FILE"
    echo "project_root = \"$(pwd)\"" >> "$CONFIG_FILE"
fi

# ==============================================================================
# --- 10. Default model ---
# ==============================================================================

echo "--> Configuring default model in config/model_name.txt..."
if [ "$CI" == "true" ]; then
    echo "vosk-model-small-en-us-0.15" > config/model_name.txt
elif [ "$SELECTED_LANG" == "de" ]; then
    echo "vosk-model-de-0.21" > config/model_name.txt
else
    echo "Please set a vosk-model in config/model_name.txt e.g. vosk-model-en-us-0.22"
    echo "See https://alphacephei.com/vosk/models"
fi

# ==============================================================================
# --- Done ---
# ==============================================================================

echo ""
echo "--- Setup for NixOS complete! (⚠️  Untested — please report issues!) ---"
echo ""
echo "IMPORTANT: If you haven't already, add the missing NixOS-specific packages"
echo "to your shell.nix or configuration.nix (see warnings above for dotool, Java, etc.)"
echo ""
echo "To run the server:"
echo "  nix-shell setup/shell.nix"
echo "  bash scripts/restart_venv_and_run-server.sh"
echo ""
