#!/bin/bash
# mass_generate_radio.sh - Generates multiple radio segments for the SL5-aura-service

# --- CONFIGURATION ---
PROJECT_DIR="$HOME/projects/py/STT"
PYTHON_SCRIPT="config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py"
VENV_PATH=".venv/bin/activate"
ITERATIONS=2

# Navigate to project directory
cd "$PROJECT_DIR" || { echo "Directory not found"; exit 1; }

# Activate virtual environment
if [ -f "$VENV_PATH" ]; then
    source "$VENV_PATH"
else
    echo "Virtual environment not found at $VENV_PATH"
    exit 1
fi

echo "--- Starting Mass Generation: $ITERATIONS Segments ---"

for ((i=1; i<=ITERATIONS; i++))
do
    echo "[$i/$ITERATIONS] Running generator..."
    python3 "$PYTHON_SCRIPT"

    # Optional: Short sleep to let the system / Ollama cool down
    sleep 2
    echo "----------------------------------------------------"
done

echo "--- Finished! ---"
# Check final count in DB
sqlite3 config/maps/plugins/z_fallback_llm/de-DE/llm_cache.db "SELECT COUNT(*) FROM prompts WHERE keywords = 'radio_deep_dive';"
