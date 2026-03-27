# Unmatched Training Plugin (`1_collect_unmatched_training`)

## Purpose

This plugin automatically collects unrecognized voice inputs and adds them
as new variants to the fuzzy map regex. This allows the system to "self-train"
over time by learning from unmatched recognition results.

## How it works

1. The `COLLECT_UNMATCHED` catch-all rule in `FUZZY_MAP_pre.py` fires when
   no other rule matched the voice input.
2. `collect_unmatched.py` is called via `on_match_exec` with the matched text.
3. The text is added to `unmatched_list.txt` (pipe-separated).
4. The regex in `FUZZY_MAP_pre.py` is automatically extended with the new variant.

## Disabling the plugin

When you have collected enough training data, disable this plugin by either:

- Deactivating it in the Aura settings
- Comment out the Rules in its FUZZY_MAP_pre.py
- Removing the plugin folder from the `maps` directory
- Renaming the folder with an invalid name (e.g. add a space: `a_collect unmatched_training`)

## File structure
```
config/maps/plugins/1_collect_unmatched_training/
├── collect_unmatched.py       # Plugin logic, called by engine
└── de-DE/
    └── FUZZY_MAP_pre.py       # Catch-all rule + growing regex variants
```

## Note

The plugin modifies `FUZZY_MAP_pre.py` at runtime. 
