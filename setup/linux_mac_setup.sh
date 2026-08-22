#!/bin/bash
# 
# setup/linux_mac_setup.sh
# Universal POSIX setup dispatcher for Linux and macOS.
#

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
OS_TYPE=$(uname -s)

if [ "${OS_TYPE}" = "Darwin" ]; then
    TARGET="${SCRIPT_DIR}/macos_setup.sh"
    echo "[INFO] Detected macOS (Darwin). Dispatching to ${TARGET}..."
    "${TARGET}" "$@"
    exit 0
fi

if [ "${OS_TYPE}" != "Linux" ]; then
    echo "[ERROR] Unsupported OS platform: ${OS_TYPE}"
    echo "[INFO] For Windows, please run: setup/windows11_setup.bat or setup/windows11_setup.ps1"
    exit 1
fi

if [ ! -f "/etc/os-release" ]; then
    echo "[ERROR] Cannot detect Linux distribution: /etc/os-release not found."
    exit 1
fi

OS_ID=$(grep -E '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')
OS_LIKE=$(grep -E '^ID_LIKE=' /etc/os-release | cut -d= -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')

case "${OS_ID}" in
    manjaro|arch|endeavouros|garuda)
        TARGET="${SCRIPT_DIR}/manjaro_arch_setup.sh"
        ;;
    linuxmint)
        TARGET="${SCRIPT_DIR}/mint_setup.sh"
        ;;
    ubuntu|debian|pop)
        TARGET="${SCRIPT_DIR}/ubuntu_setup.sh"
        ;;
    fedora|rhel|centos|rocky|almalinux)
        TARGET="${SCRIPT_DIR}/fedora_setup.sh"
        ;;
    opensuse*|suse)
        TARGET="${SCRIPT_DIR}/suse_setup.sh"
        ;;
    *)
        if [[ "${OS_LIKE}" =~ (arch) ]]; then
            TARGET="${SCRIPT_DIR}/manjaro_arch_setup.sh"
        elif [[ "${OS_LIKE}" =~ (ubuntu|debian) ]]; then
            TARGET="${SCRIPT_DIR}/ubuntu_setup.sh"
        elif [[ "${OS_LIKE}" =~ (fedora|rhel) ]]; then
            TARGET="${SCRIPT_DIR}/fedora_setup.sh"
        elif [[ "${OS_LIKE}" =~ (suse) ]]; then
            TARGET="${SCRIPT_DIR}/suse_setup.sh"
        else
            echo "[ERROR] Unsupported Linux distribution: ID='${OS_ID}', ID_LIKE='${OS_LIKE}'"
            echo "[INFO] Please run the appropriate script manually from setup/"
            exit 1
        fi
        ;;
esac

echo "[INFO] Detected Linux (${OS_ID}). Dispatching to ${TARGET}..."
"${TARGET}" "$@"

if [ "${CI}" != "true" ] && [ -t 0 ]; then
    echo ""
    read -r -p "Run CopyQ setup and hotkey configuration now? [Y/n] " user_choice
    user_choice=${user_choice:-y}
    if [[ "${user_choice}" =~ ^[yY](es)?$ ]]; then
        "${SCRIPT_DIR}/helper/setup_copyq.sh" "${SELECTED_HOTKEY:-F12}"
    fi
    echo ""
    read -r -p "Run Aura now? [Y/n] " user_choice
    user_choice=${user_choice:-y}
    if [[ "${user_choice}" =~ ^[yY](es)?$ ]]; then
#        "${SCRIPT_DIR}/../python3 aura_engine.py"
        "${SCRIPT_DIR}/../scripts/restart_venv_and_run-server.sh"
    fi
fi
