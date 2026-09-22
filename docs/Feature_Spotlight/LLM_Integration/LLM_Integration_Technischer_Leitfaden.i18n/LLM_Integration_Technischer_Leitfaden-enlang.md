> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../LLM_Integration_Technischer_Leitfaden.md).*

# 🧠 SL5 Aura: Advanced Offline LLM Integration

**Status:** Ready for production
**Engine:** Ollama (Llama 3.2 3B)
**Latency:** Instant (<0.1s on cache hit) / ~20s (generation on CPU)

## 1. The "Architect & Intern" Philosophy
Aura uses a hybrid model to combine **precision** and **flexibility**:
*   **The Architect (RegEx/Python):** Deterministic, immediate execution for system commands ("Open browser", "Louder").
*   **The Intern (Local LLM):** Handles vague requests, summaries, and general knowledge. Only becomes active when no strict rule applies.

---

## 2. Performance Architecture

To make a local LLM usable on regular CPUs (without a GPU), we rely on a **3-step strategy**:

### Level 1: The "Instant Mode" (Keywords)
*   **Trigger:** Words like "Instant", "Quick", "Immediate".
*   **Logic:** Completely bypasses the LLM. Directly compares keywords from the input with the SQLite database.
*   **Latency:** **< 0.05s**

### Level 2: The Intelligent Cache (SQLite)
*   **Logic:** Every prompt is hashed (SHA256). Before each request to Ollama, the `llm_cache.db` is checked.
*   **Feature "Active Variation":** Even with a cache hit, the system sometimes (20% chance) proactively generates a *new* response variant. Goal: ~5 variants per question for more liveliness.
*   **Feature "Semantic Hashing":** For long questions (>50 characters), the LLM first extracts keywords (e.g. "installation instructions") and hashes them. So "How do I install it?" and "Installation help please" are recognized as identical.
*   **Latency:****~0.1s * *

### Level 3: The API Generation (Fallback)
*   **Logic:** If no cache exists, we call the Ollama API (`http://localhost:11434/api/generate`).
*   **Optimization:**
    *   **Hard Limits:** `num_predict=60` forces the model to stop after about 40 words.
    *   **Input Piping:** Large texts (README) are passed via STDIN to bypass operating system argument limits.
*   **Latency:** **~15-25s** (depending on CPU)

---

System Grounding (Anti-Hallucination)

Generic LLMs often invent GUIs (buttons, menus). We inject the strict **`AURA_TECH_PROFILE`** at each call:

1.  **No GUI:** Aura is a headless CLI service.
2.  **No config files:** Logic is pure Python code, not `.json`/`.xml`.
3.  **Trigger:** External control is via file system events (`touch /tmp/sl5_record.trigger`), not APIs.
4.  **Installation:** Takes real 10-20 minutes due to 4GB model downloads (prevents false promises).

---

## 4. The Clipboard Bridge (Linux Security)

Background services (systemd) often cannot access the clipboard (X11/Wayland) for security reasons.
*   **Solution:** A script in the user session (`clipboard_bridge.sh`) mirrors the content into a RAM disk file (`/tmp/aura_clipboard.txt`).
*   **Aura:** Reads this file and thus bypasses all rights issues.

---

## 5. Self-Learning (Cache Warming)

We use the script `warm_up_cache.py`:
1.  It reads the `README.md` of the project.
2.  It instructs the LLM to come up with likely user questions.
3.  It asks these questions to Aura in order to automatically populate the database.
