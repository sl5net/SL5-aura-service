#!/bin/bash
# setup/suse_setup.sh
# Run this setup script from the project's root directory.
set -uo pipefail

SCRIPT_NAME=$(basename "$0")
# Check if the script is run from the project root.
# This check is more robust than changing directory.
if [ ! -f "requirements.txt" ]; then
    echo "ERROR: Please run this script from the project's root directory."
    echo ""
    echo "cd .. ; ./setup/$SCRIPT_NAME"
    exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
#cd "$PROJECT_ROOT"

# This script may run as a normal user (with sudo) or as root in a
# container/CI runner with no sudo binary installed at all. Guard every
# privileged call through $SUDO instead of assuming sudo exists.
if command -v sudo >/dev/null 2>&1; then
  SUDO="sudo"
else
  SUDO=""
fi

# setup/suse_setup.sh:20

echo "--> Refreshing repositories..."
$SUDO zypper -n refresh

echo "--> Resolving Python and compiler packages (robust across openSUSE releases) ..."
# Package names shift between openSUSE releases -- e.g. Leap 16.0 moved the
# base interpreter to the versioned "python313" package (companion pip/devel
# packages still use the unversioned "python3-" alias), while older Leap
# releases used "python311"/"python310"/"python3" directly, and gcc moved
# from unversioned "gcc"/"gcc-c++" to versioned "gccNN"/"gccNN-c++".
# Rather than hardcoding one release's names, probe candidate sets (newest
# first) and use the first one that fully resolves in the enabled repos.
#
# Existence is checked with `zypper search --match-exact`, a read-only,
# side-effect-free query parsed from its printed output -- NOT by trusting
# `zypper install --dry-run`'s exit code, which has known inconsistent
# behavior across zypper versions (see https://github.com/openSUSE/zypper/issues/539).
PY_CANDIDATES=(
  "python313 python3-pip python3-devel"
  "python313 python313-pip python313-devel"
  "python311 python3-pip python3-devel"
  "python311 python311-pip python311-devel python311-venv"
  "python310 python310-pip python310-devel python310-venv"
  "python3 python3-pip python3-devel python3-venv"
  "python3 python3-pip python3-devel"
  "python3 python3-base python3-devel"
)
GCC_CANDIDATES=(
  "gcc15 gcc15-c++"
  "gcc14 gcc14-c++"
  "gcc13 gcc13-c++"
  "gcc12 gcc12-c++"
  "gcc gcc-c++"
)
COMMON="git tar make"

# Optional: if running under GitHub Actions, also surface results in the
# job summary. Harmless no-op standalone (GITHUB_STEP_SUMMARY unset -> /dev/null).
SUMMARY="${GITHUB_STEP_SUMMARY:-/dev/null}"
{
  echo "### Package resolution diagnostics"
  echo
  echo "| Package | Found? |"
  echo "|---|---|"
} >> "$SUMMARY"

pkg_exists() {
  local pkg="$1" out
  out=$(zypper -n search --match-exact "$pkg" 2>&1) || true
  if grep -qw -- "$pkg" <<< "$out"; then
    echo "| $pkg | yes |" >> "$SUMMARY"
    return 0
  else
    echo "| $pkg | **no** |" >> "$SUMMARY"
    return 1
  fi
}

pick_working_set() {
  # $1 = name of caller's result variable, remaining args = candidate sets
  local __result_var="$1"; shift
  local set
  for set in "$@"; do
    echo "  -> Trying candidate set: $set"
    local ok=true pkg
    for pkg in $set; do
      if ! pkg_exists "$pkg"; then
        ok=false
        echo "     Package '$pkg' not found -- rejecting this candidate set."
        break
      fi
    done
    if [ "$ok" = true ]; then
      printf -v "$__result_var" '%s' "$set"
      return 0
    fi
  done
  return 1
}

PY_SET=""
if ! pick_working_set PY_SET "${PY_CANDIDATES[@]}"; then
  echo "ERROR: No usable python package set resolved for this system."
  echo "See the table above for exactly which packages were tried and missing."
  echo "You may need to enable an additional repo, e.g. for older Leap releases:"
  echo "  $SUDO zypper addrepo -f https://download.opensuse.org/repositories/devel:languages:python/openSUSE_Leap_15.5/ devel:languages:python"
  echo "  $SUDO zypper refresh"
  exit 1
fi
echo "--> Selected python set: $PY_SET"

GCC_SET=""
if ! pick_working_set GCC_SET "${GCC_CANDIDATES[@]}"; then
  echo "ERROR: No usable gcc package set resolved for this system."
  exit 1
fi
echo "--> Selected gcc set: $GCC_SET"

echo "Installing: $COMMON $PY_SET $GCC_SET"
$SUDO zypper -n install $COMMON $PY_SET $GCC_SET

# Map resolved package name -> actual interpreter/compiler binary names.
# Versioned packages (python313, gcc15, ...) install as python3.13/gcc-15,
# not literally "python313"/"gcc15".
PY_PKG=$(awk '{print $1}' <<< "$PY_SET")
case "$PY_PKG" in
  python3) PY_BIN="python3" ;;
  python3[0-9][0-9]) PY_BIN="python3.${PY_PKG#python3}" ;;
  *) PY_BIN="$PY_PKG" ;;
