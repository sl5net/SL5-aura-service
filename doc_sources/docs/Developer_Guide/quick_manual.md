## Advanced Rule Attributes

In addition to standard fields, rules can be enhanced with special options:

### `only_in_windows` (Window Title Filter)
Despite its name, this attribute is **OS-independent**. It filters rules based on the title of the currently active window.

*   **Function:** The rule is only processed if the active window title matches one of the provided patterns (Regex).
*   **Example:**
    ```python
    (
        '|', 
        r'\b(pipe|symbol)\b', 
        75, 
        {'only_in_windows': ['Terminal', 'Console', 'iTerm']}
    ),
    ```
    *In this case, the replacement only occurs if the user is working inside a terminal window.*

### `on_match_exec` (Script Execution)
Allows triggering external Python scripts when a rule matches.

*   **Syntax:** `'on_match_exec': [CONFIG_DIR / 'script.py']`
*   **Use Case:** Ideal for complex actions like API calls, file system tasks, or generating dynamic content.

