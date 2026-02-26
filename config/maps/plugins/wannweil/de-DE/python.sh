#!/usr/bin/env bash
set -euo pipefail

# maybe add to zshrc:
## Prefer local ./python.sh when you type "python.sh"
## Put this in ~/.zshrc and then run: . ~/.zshrc
#function 'python.sh'() {
#  # If first argument looks like --help or -h just forward to local script if exists
#  if [[ -x ./python.sh ]]; then
#    # exec replaces the shell process with the script (so signals/exit behave naturally)
#    exec ./python.sh "$@"
#  else
#    # No local script: try running whatever python.sh would normally do (if any)
#    # Use command to bypass shell function/alias lookups
#    command python.sh "$@"
#  fi
#}
#
#python_local() {
#  if [[ -x ./python.sh ]]; then
#    exec ./python.sh "$@"
#  else
#    command python.sh "$@"
#  fi
#}
## Create an alias name without a dot (dots are awkward in function names)
#alias python.sh=python_local





# Usage: ./run.sh [path-to-project|path-to-script]
# default: current repo structure relative path
DEFAULT_DIR="$(cd "$(dirname "$0")" && pwd)"
# If called with an argument that is a .py file, use it; if a dir, use check_trash.py inside it
TARGET="${1:-$DEFAULT_DIR}"
if [[ -f "$TARGET" && "$TARGET" == *.py ]]; then
  SCRIPT="$TARGET"
  PROJDIR="$(dirname "$SCRIPT")"
else
  PROJDIR="${TARGET%/}"
  SCRIPT="$PROJDIR/check_trash.py"
fi

VENV_PY="../../../../../.venv/bin/python"

VENV_PY=".venv/bin/python"

if [[ -x "$VENV_PY" ]]; then
  exec "$VENV_PY" "$SCRIPT" "${@:2}"
else
  echo "Warning: virtualenv python not found at $VENV_PY, falling back to system python" >&2
  exec python3 "$SCRIPT" "${@:2}"
fi
