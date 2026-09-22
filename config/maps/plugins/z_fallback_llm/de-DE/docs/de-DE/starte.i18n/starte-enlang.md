> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../starte.md).*

#### Wrong (old input):

```bash
python -m config/maps/plugins/z_fallback_llm/de-DE/simulate_conversation.py
```

This works as it does without:

for   in range(5):
    PROJECT ROOT DIR = PROJECT ROOT DIR.parent
from config.maps.plugins.standard actions.get suggestions import get suggestions

Implication was


#### Correct (new input):

You must replace all slashes (`/`) with points (`.`) and omit the `.py` ending:

```bash
# Stellen Sie sicher, dass Sie im Projekt-Root-Verzeichnis ~/pr/py/STT sind
python -m config.maps.plugins.z_fallback_llm.de-DE.simulate_conversation
```

### The explanation

*   **`python -m`** means: "Execute the following element as a **module** or **package**."
*   Python modules and packages are always addressed with **point notation** (`package.subpackage.module`) because the points represent the hierarchy.
*   Your module is **`simulate_conversation`** and is in the package path **`config.maps.plugins.z_fallback_llm.de-DE`**.

If you use the corrected command, the original error message (`No module named 'config.maps'`) should be fixed because Python now correctly adds your project's root directory to the search path.
