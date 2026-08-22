#!/bin/bash
#
# setup/helper/setup_copyq.sh
# Installs CopyQ, configures trigger command, and creates autostart desktop entry.
#

set -e

HOTKEY="${1:-${SELECTED_HOTKEY:-F12}}"
TRIGGER_CMD="touch /tmp/sl5_record.trigger"

echo "[INFO] Setting up CopyQ with trigger shortcut: ${HOTKEY}..."

if ! command -v copyq &> /dev/null; then
    echo "[INFO] Installing CopyQ via package manager..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -y && sudo apt-get install -y copyq
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm --needed copyq
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y copyq
    elif command -v zypper &> /dev/null; then
        sudo zypper install -y copyq
    else
        echo "[WARNING] Unknown package manager. Please install CopyQ manually."
    fi
else
    echo "[INFO] CopyQ is already installed."
fi

if ! pgrep -x "copyq" > /dev/null; then
    copyq --start-server &
    sleep 1
fi

copyq eval "
var newCmd = {
    name: 'SL5 Voice Trigger',
    cmd: '${TRIGGER_CMD}',
    globalShortcuts: ['${HOTKEY}'],
    isGlobalShortcut: true,
    icon: '\xf028'
};
var cmds = commands();
var filtered = cmds.filter(function(c){ return c.name !== 'SL5 Voice Trigger'; });
filtered.push(newCmd);
setCommands(filtered);
"
AUTOSTART_DIR="${HOME}/.config/autostart"
mkdir -p "${AUTOSTART_DIR}"

cat <<EOF > "${AUTOSTART_DIR}/copyq.desktop"
[Desktop Entry]
Type=Application
Name=CopyQ
GenericName=Clipboard Manager
Comment=CopyQ Clipboard Manager with SL5 Voice Trigger
Exec=copyq
Icon=copyq
Terminal=false
Categories=Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

echo "[INFO] CopyQ configuration and autostart setup complete."

