#!/usr/bin/env bash
# setup/helper/install_cudatext.sh
# https://stackoverflow.com/ai-assist/chat/bc63713a-c27b-4f9f-80c6-47ae4deaa157 , 23.8.'26 17:27 Sun 

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
LOG_DIR="${PROJECT_ROOT}/log/setup"
mkdir -p "${LOG_DIR}"
LOG_FILE="${LOG_DIR}/install_cudatext.log"

exec > >(tee -a "${LOG_FILE}") 2>&1

CANDIDATE_NAME="cudatext"
OPT_DIR="/opt/${CANDIDATE_NAME}"
BIN_LINK="/usr/local/bin/${CANDIDATE_NAME}"
#SF_BASE="https://downloads.sourceforge.net/project/cudatext/release/Linux"

#FALLBACK_URL="https://downloads.sourceforge.net/project/cudatext/release/1.232.2.1/cudatext-linux-gtk2-amd64-1.232.2.1.tar.xz"

FALLBACK_URL="https://downloads.sourceforge.net/project/cudatext/release/1.232.2.1/cudatext-linux-gtk3-amd64-1.232.2.1.tar.xz"



cleanup() {
  local rc=$?
  [[ -n "${TMP_DIR:-}" && -d "${TMP_DIR}" ]] && rm -rf "${TMP_DIR}"
  return "${rc}"
}
trap cleanup EXIT

if command -v "${CANDIDATE_NAME}" >/dev/null 2>&1; then
  echo "[INFO] ${CANDIDATE_NAME} is already installed: $(command -v "${CANDIDATE_NAME}")"


elif [[ "$(uname -s)" == "Darwin" ]]; then
  ARCH="$(uname -m)"
  case "${ARCH}" in
    arm64|aarch64) TAR_NAME_PREFIX="cudatext-macos-cocoa-aarch64" ;;
    x86_64|amd64) TAR_NAME_PREFIX="cudatext-macos-cocoa-amd64" ;;
    *) echo "[ERROR] Unsupported macOS architecture: ${ARCH}"; exit 2 ;;
  esac
  TMP_DIR="$(mktemp -d)"
  CUDATEXT_URL="$(curl -fsSL "https://sourceforge.net/projects/cudatext/rss?path=/release" \
    | grep -E -o "https://[^<\"]*${TAR_NAME_PREFIX}[^<\"]*\\.zip/download" \
    | head -n1 || true)"
  if [[ -z "${CUDATEXT_URL:-}" ]]; then
    CUDATEXT_URL="https://downloads.sourceforge.net/project/cudatext/release/1.236.0.5/${TAR_NAME_PREFIX}-1.236.0.5.zip"
  fi

echo "[INFO] Downloading CudaText macOS from: ${CUDATEXT_URL}"
  curl -fSL -o "${TMP_DIR}/cudatext.zip" "${CUDATEXT_URL}"
  mkdir -p "${TMP_DIR}/extracted" "${TMP_DIR}/mnt"
  unzip -q "${TMP_DIR}/cudatext.zip" -d "${TMP_DIR}/extracted"

  DMG_FILE="$(find "${TMP_DIR}/extracted" -name "*.dmg" | head -n1 || true)"
  if [[ -n "${DMG_FILE}" ]]; then
    echo "[INFO] Mounting disk image: ${DMG_FILE}"
    hdiutil attach "${DMG_FILE}" -mountpoint "${TMP_DIR}/mnt" -nobrowse -quiet
    APP_SRC="$(find "${TMP_DIR}/mnt" -maxdepth 2 -name "*.app" | head -n1 || true)"
    if [[ -n "${APP_SRC}" ]]; then
      ${SUDO} rm -rf /Applications/CudaText.app
      ${SUDO} cp -R "${APP_SRC}" /Applications/CudaText.app
      echo "[INFO] Copied ${APP_SRC} to /Applications/CudaText.app"
    fi
    hdiutil detach "${TMP_DIR}/mnt" -quiet || true
  else
    APP_SRC="$(find "${TMP_DIR}/extracted" -name "*.app" -type d | head -n1 || true)"
    if [[ -n "${APP_SRC}" ]]; then
      ${SUDO} rm -rf /Applications/CudaText.app
      ${SUDO} cp -R "${APP_SRC}" /Applications/CudaText.app
      echo "[INFO] Copied ${APP_SRC} to /Applications/CudaText.app"
    fi
  fi

  APP_BIN="$(find /Applications/CudaText.app -type f -name "cudatext" 2>/dev/null | head -n1 || true)"
  [[ -z "${APP_BIN}" ]] && APP_BIN="$(find /Applications/CudaText.app/Contents/MacOS -type f -perm +111 2>/dev/null | head -n1 || true)"  
  
  if [[ -n "${APP_BIN}" ]]; then
    ${SUDO} chmod +x "${APP_BIN}" || true
    if command -v brew >/dev/null 2>&1; then
      BREW_BIN="$(brew --prefix)/bin"
      mkdir -p "${BREW_BIN}"
      ln -sf "${APP_BIN}" "${BREW_BIN}/cudatext" || true
    fi
    ${SUDO} mkdir -p /usr/local/bin
    ${SUDO} ln -sf "${APP_BIN}" /usr/local/bin/cudatext 2>/dev/null || true
    echo "[INFO] CudaText binary ${APP_BIN} symlinked to PATH."
  else
    echo "[ERROR] Failed to locate CudaText binary inside /Applications/CudaText.app"
    exit 3
  fi
