
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

TARGET_DIR="${PROJECT_ROOT}/README.i18n"
CACHE_FILE="${SCRIPT_DIR}/translation_cache.json"
SEARCH_PHRASE="Define exactly what your voice does"

echo "Scanning for untranslated files in ${TARGET_DIR}..."

if [[ ! -d "${TARGET_DIR}" ]]; then
    echo "Directory not found: ${TARGET_DIR}"
    exit 0
fi

FOUND_COUNT=0
while IFS= read -r file; do
    if grep -Fq "${SEARCH_PHRASE}" "${file}"; then
        echo "Removing untranslated file: ${file}"
        rm -f "${file}"
        FOUND_COUNT=$((FOUND_COUNT + 1))
    fi
done < <(find "${TARGET_DIR}" -type f -name "*.md")

echo "Deleted ${FOUND_COUNT} untranslated file(s)."

# if [[ -f "${CACHE_FILE}" ]]; then
#     echo "Removing stale translation cache: ${CACHE_FILE}"
#     rm -f "${CACHE_FILE}"
# fi

# echo "Cleanup completed successfully."