esac

GCC_PKG=$(awk '{print $1}' <<< "$GCC_SET")
case "$GCC_PKG" in
  gcc) CC="gcc"; CXX="g++" ;;
  gcc[0-9][0-9]) GCC_VER="${GCC_PKG#gcc}"; CC="gcc-${GCC_VER}"; CXX="g++-${GCC_VER}" ;;
  *) CC="$GCC_PKG"; CXX="$GCC_PKG" ;;
esac

echo "--> Verifying resolved interpreter/compiler are actually callable..."
for bin in "$PY_BIN" "$CC" "$CXX"; do
  if ! command -v "$bin" >/dev/null 2>&1; then
    echo "ERROR: expected binary '$bin' (from package '$PY_PKG'/'$GCC_PKG') is not on PATH."
    exit 1
  fi
done
"$PY_BIN" --version
"$CC" --version | head -1
"$CXX" --version | head -1

# Export so every later step in this script -- and any pip build that shells
# out to a C/C++ compiler (e.g. building wheels like fasttext) -- picks up
# the real, versioned compiler instead of a missing/non-functional "cc".
export CC CXX

eval $(./.venv/bin/python scripts/py/setup_config.py 2>/dev/null) || eval $($PY_BIN scripts/py/setup_config.py)
echo "LANG 1: $SELECTED_LANG | LANG 2: $SECOND_LANG | EXCLUDE_LANGUAGES: $EXCLUDE_LANGUAGES"


# Ensure virtualenv exists and pip is available inside it
if [ ! -d ".venv" ]; then
  echo "--> Creating Python virtual environment in './.venv'..."
  "$PY_BIN" -m venv .venv
fi

echo "--> Ensuring pip is available in the venv and upgrading packaging tools..."
# Try ensurepip first, then upgrade pip/setuptools/wheel via venv python
./.venv/bin/python -m ensurepip --upgrade 2>/dev/null || true
./.venv/bin/python -m pip install --upgrade pip setuptools wheel

echo "--> Installing project Python requirements..."
./.venv/bin/python -m pip install -r requirements.txt


SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROJECT_ROOT=$(dirname "$SCRIPT_DIR")
cd "$PROJECT_ROOT"

echo "--> Running setup from project root: $(pwd)"
# --- End of location-independent block ---

echo "--- Starting STT Setup for openSUSE ---"
# --- End of location-independent block ---

set -e

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

echo "--> Installing core dependencies..."
$SUDO zypper -n install \
    inotify-tools wget unzip portaudio-devel


if [ "$JAVA_OK" -eq 0 ]; then
    echo "    -> Installing a modern JDK (>=17)..."
    $SUDO zypper refresh && $SUDO zypper -n install java-21-openjdk
fi


# --- 2. Python Virtual Environment ---
# (Already created above, kept here for standalone-script compatibility.)
if [ ! -d ".venv" ]; then
    echo "--> Creating Python virtual environment in './.venv'..."
    "$PY_BIN" -m venv .venv
else
    echo "--> Virtual environment already exists. Skipping creation."
fi

# --- 3. Python Requirements ---
# (Already installed above; re-run is a fast no-op if nothing changed.)
echo "--> Installing Python requirements into the virtual environment..."
./.venv/bin/pip install -r requirements.txt

# --- 4. Project Structure and Configuration ---
echo "--> Setting up project directories and initial files..."
"$PY_BIN" "scripts/py/func/create_required_folders.py" "$(pwd)"




# ==============================================================================
# --- 5. Download and Extract Required Components ---
# This block intelligently handles downloads and extractions.
# ==============================================================================

echo "--> Checking for required components (LanguageTool, Vosk-Models)..."

# --- Configuration ---
PREFIX="Z_"

if [ "$GITHUB_ACTIONS" == "true" ]; then
  # Format: "BaseName FinalDirName DestinationPath"
  ARCHIVE_CONFIG=(
      "LanguageTool-6.6 LanguageTool-6.6 ."
      "vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15 ./models"
      "lid.176 lid.176.bin ./models"
  )
  echo "--> GitHub CI detected: Large models (0.21, 0.22) excluded to prevent 502 errors."
else
  # Format: "BaseName FinalDirName DestinationPath"
  ARCHIVE_CONFIG=(
      "LanguageTool-6.6 LanguageTool-6.6 ."
      "vosk-model-en-us-0.22 vosk-model-en-us-0.22 ./models"
      "vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15 ./models"
      "vosk-model-de-0.21 vosk-model-de-0.21 ./models"
      "lid.176 lid.176.bin ./models"
  )
fi

DOWNLOAD_REQUIRED=false

# --- Filter Configuration based on EXCLUDE_LANGUAGES ---
INSTALL_CONFIG=()
if [ -z "$EXCLUDE_LANGUAGES" ]; then
    # Keine Ausschlüsse, die gesamte MASTER-Liste wird installiert.
    INSTALL_CONFIG=("${ARCHIVE_CONFIG[@]}")
