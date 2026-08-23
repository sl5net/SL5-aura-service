#!/bin/bash
#
# setup/helper/verify_distro.sh
# Validates that running OS matches expected distribution identifiers.
#

verify_distro() {
    local expected_patterns=("$@")
    if [ ! -f "/etc/os-release" ]; then
        echo "[WARNING] /etc/os-release not found. Skipping verification."
        return 0
    fi

    local os_id os_like
    os_id=$(grep -E '^ID=' /etc/os-release | cut -d= -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')
    os_like=$(grep -E '^ID_LIKE=' /etc/os-release | cut -d= -f2 | tr -d '"' | tr '[:upper:]' '[:lower:]')

    for pattern in "${expected_patterns[@]}"; do
        local pat_lower
        pat_lower=$(echo "$pattern" | tr '[:upper:]' '[:lower:]')
        if [[ "$os_id" == *"$pat_lower"* ]] || [[ "$os_like" == *"$pat_lower"* ]]; then
            return 0
        fi
    done

    echo "[ERROR] Incompatible distribution detected!"
    echo "[ERROR] Current OS: ID='${os_id}', ID_LIKE='${os_like}'."
    echo "[ERROR] Required: ${expected_patterns[*]}"
    echo "[INFO] Try running the automatic dispatcher: ./setup/setup.sh"
    exit 1
}
