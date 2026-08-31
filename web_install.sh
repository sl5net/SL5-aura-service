#!/usr/bin/env bash
set -e

# Immediately terminate entire process group on single Ctrl+C
trap 'echo -e "\n[INFO] Installation aborted by user."; kill 0 2>/dev/null; exit 130' INT TERM

APP_NAME="sl5-aura-service"
#export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"

mkdir -p "${HOME}/programs"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/programs/}"
export INSTALL_DIR="${XDG_DATA_HOME}/${APP_NAME}"
REPO_BRANCH="${AURA_BRANCH:-master}"
REPO_TAR_URL="https://github.com/sl5net/SL5-aura-service/archive/refs/heads/${REPO_BRANCH}.tar.gz"
echo "============================================"
echo "   SL5 Aura Service - Web One-Liner Setup   "
echo "============================================"
echo "[INFO] Installation target: ${INSTALL_DIR}"
echo "[INFO] Alternative setups (e.g. Docker) are available in setup/"

if ! command -v curl >/dev/null 2>&1 && ! command -v wget >/dev/null 2>&1; then
    echo "[ERROR] Neither 'curl' nor 'wget' is installed. Please install curl or wget first."
    exit 1
fi

if ! command -v tar >/dev/null 2>&1; then
    echo "[ERROR] 'tar' is required but not installed. Please install tar first."
    exit 1
fi

mkdir -p "${INSTALL_DIR}"

echo "[INFO] Downloading and extracting latest release…"
if command -v curl >/dev/null 2>&1; then
    curl -sSL "${REPO_TAR_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1
elif command -v wget >/dev/null 2>&1; then
    wget -qO- "${REPO_TAR_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1
fi

echo "[INFO] Launching system setup…"
cd "${INSTALL_DIR}"
chmod +x setup/linux_mac_setup.sh

# Check if non-interactive mode is requested via flag or env variable
NON_INTERACTIVE_MODE=false
for arg in "$@"; do
    if [ "$arg" = "--non-interactive" ] || [ "$arg" = "-y" ] || [ "$arg" = "--yes" ]; then
        NON_INTERACTIVE_MODE=true
        break
    fi
done

if [ "$NON_INTERACTIVE_MODE" = true ] || [ "$NON_INTERACTIVE" = "true" ]; then
    # Explicitly non-interactive -> do not attach /dev/tty
    exec bash setup/linux_mac_setup.sh "$@"
elif [ -t 0 ]; then
    # Direct execution in terminal
    exec bash setup/linux_mac_setup.sh "$@"
elif ( : < /dev/tty ) 2>/dev/null; then
    # Piped (curl | bash) in an interactive terminal -> reconnect stdin
    exec bash setup/linux_mac_setup.sh "$@" < /dev/tty
else
    # Fallback for headless environments (CI / Docker)
    exec bash setup/linux_mac_setup.sh "$@"
fi
