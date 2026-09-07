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
    elif [ "$(uname -s)" = "Darwin" ]; then
        echo "[INFO] macOS detected. Installing CopyQ from official release DMG..."
        ARCH=$(uname -m)
        if [ "${ARCH}" = "arm64" ]; then
            PATTERN="m1\.dmg"
            FALLBACK_URL="https://github.com/hluk/CopyQ/releases/download/v16.0.0/CopyQ-16.0.0-macos-12-m1.dmg"
        else
            PATTERN="macos-.*\.dmg"
            FALLBACK_URL="https://github.com/hluk/CopyQ/releases/download/v16.0.0/CopyQ-16.0.0-macos-13.dmg"
        fi
        CURL_HDR=()
        if [ -n "${GITHUB_TOKEN:-}" ]; then
            CURL_HDR=(-H "Authorization: token ${GITHUB_TOKEN}")
        fi
        DMG_URL=$(curl -fsSL "${CURL_HDR[@]}" https://api.github.com/repos/hluk/CopyQ/releases/latest 2>/dev/null | grep "browser_download_url" | grep -E "${PATTERN}" | head -n 1 | cut -d '"' -f 4 || true)
        DMG_URL="${DMG_URL:-${FALLBACK_URL}}"
        TMP_DMG="/tmp/CopyQ.dmg"
        echo "[INFO] Downloading CopyQ from ${DMG_URL}..."
        curl -fsSL -L "${DMG_URL}" -o "${TMP_DMG}"
        MOUNT_DIR=$(mktemp -d /tmp/copyq_mount.XXXXXX)
        hdiutil attach "${TMP_DMG}" -nobrowse -mountpoint "${MOUNT_DIR}" -quiet

        cp -R "${MOUNT_DIR}/CopyQ.app" /Applications/
        hdiutil detach "${MOUNT_DIR}" -quiet || true
        rm -rf "${MOUNT_DIR}" "${TMP_DMG}"
        xattr -cr /Applications/CopyQ.app 2>/dev/null || true
        codesign --force --deep --sign - /Applications/CopyQ.app 2>/dev/null || true
    else      
        echo "[WARNING] Unknown package manager. Please install CopyQ manually."
    fi
else
    echo "[INFO] CopyQ is already installed."
fi

if [ "$(uname -s)" = "Darwin" ]; then
    if [ -x "/Applications/CopyQ.app/Contents/MacOS/copyq" ]; then
        if command -v brew &> /dev/null; then
            BREW_BIN="$(brew --prefix 2>/dev/null)/bin"
            mkdir -p "${BREW_BIN}"
            ln -sfn "/Applications/CopyQ.app/Contents/MacOS/copyq" "${BREW_BIN}/copyq" 2>/dev/null || true
        fi
        export PATH="/Applications/CopyQ.app/Contents/MacOS:$PATH"
    fi
fi



if [ "$(id -u)" -eq 0 ] && [ -n "${SUDO_USER:-}" ] && [ "${SUDO_USER}" != "root" ]; then
    TARGET_USER="${SUDO_USER}"
    TARGET_UID="$(id -u "${TARGET_USER}")"
    RUNTIME_DIR="/run/user/${TARGET_UID}"
    USER_CMD=(sudo -u "${TARGET_USER}" \
        DISPLAY="${DISPLAY:-:0}" \
        DBUS_SESSION_BUS_ADDRESS="unix:path=${RUNTIME_DIR}/bus" \
        XDG_RUNTIME_DIR="${RUNTIME_DIR}")
    echo "[INFO] Running as root via sudo - delegating CopyQ commands to user '${TARGET_USER}'."
else
    USER_CMD=()
fi

if [ "$(uname -s)" = "Darwin" ]; then
    if ! pgrep -x "copyq" > /dev/null 2>&1 && ! pgrep -x "CopyQ" > /dev/null 2>&1; then
        open -a CopyQ 2>/dev/null || copyq --start-server &
        sleep 2
    fi
else
    if [ "$(id -u)" -eq 0 ]; then
        pkill -9 -f "/usr/bin/copyq" 2>/dev/null || true
        sleep 0.5
    fi
    if ! "${USER_CMD[@]}" pgrep -x "copyq" > /dev/null 2>&1; then
        "${USER_CMD[@]}" copyq --start-server &
        sleep 1
    fi
fi

JS_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/scripts/search_rules/run_rule_copyq.js"
if [ ! -f "${JS_PATH}" ]; then
    echo "[ERROR] CopyQ search script not found: ${JS_PATH}"
    exit 1
fi

"${USER_CMD[@]}" copyq eval "
var f = File('${JS_PATH}');
var scriptText = '';
if (f.open()) {
    scriptText = str(f.readAll());
    f.close();
}
var voiceCmd = {
    name: 'SL5 Voice Trigger',
    cmd: '${TRIGGER_CMD}',
    globalShortcuts: ['${HOTKEY}'],
    isGlobalShortcut: true,
    icon: 'audio-volume-high'
};
var searchCmd = {
    name: 'SL5 Rule Search',
    cmd: 'copyq:' + String.fromCharCode(10) + scriptText,
    globalShortcuts: ['Meta+Y', 'F11'],
    isGlobalShortcut: true,
    icon: 'search'
};
var cmds = commands();
var filtered = cmds.filter(function(c){ return c.name !== 'SL5 Voice Trigger' && c.name !== 'SL5 Rule Search'; });
filtered.push(voiceCmd);
filtered.push(searchCmd);
setCommands(filtered);
"

if [ "$(uname -s)" = "Darwin" ]; then
    copyq config autostart true 2>/dev/null || true
    osascript -e 'tell application "System Events" to make login item at end with properties {path:"/Applications/CopyQ.app", hidden:false}' 2>/dev/null || true
    echo "[INFO] CopyQ configuration complete."
    echo "[IMPORTANT] Accessibility Permissions Required on macOS:"
    echo "  Please open 'System Settings -> Privacy & Security -> Accessibility'"
    echo "  and ensure 'CopyQ' and your terminal emulator are granted access."
    echo "  Otherwise, global hotkeys like '${HOTKEY}' cannot be detected."
else
    if [ "$(id -u)" -eq 0 ] && [ -n "${SUDO_USER:-}" ]; then
        TARGET_HOME="$(getent passwd "${SUDO_USER}" | cut -d: -f6)"
    else
        TARGET_HOME="${HOME}"
    fi
    AUTOSTART_DIR="${TARGET_HOME}/.config/autostart"
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
    if [ "$(id -u)" -eq 0 ] && [ -n "${SUDO_USER:-}" ]; then
        chown -R "${SUDO_USER}:${SUDO_USER}" "${AUTOSTART_DIR}/copyq.desktop"
    fi
    echo "[INFO] CopyQ configuration and autostart setup complete."
fi

