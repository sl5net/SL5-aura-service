#!/usr/bin/env bash
#
# setup/helper/install_cudatext.sh
# Installs CudaText editor for Linux distributions.
#

set -euo pipefail

if command -v cudatext &> /dev/null; then
    echo "[INFO] CudaText is already installed ($(command -v cudatext))."
    exit 0
fi

echo "[INFO] Installing CudaText editor..."

# Arch / Manjaro
if command -v pacman &> /dev/null; then
    if command -v yay &> /dev/null; then
        yay -S --noconfirm cudatext-gtk2-bin || true
    fi
fi

# Debian / Ubuntu / Linux Mint
if ! command -v cudatext &> /dev/null; then
    TMP_DIR=$(mktemp -d)
    OPT_DIR="/opt/cudatext"

    echo "[INFO] Downloading CudaText release package..."
    CUDATEXT_URL="https://downloads.sourceforge.net/project/cudatext/release/Linux/cudatext-linux-gtk2-amd64-1.236.0.0.tar.xz"
    wget -q --show-progress -O "${TMP_DIR}/cudatext.tar.xz" "${CUDATEXT_URL}" || \
    wget -q -O "${TMP_DIR}/cudatext.tar.xz" "http://uvviewsoft.com/cudatext/files_linux/cudatext-linux-gtk2-amd64-1.236.0.0.tar.xz"

    echo "[INFO] Extracting CudaText to ${OPT_DIR}..."
    sudo mkdir -p "${OPT_DIR}"
    sudo tar -xf "${TMP_DIR}/cudatext.tar.xz" -C "${OPT_DIR}" --strip-components=1 2>/dev/null || \
    sudo tar -xf "${TMP_DIR}/cudatext.tar.xz" -C "${OPT_DIR}"

    sudo chmod +x "${OPT_DIR}/cudatext"
    sudo ln -sf "${OPT_DIR}/cudatext" /usr/local/bin/cudatext
    sudo ln -sf "${OPT_DIR}/cudatext" /usr/bin/cudatext 2>/dev/null || true

    rm -rf "${TMP_DIR}"
fi

if command -v cudatext &> /dev/null; then
    echo "[INFO] CudaText installed successfully."
else
    echo "[WARNING] CudaText could not be installed automatically."
fi
