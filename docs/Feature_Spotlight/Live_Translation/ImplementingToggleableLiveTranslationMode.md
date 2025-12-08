## Feature Spotlight: Implementing a Toggleable Live Translation Mode

Our pluginable voice assistant framework is designed for maximum flexibility. This guide demonstrates a powerful feature: a live translation mode that can be toggled on and off with a simple voice command. Imagine speaking to your assistant in German and hearing the output in Portuguese, then switching back to normal behavior instantly.

This is achieved not by changing the core engine, but by cleverly manipulating the rule configuration file itself.

### How to Use It

Setting this up involves adding two rules to your `FUZZY_MAP_pre.py` file and creating the corresponding scripts.

**1. The Toggle Rule:** This rule listens for the command to turn the translation mode on or off.

```python
# Rule to turn the translation mode on or off
    ('', r'^(portugiesisch|übersetzung|übersetzer) (aktivieren|aktiviert|aktiv|einschalten|deaktivieren|ausschalten|toggle|Dogge|doppelt)\b', 95, {
        'flags': re.IGNORECASE,
        'on_match_exec': [CONFIG_DIR / 'toggle_translation_mode.py']
    }),
```
When you say "Übersetzung einschalten" (Turn translation on), the `toggle_translation_mode.py` script is executed.

**2. The Translation Rule:** This is a "catch-all" rule that, when active, matches any text and sends it to the translation script.

```python
    # ANCHOR: The following line is controlled by the toggle script.
    # TRANSLATION_RULE
    ('', r'.+', 5, {'flags': re.IGNORECASE,'on_match_exec': [CONFIG_DIR / 'translate_from_to.py']}),
```
The key here is the `# TRANSLATION_RULE` comment. This acts as an "anchor" that the toggle script uses to find and modify the rule below it.

### How It Works: The Magic Behind the Curtain

Instead of using an internal state, this method directly edits the rule map on the file system. The `toggle_translation_mode.py` script acts as a configuration manager.

1.  **Find the Rule:** When triggered, the script reads the content of `FUZZY_MAP_pre.py`. It searches for the unique anchor comment `# TRANSLATION_RULE`.

2.  **Toggle the State:**
    *   **To Disable:** If the rule line below the anchor is active, the script adds a `#` at the beginning of the line, effectively commenting it out and disabling it.
    *   **To Enable:** If the rule line is already commented out, the script carefully removes the leading `#`, re-activating the rule.

3.  **Save and Reload:** The script saves the modified content back to `FUZZY_MAP_pre.py`. It then creates a special trigger file (e.g., `RELOAD_RULES.trigger`). The main service constantly watches for this trigger file. When it appears, the service knows its configuration has changed and reloads the entire rule map from disk, applying the change instantly.

### Design Philosophy: Advantages and Considerations

This approach of modifying the configuration file directly was chosen for its clarity and simplicity for the end-user.

#### Advantages:

*   **High Transparency:** The current state of the system is always visible. A quick look at the `FUZZY_MAP_pre.py` file immediately reveals whether the translation rule is active or commented out.
*   **No Core Engine Changes:** This powerful feature was implemented without altering a single line of the core rule-processing engine. It demonstrates the flexibility of the plugin system.
*   **Intuitive for Developers:** The concept of enabling or disabling a piece of configuration by commenting it out is a familiar, simple, and trusted pattern for anyone who has worked with code or config files.

#### Considerations:

*   **File System Permissions:** For this method to work, the assistant's process must have write permissions to its own configuration files. In some high-security environments, this might be a consideration.
