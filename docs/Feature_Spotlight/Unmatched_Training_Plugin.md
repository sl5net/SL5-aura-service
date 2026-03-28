# Unmatched Training Plugin (`1_collect_unmatched_training`)

## Purpose

This plugin automatically collects unrecognized voice inputs and adds them
as new variants to the fuzzy map regex. This allows the system to "self-train"
over time by learning from unmatched recognition results.

## How it works

1. The `COLLECT_UNMATCHED` catch-all rule fires when no other rule matched.
2. `collect_unmatched.py` is called via `on_match_exec` with the matched text.
3. The regex in the calling `FUZZY_MAP_pre.py` is automatically extended.

## Usage

Add this catch-all rule at the end of any `FUZZY_MAP_pre.py` you want to train:
```python
from pathlib import Path
import os
PROJECT_ROOT = Path(os.environ["SL5NET_AURA_PROJECT_ROOT"])

FUZZY_MAP_pre = [
    # 1. Your rule to optimize (result first!)
    ('Blumen orchestrieren',
     r'^(Blumen giesen|Blumen gessen|Blumen essen)$', 100,
     {'flags': re.IGNORECASE}
    ),

    #################################################
    # 2. Activate this rule (place it after the rule you want to optimize)
    (f'{str(__file__)}', r'^(.*)$', 10,
     {'on_match_exec': [PROJECT_ROOT / 'config' / 'maps' / 'plugins' / '1_collect_unmatched_training' / 'collect_unmatched.py']}),
    #################################################
]
```

The label `f'{str(__file__)}'` tells `collect_unmatched.py` exactly which
`FUZZY_MAP_pre.py` to update — so the rule is portable across any plugin.

## Disabling the plugin

When you have collected enough training data, disable by either:

- Commenting out the catch-all rule
- Renaming the folder with an invalid name (e.g. add a space)
- Removing the plugin folder from the `maps` directory

## File structure
```
1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Example with catch-all rule
```

## Note

The plugin modifies `FUZZY_MAP_pre.py` at runtime. Commit the updated
file regularly to preserve collected training data.
