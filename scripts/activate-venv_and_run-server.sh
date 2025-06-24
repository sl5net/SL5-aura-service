#!/bin/bash

# Exit immediately if a command fails
set -e

# This line is the key: It finds the absolute path of the directory
# where the script itself is located (i.e., the 'scripts' directory).
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# The project's root directory is one level above the script's directory.
PROJECT_ROOT="$SCRIPT_DIR/.."

echo "Activating virtual environment at '$PROJECT_ROOT/venv'..."
source "$PROJECT_ROOT/vosk-tts/bin/activate"

echo "Starting Python server from '$PROJECT_ROOT'..."
# We run the python script using its absolute path to be safe
python3 "$PROJECT_ROOT/dictation_service.py"

echo "Server has stopped."
