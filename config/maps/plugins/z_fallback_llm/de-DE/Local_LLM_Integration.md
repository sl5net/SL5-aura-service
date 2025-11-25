# 🧠 SL5 Aura Hybrid Mode: Local LLM & Clipboard Integration

**Status:** Stable
**Technology:** Ollama (Llama 3.2) + File Bridge Architecture
**Privacy:** 100% Offline

## The Concept: "Architect & Intern"

Traditionally, Aura relies on deterministic rules (RegEx) – fast and precise. This is the **"Architect"**.
The **Local LLM Plugin** acts as the **"Intern"**: It handles fuzzy requests, summarizes texts, and answers general questions.

## 🛠 Architecture: The Clipboard Bridge

Due to security restrictions in Linux (Wayland/X11), background processes (like Aura) often cannot access the clipboard directly. We solved this with a **Bridge Architecture**:

1.  **The Provider (User Session):** A small shell script (`clipboard_bridge.sh`) runs in the user's session. It watches the clipboard and mirrors its content to a temporary file (`/tmp/aura_clipboard.txt`).
2.  **The Consumer (Aura):** The Python plugin reads this file. Since file access is universal, permission issues are bypassed.

---

## 🚀 Setup Guide

### 1. Install Ollama
```bash
sudo pacman -S ollama xclip wl-clipboard
sudo systemctl enable --now ollama
ollama run llama3.2
```

### 2. Setup the Bridge Script
Create `~/clipboard_bridge.sh` and make it executable:

```bash
#!/bin/bash
# Mirrors clipboard to a file in RAM
FILE="/tmp/aura_clipboard.txt"
while true; do
    if command -v wl-paste &> /dev/null; then
        wl-paste --no-newline > "$FILE" 2>/dev/null
    else
        xclip -selection clipboard -o > "$FILE" 2>/dev/null
    fi
    sleep 1.5
done
```

**Important:** Add this script to your System Autostart!

### 3. Plugin Logic (`ask_ollama.py`)

The script is located in `config/maps/plugins/z_fallback_llm/de-DE/`.
*   **Trigger:** Detects words like "Computer", "Aura", "Clipboard", "Summary".
*   **Memory:** Keeps a `conversation_history.json` to remember context (e.g., "What did I just ask?").
*   **Prompt Engineering:** Prioritizes current clipboard data over historical conversation context to prevent hallucinations.

---

## 📝 Usage Examples

1.  **Summarize Text:**
    *   *Action:* Copy a long email or website text (Ctrl+C).
    *   *Voice Command:* "Computer, summarize the text in the clipboard."

2.  **Translation/Analysis:**
    *   *Action:* Copy a code snippet.
    *   *Voice Command:* "Computer, what does the code in the clipboard do?"

3.  **General Chat:**
    *   *Voice Command:* "Computer, tell me a joke about programmers."

4.  **Reset Memory:**
    *   *Voice Command:* "Computer, forget everything." (Clears JSON history).
    
