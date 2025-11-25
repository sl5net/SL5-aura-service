# 🧠 SL5 Aura Hybrid Mode: Local LLM Integration

**Status:** Experimental / Stable
**Technology:** Ollama (Llama 3.2) + Python Subprocess
**Privacy:** 100% Offline

## The Concept: "Architect & Intern"

Traditionally, Aura relies on deterministic rules (RegEx) – fast, precise, and predictable. This is the **"Architect"**. However, sometimes the user wants to ask something "fuzzy" or creative, like *"Tell me a joke"* or *"Summarize this text"*.

This is where the **Local LLM Plugin** comes in (the **"Intern"**):
1.  **Aura (RegEx)** first checks all strict commands ("Turn on lights", "Open App").
2.  If nothing matches **AND**/ **OR** a specific trigger word (e.g., "Aura ...") is detected, the fallback rule activates.
3.  The text is sent to a local AI model (Ollama).
4.  The response is sanitized and output via TTS or text typing.

---

## 🛠 Prerequisites

The plugin requires a running instance of [Ollama](https://ollama.com/) operating locally on the machine.

```bash
# Installation (Arch/Manjaro)
sudo pacman -S ollama
sudo systemctl enable --now ollama

# Download model (Llama 3.2 3B - only ~2GB, very fast)
ollama run llama3.2
```

---

## 📂 Structure & Load Order

The plugin is intentionally placed in the folder `z_fallback_llm`.
Since Aura loads plugins **alphabetically**, this naming ensures that the LLM rule is loaded **last**. It serves as a "safety net" for unrecognized commands.

**Path:** `config/maps/plugins/z_fallback_llm/de-DE/`

### 1. The Map (`FUZZY_MAP_pre.py`)

We use a **high score (100)** and a trigger word to force Aura to hand over control to the script.

```python
import re
from pathlib import Path
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    # Trigger: "Aura" + any text
    ('ask_ollama', r'^\s*(Aura|Aurora|Laura)\s+(.*)$', 100, {
        'flags': re.IGNORECASE,
        # 'skip_list': ['LanguageTool'], # Optional: Performance boost
        'on_match_exec': [CONFIG_DIR / 'ask_ollama.py']
    }),
]
```

### 2. The Handler (`ask_ollama.py`)

This script communicates with the Ollama CLI.
**Important:** It contains a `clean_text_for_typing` function. Raw LLM outputs often contain emojis (😂, 🚀) or special characters that can crash tools like `xdotool` or legacy TTS systems.

```python
# Snippet from ask_ollama.py
def execute(match_data):
    # ... (Regex group extraction) ...
    
    # System prompt for short answers
    system_instruction = "Answer in German. Max 2 sentences. No emojis."
    
    # Subprocess call (blocks briefly, note the timeout!)
    cmd = ["ollama", "run", "llama3.2", full_prompt]
    result = subprocess.run(cmd, capture_output=True, ...)

    # IMPORTANT: Sanitize output for system stability
    return clean_text_for_typing(result.stdout)
```

---

## ⚙️ Customization Options

### Changing the Trigger
Modify the RegEx in `FUZZY_MAP_pre.py` if you don't want to use "Aura" as the wake word.
*   Example for a true Catch-All (everything Aura doesn't know): `r'^(.*)$'` (Caution: Adjust the score!)

### Swapping the Model
You can easily swap the model in `ask_ollama.py` (e.g., to `mistral` for more complex logic, though it requires more RAM).
```python
cmd = ["ollama", "run", "mistral", full_prompt]
```

### System Prompt (Persona)
You can give Aura a personality by adjusting the `system_instruction`:
> "You are a sarcastic assistant from a Sci-Fi movie."

---

## ⚠️ Known Limitations

1.  **Latency:** The very first request after boot might take 1-3 seconds as the model loads into RAM. Subsequent requests are faster.
2.  **Conflicts:** If the RegEx is too broad (`.*`) without a proper folder structure, it might swallow standard commands. The alphabetical ordering (`z_...`) is essential.
3.  **Hardware:** Requires approx. 2GB of free RAM for Llama 3.2.
