#!/usr/bin/env bash

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

FALLBACK_URL="https://downloads.sourceforge.net/project/cudatext/release/1.232.2.1/cudatext-linux-gtk2-amd64-1.232.2.1.tar.xz"

cleanup() {
  local rc=$?
  [[ -n "${TMP_DIR:-}" && -d "${TMP_DIR}" ]] && rm -rf "${TMP_DIR}"
  return "${rc}"
}
trap cleanup EXIT

if command -v "${CANDIDATE_NAME}" >/dev/null 2>&1; then
  echo "[INFO] ${CANDIDATE_NAME} is already installed: $(command -v "${CANDIDATE_NAME}")"
  exit 0
fi

# Detect architecture
ARCH="$(uname -m)"
case "${ARCH}" in
  x86_64|amd64) TAR_NAME_PREFIX="cudatext-linux-gtk2-amd64" ;;
  aarch64|arm64) TAR_NAME_PREFIX="cudatext-linux-gtk2-arm64" ;; 
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
${SUDO} mkdir -p "${OPT_DIR}"
${SUDO} cp -a "${EXTRACT_DIR}/." "${OPT_DIR}/"

${SUDO} chmod +x "${OPT_DIR}/cudatext" || true
${SUDO} ln -sf "${OPT_DIR}/cudatext" "${BIN_LINK}"

echo "[INFO] Installation complete. Checking version:"
"${BIN_LINK}" --version || "${BIN_LINK}" -v || echo "[WARN] Could not determine version."

echo "[INFO] Done."
