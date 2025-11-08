# SL5 Aura Rule Engine Documentation

## Advanced Rule Parameter: Overriding Safety Checks

In some scenarios (e.g., highly reliable internal commands or simple, high-confidence inputs), users might want to force the execution of post-processing steps (like `fuzzyRules`), even if the systems confidence in the initial voice recognition is low.

By default, SL5 Aura employs a safety guardrail: If the inputs changes are high (`LT_SKIP_RATIO_THRESHOLD`), post-processing tools are skipped to prevent unreliable corrections/hallucinations and for performance reasons.


To disable this safety check for a specific rule, add the identifier to the `skip_list` parameter:

```python
('command_name', r'^(regex for command)$', 95, {
     'flags': re.IGNORECASE,
     # This explicitly tells the system to ignore the ratio check and use LT
     'skip_list': ['LanguageTool', 'LT_SKIP_RATIO_THRESHOLD'],
     'on_match_exec': [CONFIG_DIR / 'script.py']
}),
