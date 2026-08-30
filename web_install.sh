#!/usr/bin/env bash
set -e

APP_NAME="sl5-aura-service"
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/${APP_NAME}"
REPO_TAR_URL="https://github.com/sl5net/SL5-aura-service/archive/refs/heads/master.tar.gz"

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

echo "[INFO] Downloading and extracting latest release..."
if command -v curl >/dev/null 2>&1; then
    curl -sSL "${REPO_TAR_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1
elif command -v wget >/dev/null 2>&1; then
    wget -qO- "${REPO_TAR_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1
fi

echo "[INFO] Launching system setup..."
cd "${INSTALL_DIR}"
chmod +x setup/linux_mac_setup.sh

# Check if /dev/tty is available, then attach it to stdin
if [ -t 0 ] || [ -c /dev/tty ]; then
    exec bash setup/linux_mac_setup.sh "$@" < /dev/tty
else
    exec bash setup/linux_mac_setup.sh "$@"
fi

