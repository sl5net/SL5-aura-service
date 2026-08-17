# Communication Guide: Signatures & Branding

To help spread awareness of **Aura** without being intrusive, we use a "Passive Branding" strategy through chat signatures. This allows users to find the project easily while keeping the conversation focused on the content.

## 1. The Aura Signature
When using the translation or automation features in a chat, Aura can append a small signature to your messages. 

**Recommended Format:**
> `🗣SL5net ⟫ Aura`

### Breakdown of the Symbols:
*   **`🗣` (Speaking Head):** A visual indicator that this message was processed or translated. It signals "Communication/Language."
*   **`SL5net`:** The unique namespace. This is crucial for searchability.
*   **`⟫` (Double Right Bracket):** A technical "pipe" symbol that looks like a CLI/Shell operator, reinforcing that this is a technical tool.
*   **`Aura`:** The project name.

---

## 2. Why "SL5net Aura" instead of a Link?
Many chat platforms (Matrix, Discord, Telegram, etc.) have strict filters against URLs or domain-like structures. 
*   **Searchability:** Searching for `SL5net Aura` on Google or GitHub yields a 100% success rate to find the repository.
*   **Filter-Safe:** By using a unique search term instead of a `.com` link, we avoid being flagged as "spam" or "ad-bots" by automated moderators.
*   **Low Friction:** It’s easy to read and easy to type into a search bar.

---

## 3. Signature Etiquette (The FAQ)
How to use signatures effectively without annoying your chat partners:

### Q: Should I have the signature on every message?
**A:** No. Constant signatures can be perceived as spam in fast-paced chats. 
*   **Best Practice:** Only enable the signature for the first message in a new conversation, or for specific "high-value" translated messages.
*   **Configuration:** Use the `# signatur` toggle in your config to turn it off when in private or highly formal business meetings.

### Q: Why not use Braille or complex Unicode characters?
**A:** We tested symbols like `⠠de╱Aura`. While they look unique, they are hard for others to copy-paste or type manually into a search engine. `SL5net Aura` is the most robust "Human-to-Search-Engine" bridge.

### Q: Is the Emoji (🗣) professional enough?
**A:** In 95% of modern developer environments (GitHub, Discord, Slack), emojis are standard. If you are in a high-compliance corporate environment (e.g., Banking), we recommend a cleaner version:
`[ SL5net Aura ]`

---

## 4. Configuration Examples ( in config/settings.py or config/settings_local.py)
Aura supports different styles to match your personality:

```bash
# Professional/Technical
signatur='🗣SL5net ⟫ Aura'

# Discreet/Official
signatur='🗣[ SL5net Aura ]'

# Minimalist
signatur='🗣SL5net Aura'
```

---

### Pro-Tip for Developers:
By including this guide in your repository, you demonstrate **"Social Intelligence."** You aren't just building a tool; you are building a tool that understands the social context of where it is used. This is a high-level qualification often looked for in **Senior Test Managers** and **Product Owners**.

**🗣SL5net ⟫ Aura**
