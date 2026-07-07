# Rule Attribute: `execute_only` (Experimental, 7.7.'26 Tue)

The `execute_only` attribute is an experimental configuration option designed for rules that only trigger external scripts without modifying or replacing the input text.

## Overview
- **Type:** `bool` (e.g., `True` or `False`)
- **Primary Use Case:** Typically used in combination with `on_match_exec` to run external scripts.

## How it Works & Current Behavior
- **Speed Optimization:** (some miliseconds only) Bypasses text post-processing and text replacement routines, speeding up the immediate execution of the triggered action.
- **No Exclusion/Fall-Through Side Effect:** Setting `execute_only` to `True` does **not** prevent other matching rules from evaluating the same input text. 
- **Halting Flow:** If you need to stop subsequent rules from processing the same input text, you currently have to terminate the execution flow manually (e.g., by throwing an exception at the end of your triggered script or ruleset handler).

## Example Configuration

```python
# EXAMPLE: gather metal
('gather metal',
 r'^(gather\s*)?(met\w+|mat\w+|metall|mit|zitat|metal|matcha|günther)$',
 85,
 {
     'flags': re.IGNORECASE,
     'only_in_windows': ['0ad', '0AD', '0 a.d.', '0 a.d'],
     'on_match_exec': [CONFIG_DIR / '..' / '0ad_actions.py'],
     'execute_only': True, # Experimental: Fast execution, does not halt the rule-chain.
 }),
```

