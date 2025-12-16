Aura SL5 Hooks: Added 
on_folder_change() and 
on_reload() to trigger logic after hot-reloads. Use this to "daisy chain" execution to parent scripts like secure_packer.py for complex packages.

# Developer Guide: Plugin Lifecycle Hooks

Aura SL5 allows plugins (Maps) to define specific "Hooks" that are executed automatically when the module's state changes. This is essential for advanced workflows like the **Secure Private Map** system.

## The `on_folder_change` hook  Hook

Implemented `on_folder_change` hook detection. The reloader now scans up the directory

## The `on_reload()` Hook

The `on_reload()` function is an optional function you can define in any Map module.

### Behavior
*   **Trigger:** Executed immediately after a module is successfully **hot-reloaded** (file modification + voice trigger).
*   **Context:** Runs within the main application thread.
*   **Safety:** Wrapped in a `try/except` block. Errors here will be logged but will **not crash** the application.

### Usage Pattern: The "Daisy Chain"
For complex packages (like Private Maps), you often have many sub-files, but only one central script (`secure_packer.py`) should handle the logic.

You can use the hook to delegate the task upwards:

```python
# Example: Delegating logic to a parent script
import importlib.util
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def on_reload():
    """
    Searches for 'secure_packer.py' in parent directories and executes it.
    """
    logger.info("🔄 Map modified. Triggering packer...")
    
    current_path = Path(__file__).resolve()
    search_dir = current_path.parent
    packer_script = None

    # Search upwards (max 4 levels)
    for _ in range(4):
        candidate = search_dir / "secure_packer.py"
        if candidate.exists():
            packer_script = candidate
            break
        if search_dir.name in ["maps", "config"]: break
        search_dir = search_dir.parent

    if packer_script:
        try:
            # Dynamic Import & Execution
            spec = importlib.util.spec_from_file_location("packer_dyn", packer_script)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'on_reload'):
                module.on_reload()
        except Exception as e:
            logger.error(f"❌ Failed to run packer: {e}")
