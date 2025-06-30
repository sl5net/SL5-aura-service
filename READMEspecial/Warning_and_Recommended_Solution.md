### **Developer Warning: A Critical Pitfall in AutoKey Inter-Script Communication**

**Applies to:** Developers passing state or data between AutoKey scripts, especially when using `engine.run_script()`.

#### Context

A common automation pattern in AutoKey involves a "controller" script (Script A) that sets a value or state, and then immediately calls a "worker" script (Script B) to perform an action based on that new state.

**Example:** Script A sets a language model to `english`, and then Script B is expected to use that `english` model.

#### The Pitfall: `store.set_value()` is Not Immediately Consistent

The intuitive approach is to use AutoKey's built-in `store` API:

**Script A (`set_model.py`):**```python
# The intuitive, but flawed, approach
new_model = "some-new-value"
store.set_value("my_setting", new_model)
engine.run_script("worker_script") 
```

**Script B (`worker_script.py`):**
```python
# This code will often read the OLD value
current_setting = store.get_value("my_setting")

# This condition often fails because current_setting still holds the old value
if current_setting == "some-new-value":
    # This block is NOT reliably executed
    ...
```

**Symptom:** The worker script appears to ignore the change made by the controller script. Crucially, adding a `time.sleep()` delay in the controller script is **not** a reliable fix for this issue.

**Cause:** AutoKey appears to provide each script with its own runtime environment, which includes a cached version of the `store` data. When Script B is launched by `engine.run_script()`, there is no guarantee that the change just written by Script A has been propagated to Script B's cache. This creates a race condition that makes the `store` API unreliable for rapid, direct communication between scripts.

### The Recommended Solution: Use the Filesystem as a Reliable Communication Channel

The most robust and transparent solution is to bypass the `store` API for this purpose and use the operating system's filesystem as a "mailbox". Filesystem I/O is managed by the OS kernel and is consistent across different processes.

**Principle:**
1.  **Script A writes** the new value to a dedicated file in a temporary location (e.g., `/tmp/my_app_setting`).
2.  **Script B reads** the value from that file upon startup.

#### Implementation Example

**Script A (`set_model.py`):**
```python
from pathlib import Path

# The path to our communication file
SETTING_FILE = "/tmp/myapp_model_setting.txt"
new_model = "vosk-model-small-en-us-0.15"

# Write the new value to the file, overwriting any previous content
Path(SETTING_FILE).write_text(new_model)

# Call the worker script
engine.run_script("worker_script")
```

**Script B (`worker_script.py`):**
```python
from pathlib import Path

SETTING_FILE = "/tmp/myapp_model_setting.txt"
DEFAULT_MODEL = "vosk-model-de-0.21"

setting_file_path = Path(SETTING_FILE)

# Try to read the value from the file
if setting_file_path.exists():
    current_model = setting_file_path.read_text().strip()
    # Optional: Delete the file after reading to prevent reusing a stale signal
    # setting_file_path.unlink() 
else:
    current_model = DEFAULT_MODEL

# From here, `current_model` can be used reliably
# For example:
# if current_model != get_last_used_model():
#     restart_service(current_model)
```

**Advantages of this method:**
*   **Reliability:** It is 100% consistent, as file operations are managed by the OS.
*   **Transparency:** The current state can be easily inspected from any terminal for debugging (`cat /tmp/myapp_model_setting.txt`).
*   **Independence:** It makes your application logic independent of the undocumented and unpredictable caching behavior of AutoKey's `store`.

We strongly advise developers to adopt this file-based approach for all critical, state-passing communication between AutoKey scripts to avoid hard-to-debug timing issues.
