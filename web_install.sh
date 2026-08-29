#!/usr/bin/env bash
set -e

APP_NAME="sl5-aura-service"
INSTALL_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/${APP_NAME}"
REPO_TAR_URL="https://github.com/sl5net/SL5-aura-service/archive/refs/heads/master.tar.gz"

echo "============================================"
echo "   SL5 Aura Service - Web One-Liner Setup   "
echo "============================================"
echo "[INFO] Installation target: ${INSTALL_DIR}"

if ! command -v curl >/dev/null 2>&1; then
    echo "[ERROR] 'curl' is required but not installed. Please install curl first."
    exit 1
fi

if ! command -v tar >/dev/null 2>&1; then
    echo "[ERROR] 'tar' is required but not installed. Please install tar first."
    exit 1
fi

mkdir -p "${INSTALL_DIR}"

echo "[INFO] Downloading and extracting latest release..."
curl -sSL "${REPO_TAR_URL}" | tar -xz -C "${INSTALL_DIR}" --strip-components=1

echo "[INFO] Launching system setup..."
cd "${INSTALL_DIR}"
chmod +x setup/linux_mac_setup.sh
exec bash setup/linux_mac_setup.sh "$@"
