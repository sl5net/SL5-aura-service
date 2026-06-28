#!/usr/bin/env bash
# autosync.sh
set -euo pipefail

# Konfiguration: Intervall in Sekunden (kann per ENV überschrieben werden)
INTERVAL="${INTERVAL:-10}"
COMMIT_MESSAGE="${COMMIT_MESSAGE:-WIP}"

while true; do
    git add .
    if git diff --cached --quiet; then
      echo "Nach 'git add' nichts zum Committen."
    else
      if git commit -m "${COMMIT_MESSAGE}"; then
        echo "Commit erfolgreich. Versuche zu pushen..."
        if git push; then
          echo "Push erfolgreich."
        else
          echo "Push fehlgeschlagen. Bitte manuell prüfen."
        fi
      else
        echo "Commit fehlgeschlagen."
      fi
    fi
  sleep "${INTERVAL}"
done
