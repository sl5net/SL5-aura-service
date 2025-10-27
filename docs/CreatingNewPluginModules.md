## Creating New Plugin Modules

Our framework uses a powerful auto-discovery system to load rule modules. This makes adding new sets of commands simple and clean, without needing to manually register every new component. This guide explains how to create, structure, and manage your own custom modules.

### The Core Concept: Folder-Based Modules

A module is simply a folder within the `config/maps/` directory. The system automatically scans this directory and treats each subfolder as a loadable module.

### Step-by-Step Guide to Creating a Module

Follow these steps to create a new module, for example, to hold macros for a specific game.

**1. Navigate to the Maps Directory**
   All rule modules reside in the `config/maps/` folder of the project.

**2. Create Your Module Folder**
   Create a new folder. The name should be descriptive and use underscores instead of spaces (e.g., `my_game_macros`, `custom_home_automation`).

**3. Add Language Subfolders (Critical Step)**
   Inside your new module folder, you must create subfolders for each language you intend to support.

   *   **Naming Convention:** The names of these subfolders **must be valid language-locale codes**. The system uses these names to load the correct rules for the active language.
   *   **Correct Examples:** `de-DE`, `en-US`, `en-GB`, `pt-BR`
   *   **Warning:** If you use a non-standard name like `german` or `english_rules`, the system will either ignore the folder or treat it as a separate, non-language-specific module.

**4. Add Your Rule Files**
   Place your rule files (e.g., `FUZZY_MAP_pre.py`) inside the appropriate language subfolder. The easiest way to start is to copy the contents of an existing language module folder to use as a template.

### Example Directory Structure

```
config/
└── maps/
    ├── standard_actions/      # An existing module
    │   ├── de-DE/
    │   └── en-US/
    │
    └── my_game_macros/        # <-- Your new custom module
        └── de-DE/             # <-- Language-specific rules
            └── FUZZY_MAP_pre.py

        ├── __init__.py        # <-- Important: This Empty File must be in every Folders!!
            
```

### Managing Modules in the Configuration

The system is designed to require minimal configuration.

#### Enabling Modules (The Default)

Modules are **enabled by default**. As long as a module folder exists in `config/maps/`, the system will find it and load its rules. **You do not need to add an entry to your settings file to enable a new module.**

#### Disabling Modules

To disable a module, you must add an entry for it in the `PLUGINS_ENABLED` dictionary within your settings file and set its value to `False`.

**Example (`config/settings.py`):**
```python
# A dictionary to explicitly control the state of modules.
# The key is the path to the module relative to 'config/maps/'.
PLUGINS_ENABLED = {
    "empty_all": False,

    # This module is explicitly enabled.
    "git": True,

    # This module is also enabled. Second Parameter is per default True. Not False means True.
    # "wannweil": False,

    # This module is explicitly disabled.
    "game": False,

    # This module is disabled by other rule
    "game/game-dealers_choice": True,

    # This module is disabled by other rule
    "game/0ad": True,
}


```
### Important Design Notes

*   **Default Behavior: No Entry Equals `True`**
    If a module is not listed in the `PLUGINS_ENABLED` dictionary, it is considered **active** by default. This design keeps the configuration file clean, as you only need to list the exceptions.

*   **Shorthand for Enabling**
    Your configuration system also understands that listing a module key without a value implies it is enabled. For example, adding `"wannweil"` to the dictionary is the same as adding `"wannweil": True`. This provides a convenient shorthand for enabling modules.

*   **Disabling Parent Modules:** The intended behavior is that disabling a parent module should          
    automatically disable all of its child modules and language subfolders. For example, setting `"standard_actions": False` should prevent both `de-DE` and `en-US` from loading. (27.10.'25 Mon)
    
*   **goal**
    The goal is to enhance this system further. For example, providing a way for child module settings to be respected even if the parent is disabled, or introducing more complex inheritance rules. (27.10.'25 Mon)

