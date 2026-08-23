#!/bin/bash
#
# setup/mint_setup.sh
# Linux Mint setup forwarder delegating to ubuntu_setup.sh
#

set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "${SCRIPT_DIR}/.." && pwd)
LOG_DIR="${PROJECT_ROOT}/log"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/mint_setup.log"
exec > >(tee -a "${LOG_FILE}") 2>&1

TARGET_SCRIPT="${SCRIPT_DIR}/ubuntu_setup.sh"

echo "[INFO] Linux Mint selected. Forwarding setup execution to ubuntu_setup.sh..."

if [ ! -f "${TARGET_SCRIPT}" ]; then
    echo "[ERROR] Target setup script not found: ${TARGET_SCRIPT}"
    exit 1
fi

exec "${TARGET_SCRIPT}" "$@"