else
    # Ausschlüsse aktiv, die Liste wird gefiltert.
    for config_line in "${ARCHIVE_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"

        IS_MANDATORY=false
        IS_EXCLUDED=false

        # Komponenten, die immer benötigt werden (z.B. LanguageTool Core)
        if [[ "$base_name" == "LanguageTool-6.6" ]] || [[ "$base_name" == "lid.176" ]]; then
            IS_MANDATORY=true
        fi

        # 1. Ausschluss-Check: exclude=all
        if [ "$EXCLUDE_LANGUAGES" == "all" ] && [ "$IS_MANDATORY" = false ]; then
            echo "    -> Excluding (all): $base_name"
            IS_EXCLUDED=true
        fi

        # 2. Ausschluss-Check: Spezifische Sprachen (z.B. de, en)
        if [ "$IS_EXCLUDED" = false ]; then
            # Test auf 'de' im Namen und in der Ausschlussliste
            if [[ "$base_name" =~ vosk-model-de- ]] && [[ "$EXCLUDE_LANGUAGES" =~ de ]]; then
                echo "    -> Excluding (de): $base_name"
                IS_EXCLUDED=true
            fi
            # Test auf 'en' im Namen und in der Ausschlussliste
            if [[ "$base_name" =~ vosk-model.*en-us ]] && [[ "$EXCLUDE_LANGUAGES" =~ en ]]; then
                echo "    -> Excluding (en): $base_name"
                IS_EXCLUDED=true
            fi


            if [[ "$base_name" == "vosk-model-en-us-0.22" ]] && ([[ "$EXCLUDE_LANGUAGES" =~ en ]] || [[ "$CI" == "true" ]]); then
                echo "    -> Excluding large in CI (en): $base_name"
                IS_EXCLUDED=true
            fi



            # Hinzufügen weiterer spezifischer Exklusionsregeln nach Bedarf...
        fi

        # Nur hinzufügen, wenn nicht ausgeschlossen
        if [ "$IS_EXCLUDED" = false ]; then
            INSTALL_CONFIG+=("$config_line")
        fi
    done
fi
# --- End Filter Configuration ---


# --- Phase 1: Check and attempt to restore from local ZIP cache ---
echo "    -> Phase 1: Checking and trying to restore from local cache..."
for config_line in "${INSTALL_CONFIG[@]}"; do
    read -r base_name final_name dest_path <<< "$config_line"
    target_path="$dest_path/$final_name"
    zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

    # If the component already exists, we're good for this one.
    if [ -e "$target_path" ]; then
        continue
    fi

    # The component is missing. Let's see if we can unzip it from a local cache.
    echo "    -> Missing: '$target_path'. Searching for '$zip_file'..."
    if [ -f "$zip_file" ]; then
        echo "    -> Found ZIP cache. Extracting '$zip_file'..."
        unzip -q "$zip_file" -d "$dest_path"
    else
        # The ZIP is not there. We MUST run the downloader.
        echo "    -> ZIP cache not found. A download is required."
        DOWNLOAD_REQUIRED=true
    fi
done

# --- Phase 2: Download if necessary ---
if [ "$DOWNLOAD_REQUIRED" = true ]; then
    echo "    -> Phase 2: Running Python downloader for missing components..."

    # Create the models directory before attempting to download files into it.
    mkdir -p ./models

    ./.venv/bin/python tools/download_all_packages.py --exclude "$EXCLUDE_LANGUAGES"
    echo "    -> Downloader finished. Retrying extraction..."

    # After downloading, we must re-check and extract anything that's still missing.
    for config_line in "${INSTALL_CONFIG[@]}"; do
        read -r base_name final_name dest_path <<< "$config_line"
        target_path="$dest_path/$final_name"
        zip_file="$PROJECT_ROOT/${PREFIX}${base_name}.zip"

        if [ -e "$target_path" ]; then
            continue
        fi

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
# --- End of Download/Extract block ---
# ==============================================================================




# --- Install fzf (Fuzzy Finder) ---
if ! command -v fzf &> /dev/null; then
    echo "[INFO] fzf not found. Installing..."
    $SUDO zypper install -y fzf
else
    echo "[INFO] fzf is already installed."
fi




source "$(dirname "${BASH_SOURCE[0]}")/../scripts/sh/get_lang.sh"

# --- 5. Project Configuration ---
# Ensures Python can treat 'config' directories as packages.

echo '--> Creating Python package markers (__init__.py)...'
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
    $SUDO zypper install -y dotool || echo "WARNING: dotool not found in repos. Install manually. See docs/LINUX_WAYLAND_dotool.md"
fi
$SUDO usermod -aG input $USER
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | $SUDO tee /etc/udev/rules.d/80-dotool.rules
$SUDO udevadm control --reload-rules && $SUDO udevadm trigger
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
echo "--- Setup for openSUSE is complete! ---"
echo ""
echo "To activate the environment and run the server, use the following commands:"
echo "  source .venv/bin/activate"
echo "  ./scripts/restart_venv_and_run-server.sh"
echo ""
