# Home Directory & Cross-Platform Path Handling

Aura is designed to run across multiple operating systems. To ensure that file system navigation commands work regardless of whether you are running Linux, macOS, or Windows, path strings are parsed dynamically before they are registered in the active fuzzy maps.

---

## Path Normalization Logic (`FUZZY_MAP_pre.py`)

The dynamic path mapping logic relies on the following standard practices:

### 1. Tilde Reduction (POSIX)
On POSIX-compliant systems (Linux and macOS), absolute paths matching the user's home directory (e.g., `/home/username/`) are converted to `~` relative paths at startup. This keeps string lengths shorter and makes the generated rules portable between different users on the same operating system:

```python
# Replaces '/home/username/projects' with '~/projects'
if sys.platform != 'win32' and project_root_str_full.startswith(home_dir_str):
    PROJECT_ROOT_FOR_MAP = project_root_str_full.replace(home_dir_str, '~', 1)
```

### 2. Absolute Path Preservation (Windows)
Windows does not reliably evaluate the `~` character in standard Command Prompt (`cmd.exe`) or PowerShell environments. Therefore, when the plugin detects a Windows environment (`sys.platform == 'win32'`), it preserves the fully qualified absolute path (e.g., `C:\Users\username\...`) to ensure command execution does not fail.

### 3. Forward Slash Normalization (`as_posix()`)
Aura uses POSIX-style forward slashes (`/`) internally for configuration maps. The script normalizes all OS-dependent path separators by utilizing Python's `pathlib.Path.as_posix()` method, which automatically sanitizes backslashes (`\`) on Windows environments.
