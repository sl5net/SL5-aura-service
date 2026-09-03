#!/usr/bin/env bash
#
# setup/helper/install_dotool.sh
# Installs dotool and dotoold binaries and configures uinput permissions.
#

set -euo pipefail

INSTALL_DIR="/usr/local/bin"

if command -v dotool &> /dev/null && command -v dotoold &> /dev/null; then
    echo "[INFO] dotool and dotoold are already installed."
else
    echo "[INFO] Installing dotool..."

    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm --needed dotool || true
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y dotool || true
    fi

    if ! command -v dotool &> /dev/null; then
        if command -v apt-get &> /dev/null; then
            echo "[INFO] Installing golang to compile dotool..."
            sudo apt-get update -y && sudo apt-get install -y golang-go libx11-dev libxtst-dev
            echo "[INFO] Compiling and installing dotool via go..."
            GOBIN="${INSTALL_DIR}" sudo -E go install git.sr.ht/~geb/dotool@latest
        fi
    fi
fi

echo "[INFO] Configuring /dev/uinput permissions..."
getent group input >/dev/null 2>&1 || sudo groupadd -r input 2>/dev/null || true
TARGET_USER="${SUDO_USER:-${USER:-$(id -un)}}"
sudo usermod -aG input "${TARGET_USER}" || true
[ -n "${USER}" ] && sudo usermod -aG input "${USER}" 2>/dev/null || true
echo 'KERNEL=="uinput", GROUP="input", MODE="0660", OPTIONS+="static_node=uinput"' \
  | sudo tee /etc/udev/rules.d/80-dotool.rules > /dev/null
sudo udevadm control --reload-rules || true
sudo udevadm trigger || true
sudo chmod 0666 /dev/uinput 2>/dev/null || true

echo "[INFO] dotool setup complete."