else
  
  
  # Detect architecture
  ARCH="$(uname -m)"
  case "${ARCH}" in
  
#    x86_64|amd64) TAR_NAME_PREFIX="cudatext-linux-gtk2-amd64" ;;
#    aarch64|arm64) TAR_NAME_PREFIX="cudatext-linux-gtk2-arm64" ;;
#  
      x86_64|amd64) TAR_NAME_PREFIX="cudatext-linux-gtk3-amd64" ;;
      aarch64|arm64) TAR_NAME_PREFIX="cudatext-linux-gtk3-arm64" ;;  
  
    *)
      echo "[ERROR] Unsupported CPU architecture: ${ARCH}"
      exit 2
      ;;
  esac
  
  TMP_DIR="$(mktemp -d)"
  echo "[INFO] Temporary directory: ${TMP_DIR}"
  
  echo "[INFO] Attempting to resolve latest release URL..."
  
  if command -v curl >/dev/null 2>&1; then
    CUDATEXT_URL="$(curl -fsSL "https://sourceforge.net/projects/cudatext/rss?path=/release" \
      | grep -o "https://[^<\"]*${TAR_NAME_PREFIX}-[^<\"]*\\.tar\\.xz/download" \
      | head -n1 || true)"
  fi

  if [[ -z "${CUDATEXT_URL:-}" ]]; then
    echo "[WARN] Automatic resolution failed, using fallback URL."
    CUDATEXT_URL="${FALLBACK_URL}"
  fi
  
  echo "[INFO] Downloading from: ${CUDATEXT_URL}"
  if command -v curl >/dev/null 2>&1; then
    curl -fSL -o "${TMP_DIR}/cudatext.tar.xz" "${CUDATEXT_URL}"
  else
    wget -O "${TMP_DIR}/cudatext.tar.xz" "${CUDATEXT_URL}"
  fi
  
  EXTRACT_DIR="${TMP_DIR}/extracted"
  mkdir -p "${EXTRACT_DIR}"
  tar -xJf "${TMP_DIR}/cudatext.tar.xz" -C "${EXTRACT_DIR}"
  
  if [[ -x "${EXTRACT_DIR}/cudatext" ]]; then
    BIN_SRC="${EXTRACT_DIR}/cudatext"
  else
    BIN_SRC="$(find "${EXTRACT_DIR}" -type f -name 'cudatext' -perm /u+x,g+x,o+x | head -n1 || true)"
  fi

  if [[ -z "${BIN_SRC}" ]]; then
    echo "[ERROR] Could not find executable 'cudatext' in archive."
    exit 3
  fi
  
  if [[ ${EUID} -ne 0 ]]; then
    SUDO="sudo"
  else
    SUDO=""
  fi
  
  echo "[INFO] Installing to ${OPT_DIR}..."
  ${SUDO} rm -rf "${OPT_DIR}"
  ${SUDO} mkdir -p "${OPT_DIR}"
  
  
  
  ${SUDO} cp -a "${EXTRACT_DIR}/." "${OPT_DIR}/"

  if [[ -f "${OPT_DIR}/cudatext" && -x "${OPT_DIR}/cudatext" ]]; then
    ACTUAL_BIN="${OPT_DIR}/cudatext"
  elif [[ -f "${OPT_DIR}/cudatext/cudatext" && -x "${OPT_DIR}/cudatext/cudatext" ]]; then
    ACTUAL_BIN="${OPT_DIR}/cudatext/cudatext"
  else
    ACTUAL_BIN="$(find "${OPT_DIR}" -type f -name 'cudatext' -perm /u+x,g+x,o+x | head -n1 || true)"
  fi
  #
  #CUDATEXT_BIN=$(find /opt/cudatext -type f -name cudatext -executable | head -n1)
  #if [ -n "$CUDATEXT_BIN" ]; then
  #   ln -sf "$CUDATEXT_BIN" /usr/local/bin/cudatext
  #fi
  
  #${SUDO} chmod +x "${ACTUAL_BIN}" || true
  #if [[ -d "${BIN_LINK}" && ! -L "${BIN_LINK}" ]]; then
  #  ${SUDO} rm -rf "${BIN_LINK}"
  #else
  #  ${SUDO} rm -f "${BIN_LINK}"
  #fi
  #${SUDO} ln -sf "${ACTUAL_BIN}" "${BIN_LINK}"
  #${SUDO} ln -sf "${ACTUAL_BIN}" /usr/bin/cudatext 2>/dev/null || true
  # echo "[INFO] Installation complete. Checking version:"
  #"${BIN_LINK}" --version || "${BIN_LINK}" -v || echo "[WARN] Could not determine version."
  
  if [[ -f "${OPT_DIR}/cudatext" && -x "${OPT_DIR}/cudatext" ]]; then
    ACTUAL_BIN="${OPT_DIR}/cudatext"
  elif [[ -f "${OPT_DIR}/cudatext/cudatext" && -x "${OPT_DIR}/cudatext/cudatext" ]]; then
    ACTUAL_BIN="${OPT_DIR}/cudatext/cudatext"
  else
    ACTUAL_BIN="$(find "${OPT_DIR}" -type f -name 'cudatext' -perm /u+x,g+x,o+x 2>/dev/null | head -n1 || true)"
  fi

  if [[ -n "${ACTUAL_BIN}" && -f "${ACTUAL_BIN}" ]]; then
    ${SUDO} chmod +x "${ACTUAL_BIN}" || true
    if [[ -d "${BIN_LINK}" && ! -L "${BIN_LINK}" ]]; then
      ${SUDO} rm -rf "${BIN_LINK}"
    else
      ${SUDO} rm -f "${BIN_LINK}"
    fi
    ${SUDO} ln -sf "${ACTUAL_BIN}" "${BIN_LINK}"
    ${SUDO} ln -sf "${ACTUAL_BIN}" /usr/bin/cudatext 2>/dev/null || true
  fi
