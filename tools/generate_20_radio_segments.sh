#!/bin/bash
# mass_generate_radio.sh - Generates multiple radio segments for the SL5-aura-service

echo "maybe use:"
echo "./tools/generate_20_radio_segments.sh --demo ; kate /tmp/sl5_aura/radio_output.txt"

# --- CONFIGURATION ---
PROJECT_DIR="$HOME/projects/py/STT"
PYTHON_SCRIPT="config/maps/plugins/z_fallback_llm/de-DE/radio_deep_dive.py"
VENV_PATH=".venv/bin/activate"
ITERATIONS=200

logg_of_runs = """
start:
2026-0402-2318
"""


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

# starten anleigung:
# python3 "$PYTHON_SCRIPT" $DEMO_FLAG > /tmp/sl5_aura/radio_output.txt 2>/dev/null
# oder
# ./generate_20_radio_segments.sh --demo; kate /tmp/sl5_aura/radio_output.txt


DEMO_FLAG=""
if [ "$1" = "--demo" ]; then
    DEMO_FLAG="--demo"
fi

> /tmp/sl5_aura/radio_output.txt

# ~/projects/py/TTS/.venv/bin/python ~/projects/py/TTS/speak_server.py
# source ~/projects/py/TTS/.venv/bin/activate && cd ~/projects/py/TTS && python speak_server.py
(cd ~/projects/py/TTS && .venv/bin/python speak_server.py) &
sleep 3


for ((i=1; i<=ITERATIONS; i++))
do
    echo "[$i/$ITERATIONS] Running generator..."
    # python3 "$PYTHON_SCRIPT"

    python3 "$PYTHON_SCRIPT" $DEMO_FLAG >> /tmp/sl5_aura/radio_output.txt 2>/dev/null

    # Optional: Short sleep to let the system / Ollama cool down
    sleep 2
    echo "----------------------------------------------------"
done

echo "--- Finished! ---"
# Check final count in DB
sqlite3 config/maps/plugins/z_fallback_llm/de-DE/llm_cache.db "SELECT COUNT(*) FROM prompts WHERE keywords = 'radio_deep_dive';"

# kill $!
