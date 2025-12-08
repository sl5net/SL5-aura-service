# 🧠 SL5 Aura: Advanced Offline LLM Integration

**Status:** Production Ready
**Engine:** Ollama (Llama 3.2 3B)
**Latency:** Instant (<0.1s on Cache Hit) / ~20s (Generation on CPU)

## 1. The "Architect & Intern" Philosophy
Aura operates on a hybrid model to balance **precision** and **flexibility**:
*   **The Architect (RegEx/Python):** Deterministic, instant execution for system commands (e.g., "Open Browser", "Volume Up").
*   **The Intern (Local LLM):** Handles fuzzy queries, summarization, and general knowledge. It is only triggered if no strict rule matches or specific keywords are used.

---

## 2. Performance Architecture

To make a local LLM usable on standard CPUs without GPU acceleration, we implemented a **3-Layer Performance Strategy**:

### Layer 1: The "Instant Mode" (Keywords)
*   **Trigger:** Words like "Instant", "Schnell", "Sofort".
*   **Logic:** Bypasses the LLM entirely. It compares user input keywords against the local SQLite database using set intersection.
*   **Latency:** **< 0.05s**

### Layer 2: The Smart Cache (SQLite)
*   **Logic:** Every prompt is hashed (SHA256). Before asking Ollama, we check `llm_cache.db`.
*   **Feature "Active Variation":** Even if a cache hit exists, the system sometimes (20% chance) generates a *new* variant to learn different phrasings for the same question. Ideally, we store ~5 variants per question.
*   **Feature "Semantic Hashing":** For long questions (>50 chars), we use the LLM to extract keywords first (e.g., "installation guide") and hash those instead of the full sentence. This matches "How do I install?" with "Installation instructions please".
*   **Latency:** **~0.1s**

### Layer 3: The API Generation (Fallback)
*   **Logic:** If no cache exists, we call the Ollama API (`http://localhost:11434/api/generate`).
*   **Optimization:**
    *   **Hard Limits:** `num_predict=60` forces the model to stop after ~40 words.
    *   **Input Piping:** Large texts (README) are passed via STDIN to avoid OS argument limits.
*   **Latency:** **~15-25s** (CPU dependent)

---

## 3. System Grounding (Anti-Hallucination)

Generic LLMs tend to invent GUI elements (Buttons, Menus). We inject a strict **`AURA_TECH_PROFILE`** into every system prompt:

1.  **No GUI:** Aura is a headless CLI service.
2.  **No Config Files:** Logic is Python code, not `.json`/`.xml`.
3.  **Triggers:** External control works via file creation (`touch /tmp/sl5_record.trigger`), not APIs.
4.  **Installation:** Takes 10-20 mins due to 4GB model downloads (prevents "It installs in 3 seconds" lies).

---

## 4. The Clipboard Bridge (Linux Security)

Background services (systemd) cannot access the X11/Wayland clipboard directly due to security isolation.
*   **Solution:** A user-session script (`clipboard_bridge.sh`) mirrors clipboard content to a RAM-disk file (`/tmp/aura_clipboard.txt`).
*   **Aura:** Reads this file, bypassing all permission issues.

---

## 5. Self-Learning (Cache Warming)

We provide a `warm_up_cache.py` script.
1.  It reads the project `README.md`.
2.  It asks the LLM to invent likely user questions about the project.
3.  It simulates these questions against Aura to pre-fill the database.