fi

# Install CudaText "Disk Wins" Auto-Reload Plugin & Disable ui_notif
PLUGIN_SRC="${SCRIPT_DIR}/cudatext/cuda_disk_wins"
if [[ -d "${PLUGIN_SRC}" ]]; then
  if [ "$(id -u)" -eq 0 ] && [ -n "${SUDO_USER:-}" ] && [ "${SUDO_USER}" != "root" ]; then
    TARGET_USER="${SUDO_USER}"
    TARGET_HOME="$(getent passwd "${TARGET_USER}" | cut -d: -f6)"
  else
    TARGET_USER="$(id -un)"
    TARGET_HOME="${HOME}"
  fi


  CONFIG_ROOTS=("${TARGET_HOME}/.config/cudatext")
  if [[ "$(uname -s)" == "Darwin" ]]; then
    CONFIG_ROOTS+=("${TARGET_HOME}/Library/Application Support/CudaText")
  fi

  for CFG_ROOT in "${CONFIG_ROOTS[@]}"; do
    CUDATEXT_PY_DIR="${CFG_ROOT}/py"
    CUDATEXT_SETTINGS_DIR="${CFG_ROOT}/settings"
    USER_JSON="${CUDATEXT_SETTINGS_DIR}/user.json"
    PLUGINS_INI="${CUDATEXT_SETTINGS_DIR}/plugins.ini"

    echo "[INFO] Installing CudaText plugin 'cuda_disk_wins' to ${CUDATEXT_PY_DIR}/cuda_disk_wins..."
    mkdir -p "${CUDATEXT_PY_DIR}/cuda_disk_wins"
    cp -r "${PLUGIN_SRC}/." "${CUDATEXT_PY_DIR}/cuda_disk_wins/"

    echo "[INFO] Configuring 'ui_notif: false' in ${USER_JSON}..."
    mkdir -p "${CUDATEXT_SETTINGS_DIR}"
    printf "[events]\ncuda_disk_wins=on_start2,on_open~,on_save~\n" > "${PLUGINS_INI}"

    if [[ ! -f "${USER_JSON}" ]]; then
      echo -e '{\n  "ui_notif": false\n}' > "${USER_JSON}"
    else
      python3 -c "
import json
from pathlib import Path
p = Path('${USER_JSON}')
try:
    data = json.loads(p.read_text(encoding='utf-8'))
except Exception:
    data = {}
data['ui_notif'] = False
p.write_text(json.dumps(data, indent=2), encoding='utf-8')
" 2>/dev/null || true
    fi
  done

  if [ "$(id -u)" -eq 0 ] && [ -n "${TARGET_USER}" ] && [ "${TARGET_USER}" != "root" ]; then
    chown -R "${TARGET_USER}:${TARGET_USER}" "${TARGET_HOME}/.config/cudatext" 2>/dev/null || true
  fi
fi


echo "[INFO] Done."
