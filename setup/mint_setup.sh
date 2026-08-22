#!/bin/bash
#
# setup/mint_setup.sh
# Linux Mint setup forwarder delegating to ubuntu_setup.sh
#

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TARGET_SCRIPT="${SCRIPT_DIR}/ubuntu_setup.sh"

echo "[INFO] Linux Mint selected. Forwarding setup execution to ubuntu_setup.sh..."

if [ ! -f "${TARGET_SCRIPT}" ]; then
    echo "[ERROR] Target setup script not found: ${TARGET_SCRIPT}"
    exit 1
fi

exec "${TARGET_SCRIPT}" "$@"
