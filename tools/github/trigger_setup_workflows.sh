#!/usr/bin/env bash
#
# tools/github/trigger_setup_workflows.sh
# Trigger setup workflows via GitHub CLI workflow_dispatch on the current branch.
#

set -euo pipefail

if ! command -v gh &> /dev/null; then
    echo "[ERROR] GitHub CLI 'gh' is not installed or not in PATH."
    exit 1
fi

CURRENT_BRANCH=$(git branch --show-current)
if [ -z "${CURRENT_BRANCH}" ]; then
    echo "[ERROR] Could not determine current git branch."
    exit 1
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PROJECT_ROOT=$(cd "${SCRIPT_DIR}/../.." && pwd)
WORKFLOWS_DIR="${PROJECT_ROOT}/.github/workflows"

if [ ! -d "${WORKFLOWS_DIR}" ]; then
    echo "[ERROR] Workflows directory not found: ${WORKFLOWS_DIR}"
    exit 1
fi

PATTERN="${1:-*setup*}"
echo "[INFO] Searching for workflows matching pattern '${PATTERN}' in ${WORKFLOWS_DIR}..."
echo "[INFO] Target branch: ${CURRENT_BRANCH}"

MATCHED_FILES=$(find "${WORKFLOWS_DIR}" -maxdepth 1 -type f \( -name "${PATTERN}.yml" -o -name "${PATTERN}.yaml" \) | sort)

if [ -z "${MATCHED_FILES}" ]; then
    echo "[WARNING] No workflow files matched pattern '${PATTERN}'."
    exit 0
fi

for file_path in ${MATCHED_FILES}; do
    filename=$(basename "${file_path}")
    echo "[INFO] Triggering workflow: ${filename} on branch '${CURRENT_BRANCH}'..."
    gh workflow run "${filename}" --ref "${CURRENT_BRANCH}" || echo "[WARNING] Failed to trigger ${filename}"
done

echo "[INFO] All matching workflows triggered."
