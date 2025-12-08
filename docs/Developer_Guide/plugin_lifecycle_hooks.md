# Plugin Lifecycle Hooks

Aura SL5 supports lifecycle hooks that allow plugins (Maps) to execute specific logic automatically when their state changes.

## The `on_reload()` Hook

The `on_reload()` function is a special optional function that you can define inside any Plugin Map (`.py`).

### Behavior
*   **Trigger:** This function is executed **immediately after** the module has been successfully hot-reloaded (detected file change + voice trigger).
*   **Context:** It runs within the main application flow.
*   **Scope:** It is **NOT** executed during the initial system startup (cold start). It is strictly for *re*-loading scenarios.

### Use Cases
*   **Security:** Automatically re-encrypt or re-zip sensitive files after editing.
*   **State Management:** Resetting global counters or clearing specific caches.
*   **Notification:** Logging specific debug info to verify a change was applied.

### Technical Details & Safety
*   **Error Handling:** The execution is wrapped in a `try/except` block. If your `on_reload` function crashes (e.g., `DivisionByZero`), it will log an error (`❌ Error executing on_reload...`) but **will not crash Aura**.
*   **Performance:** The function runs synchronously. Avoid long-running tasks (like large downloads) directly in this function, as they will briefly block the voice command processing. For heavy tasks, spawn a thread.

### Example Code

```python
# config/maps/plugins/my_custom_plugin/de-DE/my_map.py

def execute(data):
    # Standard voice command logic
    pass

# --- LIFECYCLE HOOK ---
def on_reload():
    """
    Called automatically when this file is modified and Aura reloads it.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    logger.info("🔄 Plugin updated! Performing cleanup tasks...")
    
    # Example: Validate a config file exists
    # validate_config()
