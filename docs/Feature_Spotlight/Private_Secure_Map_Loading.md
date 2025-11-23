# FEATURE SPOTLIGHT: Secure Private Map Loading and Integrity Check

This document outlines the architecture and workflow for loading private, sensitive, or experimental map plugins (`.py` files) in a way that enforces security best practices against accidental repository exposure while still allowing for automated local use and live-editing.

---

## 1. Overview and Problem Statement

**The Challenge:** Users need to store custom map files (e.g., specific client names, proprietary commands) that must never be committed to a public or shared Git repository.

**Standard Conflicts:**
1.  **Git Ignore Rule:** To ignore files, they often start with a dot (`.`) or an underscore (`_`).
2.  **Python Module Rule:** Python modules must *not* start with a dot (`.`).
3.  **Usability:** Maps must be easily editable and immediately reloaded (Live-Edit).

**The Solution:** Aura now uses an **Exception-Driven** unpacking workflow gated by a critical **`git-ignore` Security Check.**

---

## 2. Technical Deep Dive: The Security Workflow

The core logic is implemented in `scripts/py/func/map_reloader.py`.

### A. The Exception Trigger

The map scanner's standard import process is allowed to run. It will naturally encounter an intentionally invalid Python module (the dot-prefixed key file) and throw an exception.

1.  **Trigger File:** The user places a key file (e.g., **`.key.py`**) in a map directory.
2.  **Trigger Logic:** The main loop attempts to `import .key` which fails, leading to the `except Exception:` block (around line 114).

### B. The Security Gate (`_check_gitignore_for_security`)

Before any sensitive action is taken, the system executes a mandatory check:

1.  **Mandatory Rules:** The function verifies the main `.gitignore` file contains two critical rules:
    *   `config/maps/**/.*` (Protects the plaintext key file)
    *   `config/maps/**/_*` (Protects the unencrypted working code)
2.  **Action:** If either rule is missing, the process is **immediately aborted** with a `CRITICAL` log message. The private map will not load, preventing a security incident.

### C. Unpacking and Normalization

If the security check passes, the system proceeds to load the maps for use:

1.  **Key Extraction:** The password is read in plaintext from the `.key.py` file.
2.  **Unpacking:** The password-protected ZIP archive (e.g., `private.zip`) is unpacked into a temporary working directory that is prefixed with an underscore (e.g., `_private`). This prefix ensures it is immediately covered by the `gitignore` rule.
3.  **Normalization:** The logic includes a step to **normalize the folder structure**, preventing the common issue where a "right-click-zip" operation creates an unwanted nested folder (e.g., `_private/_private/`).
4.  **Live-Edit Readiness:** The working directory (`_private/`) remains on the disk. The user can now directly edit files in this directory, and the standard live-reloader will pick up the changes instantly.

---

## 3. User Workflow (How to Use)

To use the Private Map feature, follow these steps:

1.  **Add Git Ignore Rules (CRITICAL SETUP):**
    Ensure these two lines are in your main `.gitignore` file:
    ```
    config/maps/**/.*
    config/maps/**/_*
    ```

2.  **Create Key File (Password):**
    *   In your map directory (e.g., `config/maps/private/`), create a file that starts with a dot and ends with `.py` (to act as the trigger).
    *   **Example:** `config/maps/private/.auth_key.py`
    *   **Content:** The file's content must be the plaintext password for your ZIP archive.

3.  **Create ZIP Archive (Maps):**
    *   Place all your sensitive Python map files (`.py`) into a folder.
    *   **Archive:** Create a password-protected ZIP archive (e.g., `private_maps.zip`) from these files.
    *   **Placement:** Place the ZIP archive in the same directory as the key file.

4.  **Usage:**
    *   When Aura starts, it will detect the `.auth_key.py` and trigger the security check.
    *   The maps will be unpacked into a new directory (e.g., `config/maps/private/_private_maps/`).
    *   You can now **edit and test** files directly in this `_private_maps/` directory. Changes will be live-reloaded.

---

## 4. Security Note

This system provides **high assurance against accidental Git repository leakage**.

**LIMITATION:** This is **not a high-security encryption solution** against local attacks. The password is read and stored in plaintext in the `.key.....py` file, and the unencrypted map code exists on the local disk (`_private/`) and in system RAM. The solution prioritizes **Integrity Assurance** (preventing commits) and **Usability** (live-editing) over high-level local data protection.

