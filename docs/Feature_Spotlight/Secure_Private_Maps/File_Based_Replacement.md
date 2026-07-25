# FEATURE SPOTLIGHT: File-Based Rule Replacements

This document describes how to keep sensitive values (passwords, API keys, tokens)
out of `FUZZY_MAP_pre` / `FUZZY_MAP` source code and Git history by loading the
`replacement` text from a separate file at runtime instead of hardcoding it.

This is especially useful during livestreams or screen shares, where the map
source code itself may be visible, but the referenced file is not.

---

## 1. The Concept

Normally, the `replacement` field of a rule is the literal output text:

```python
('my-secret-value', r'^(trigger)$', 85, {'command_flags': re.IGNORECASE})
```

With file-based replacement enabled, a `replacement` value that starts with a
configured prefix (by default `-` or `.`) is instead treated as a **filename**.
Aura resolves that filename relative to the plugin's own directory, reads its
content, and uses that content as the replacement text.

```python
('-api_key.txt', r'^(show api key)$', 85, {'command_flags': re.IGNORECASE})
```

If `api_key.txt` exists next to the plugin's `FUZZY_MAP_pre.py`, its (stripped)
content is used as the replacement. If the file does not exist, the literal
string `-api_key.txt` is returned instead (fail-safe: no accidental leakage of
"file not found" as usable text, and no crash).

---

## 2. Settings

Configured in `config/settings.py` (or `config/settings_local.py` for local
overrides):

| Setting | Type | Default | Description |
|---|---|---|---|
| `FILE4REPLACEMENT_USE` | `bool` | `True` | Master switch for the whole feature. If `False`, `replacement` is always used literally. |
| `FILE4REPLACEMENT_ALLOWED_PREFIXES` | `tuple[str]` | `('-', '.')` | `replacement` values must start with one of these prefixes to trigger a file lookup. Empty/`None` = any value not starting with a letter is treated as a potential filename. |
| `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` | `bool` | `False` | If `True`, allows resolving files outside the plugin's own directory (e.g. absolute paths, or `../` sequences). See Security section below. |
| `FILE4REPLACEMENT_DENY_PREFIXES` | `tuple[str]` | e.g. `('/etc', '/proc', '/dev', '/var/lib', '/root', 'C:\\Windows', 'C:\\Program Files')` | Resolved absolute paths starting with any of these are **always** rejected, regardless of `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL`. Hard security boundary against system directories. |

---

## 3. Path Resolution

The file is resolved as follows:

1. The plugin's `source_path` (recorded automatically by the map loader) is
   joined against `PROJECT_ROOT` (read from the `SL5NET_AURA_PROJECT_ROOT`
   environment variable) to get the plugin's directory.
2. The `replacement` value is joined onto that directory.
3. Unless `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` is `True`, the resolved path
   must stay inside the plugin's directory, or the lookup is rejected.
4. Regardless of the above, any resolved path starting with an entry in
   `FILE4REPLACEMENT_DENY_PREFIXES` is always rejected.
5. If the file exists, its stripped content is returned. Otherwise, the
   original `replacement` string is returned unchanged.

---

## 4. Security Notes

- Only enable `FILE4REPLACEMENT_ALLOW_PATH_TRAVERSAL` if you understand the
  implications: it allows any user who can edit a `FUZZY_MAP_pre` file (e.g.
  via an online map editor) to read arbitrary files that the Aura process can
  access, and have their content surface as live output text.
- `FILE4REPLACEMENT_DENY_PREFIXES` provides a baseline protection against
  common system directories even when path traversal is allowed, but it is
  not a substitute for restricting who can edit map files in the first place.
- Referenced files are plain text on disk. Combine with your OS's file
  permissions if the content is sensitive.

---

## 5. Example

See `config/maps/plugins/TEST_FILE4REPLACEMENT/` for a working example plugin,
and `tools/tests/TEST_FILE4REPLACEMENT.sh` for a test script that exercises
both an in-directory lookup and a lookup outside the plugin directory.

```python
# config/maps/plugins/TEST_FILE4REPLACEMENT/de-DE/FUZZY_MAP_pre.py
FUZZY_MAP_pre = [
    ('.Zebra.txt', r'^(Zebra)$', 85, {'command_flags': re.IGNORECASE}),
]
```

Create `.Zebra.txt` next to this file with the desired replacement text, then
say (or type via the console) `s Zebra` to trigger it.
