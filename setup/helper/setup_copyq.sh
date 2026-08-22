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
var voiceCmd = {
    name: 'SL5 Voice Trigger',
    cmd: '${TRIGGER_CMD}',
    globalShortcuts: ['${HOTKEY}'],
    isGlobalShortcut: true,
    icon: '\xf028'
};
var searchCmd = {
    name: 'SL5 Rule Search',
    cmd: 'var tmp_dir = \"/tmp\"; var rootFile = File(tmp_dir + \"/sl5_aura/sl5net_aura_project_root\"); var project_root = \"\"; if (rootFile.open()) { project_root = str(rootFile.readAll()).trim(); rootFile.close(); } var search_script = project_root + \"/scripts/search_rules/run_rule.sh\"; var active_win_title = str(execute(\"bash\", \"-c\", \"xdotool getactivewindow getwindowname 2>/dev/null || true\").stdout).trim(); var cmd = \"export LANG=\\\"de_DE.UTF-8\\\"; export LC_ALL=\\\"de_DE.UTF-8\\\"; export DBUS_SESSION_BUS_ADDRESS=\\\"unix:path=/run/user/\$(id -u)/bus\\\"; export SEARCH_FILES_FILTER=\\\"FUZZY_MAP*.py\\\"; export AURA_ACTIVE_WINDOW_TITLE=\\\"\" + active_win_title + \"\\\"; setsid konsole -e bash \\\"\" + search_script + \"\\\" </dev/null >/dev/null 2>&1 & disown\"; execute(\"bash\", \"-c\", cmd);',
    globalShortcuts: ['Meta+Y'],
    isGlobalShortcut: true,
    icon: '\xf002'
};
var cmds = commands();
var filtered = cmds.filter(function(c){ return c.name !== 'SL5 Voice Trigger' && c.name !== 'SL5 Rule Search'; });
filtered.push(voiceCmd);
filtered.push(searchCmd);
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

