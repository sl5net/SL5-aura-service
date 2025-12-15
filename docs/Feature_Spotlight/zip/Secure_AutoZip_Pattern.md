# Secure Auto-Zip & Embedded Documentation

## Concept
SL5 Aura monitors private folders starting with `_` (e.g., `_my_confidential_data`).
When changes are detected, Aura creates an **encrypted** zip archive automatically.

## Critical Prerequisite: Encryption Key
**Encryption is mandatory.** The auto-zip process strictly requires a password file to be present in the directory hierarchy (current or parent folders).

*   **File Requirement:** The password file must start with a dot `.` (e.g., `.archive_pass`, `.secret`).
*   **Behavior:** If no dot-file with a password is found, the zip process is **blocked**. This failsafe ensures no unencrypted data is ever packaged.

## The "Embedded Docs" Pattern
Since Aura's hot-reload system listens for **valid Python files**, updating a simple `.txt` readme will not trigger a re-zip.

To include instructions for recipients (e.g., "How to unzip") while ensuring the trigger fires, use a **Python Docstring File**.

### Implementation
Create a file named `README_AUTOZIP.py` inside your monitored folder.

```python
# Documentation

"""
# SECURE ARCHIVE

This archive was automatically encrypted by SL5 Aura.
Password provided via separate channel.

TRIGGER INFO:
Folders starting with "_" are monitored.
Encryption requires a valid `.` (dot) password file in the path.

TECHNICAL NOTE:
`__init__.py` and `README_AUTOZIP.py` are required for the 
change-detection system.

---
Generiert von SL5 Aura
The Architect's Solution for Offline Voice Control.
"""
