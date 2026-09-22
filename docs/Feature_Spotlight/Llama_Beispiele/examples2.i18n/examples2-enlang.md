> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../examples2.md).*

Don't underestimate the 'Little One' (Llama 3.2 3B). Especially because it is **local, offline, and fast**, it is more powerful for Aura than a huge ChatGPT that needs the Internet.

Here are **5 concrete scenarios** that you can use immediately with your current setup:

The "Text-Polierer" (My favorite for dictation)
You often dictate quickly and unstructured. The LLM can smooth this out before it goes into the email.
*   **You say:*** "Aura formulate this politely: I don't have time for the meeting, postpone." *
*   **LLM makes:***"Dear ladies and gentlemen, unfortunately I can not attend the planned date". Would a postponement be possible? *
*   **Why:** RegEx cannot do grammar. The LLM already.

### 2. The "Linux Cheat Sheet"
Instead of googling or reading `man pages`, you just ask. The model is trained on code.
*   **You say:** *"Aura how do I find all files larger than 100 MB on Linux?"*
*   **LLM does:** `find / -type f -size +100M`
*   **Why:** You stay in the flow without switching the window.

Extract structured data (your "restaurant idea")
This is the king’s discipline. You can use the LLM to convert soft language into hard data for aura scripts.
*   **You say:*** "Aura order pizza salami but spicy and without onions." *
*   **LLM (with JSON prompt):** `{"produkt": "Pizza Salami", "mods": ["+scharf", "-Zwiebeln"]}`
*   **Advantage:** Your Python script does not have to parse thousands of variants of "without", "no", "please do not". This is done by the LLM.

### 4. Offline summaries
If you have a long text on the clipboard (or have dictated):
*   **You say:** *"Aura summarize the following text in three bullet points: [Text]"*
*   **LLM does:** Delivers you the essence instantly.

### 5. The "Creative Fallback"
If you are missing a word or need an idea.
*   **You say:** *"Aura, name 5 synonyms for 'development'."*
*   **LLM does:** *"Progress, evolution, unfolding, genesis, elaboration."*

---

### Strategic tip for the future

You now have a **"intelligence soft"**:
1.  **RegEx** for everything that needs to sit 100% (lights on, start app, navigate). **(Quick and safe)**
2.  **Llama** for everything that needs to be flexible (writing texts, answering questions). **(Smart & Adaptive)**

This is exactly the USP that OVOS or Siri often does not do well: the combination of absolute control (your RegEx) and AI magic (Llama), and completely without the cloud.
