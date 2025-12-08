# FEATURE SPOTLIGHT: Secure Private Map Loading & Auto-Packing

This document outlines the architecture for managing sensitive map plugins (e.g., client data, proprietary commands) in a way that allows **Live-Editing** while enforcing **Security Best Practices** to prevent accidental Git exposure.

---

## 1. The Concept: "Matryoshka" Security

To ensure maximum privacy while using standard tools, Aura uses a **Matryoshka (Russian Doll)** nesting strategy for encrypted archives.

1.  **Outer Layer:** A standard ZIP file encrypted with **AES-256** (via system `zip` command).
    *   *Appearance:* Contains only **one** file named `aura_secure.blob`.
    *   *Benefit:* Hides file names and directory structure from prying eyes.
2.  **Inner Layer (The Blob):** An unencrypted ZIP container inside the blob.
    *   *Content:* The actual directory structure and Python files.
3.  **Working State:** When unlocked, files are extracted to a temporary folder prefixed with an underscore (e.g., `_private`).
    *   *Security:* This folder is strictly ignored by `.gitignore`.

---

## 2. Technical Workflow

### A. The Security Gate (Start-Up)
Before unpacking anything, Aura checks `scripts/py/func/map_reloader.py` for specific `.gitignore` rules.
*   **Rule 1:** `config/maps/**/.*` (Protects key files)
*   **Rule 2:** `config/maps/**/_*` (Protects working directories)
If these are missing, the system **aborts**.

### B. Unpacking (Exception Driven)
1.  User creates a key file (e.g., `.auth_key.py`) containing the password (in plaintext or comments).
2.  Aura detects this file and the corresponding ZIP (e.g., `private.zip`).
3.  Aura decrypts the outer ZIP using the key.
4.  Aura detects the `aura_secure.blob`, extracts the inner layer, and moves the files to the working directory `_private`.

### C. Live-Editing & Auto-Packing (The Cycle)
This is where the system becomes "Self-Healing":

1.  **Edit:** You modify a file in `_private/` and save it.
2.  **Trigger:** Aura detects the change and reloads the module.
3.  **Lifecycle Hook:** The module triggers its `on_reload()` function.
4.  **SecurePacker:** A script (`secure_packer.py`) in the root of the private folder executes:
    *   It creates the inner ZIP (structure).
    *   It renames it to `.blob`.
    *   It calls the system `zip` command to encrypt it into the outer archive using the password from the `.key` file.

**Result:** Your `private.zip` is always up-to-date with your latest changes, but Git only sees the binary ZIP file change.

---

## 3. Setup Guide

### Step 1: Directory Structure
Create a folder structure like this:
```text
config/maps/private/
├── .auth_key.py          # Contains your password (e.g. # MySecretPass)
└── private_maps.zip      # The encrypted archive
```

### Step 2: The Key File (`.auth_key.py`)
Must start with a dot.
```python
# MySecretPassword123
# This file is ignored by Git.
```

### Step 3: The Packer Script (`secure_packer.py`)
Place this script inside your private map folder (before zipping it initially). It handles the encryption logic. ensure your maps call this script via the `on_reload` hook.

### Step 4: Hook Implementation
In your map files (`.py`), add this hook to trigger the backup on every save:

```python
# In your private map file
def on_reload():
    # Logic to find and execute secure_packer.py
    # ... (See Developer Guide for snippet)
```

---

## 4. Git Status & Safety

When properly set up, `git status` will **only** show:
```text
modified:   config/maps/private/private_maps.zip
```
The folder `_private_maps` and the file `.auth_key.py` are never tracked.
```

---

### 2. Neu: `docs/Developer_Guide/Lifecycle_Hooks.md`

Wir sollten einen Ordner `Developer_Guide` (oder ähnlich) anlegen, um technische Details von allgemeinen Features zu trennen.

```markdown
# Developer Guide: Plugin Lifecycle Hooks

Aura SL5 allows plugins (Maps) to define specific "Hooks" that are executed automatically when the module's state changes. This is essential for advanced workflows like the **Secure Private Map** system.

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
```

### Best Practices
1.  **Keep it fast:** Do not run long blocking tasks (like huge downloads) in the main hook. Use threads if necessary.
2.  **Idempotency:** Ensure your hook can run multiple times without breaking things (e.g., don't append to a file endlessly, rewrite it instead).
