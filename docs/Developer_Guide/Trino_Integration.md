This is a great milestone! You’ve moved from theory to a working **Trino proof-of-concept** with persistent state in the `memory` catalog.

To fix the translation issue, the logic in your `toggle_translation_mode.py` and `translate_from_to.py` likely still looks at the local `config.json` instead of querying Trino.

Here is the updated documentation and the commit message.

### 1. Git Commit
```text
docs: update Trino guide with live table examples and state management logic
```

### 2. Updated `docs/Developer_Guide/Trino_Integration.md`

```markdown
# Trino Integration Guide

## Local Environment Setup

### 1. Docker & Image
```bash
docker pull trinodb/trino
docker rm trino 2>/dev/null || true
docker run -d --name trino -p 8083:8080 trinodb/trino
# Wait for:
docker logs trino -f | grep -m1 "SERVER STARTED"
```

### 2. Client Installation
```bash
pip install trino
```

## State Management (Live Example)

We use the `memory` catalog for fast, session-based state management. Below is how to interact with the `translation_state` table.

### Insert & Query State
This example uses `determine_current_user` to handle multi-user environments:

```python
from scripts.py.func.determine_current_user import determine_current_user
import trino

current_user, _ = determine_current_user()
conn = trino.dbapi.connect(host='localhost', port=8083, user=current_user)
cur = conn.cursor()

# Update state for different contexts
cur.execute(f'''
    INSERT INTO memory.aura.translation_state (context, lang, state, updated_at) 
    VALUES ('terminal', 'en', 'off', CURRENT_TIMESTAMP)
''')

# Fetch current settings
cur.execute('SELECT * FROM memory.aura.translation_state')
rows = cur.fetchall()
print(rows)
```

## Troubleshooting: Why is it still translating?

If the Terminal or Streamlit still translates despite the Trino state being `off`, check these files:

1.  **`config/maps/plugins/.../toggle_translation_mode.py`**: Ensure this script sends an `INSERT` or `UPDATE` to Trino instead of just modifying a local variable.
2.  **`translate_from_to.py`**: This script needs to perform a `SELECT state FROM memory.aura.translation_state WHERE context = 'terminal'` before proceeding with the translation logic.
3.  **Config Priority**: Ensure Trino values override the static `config.json`.

## Current Configuration Roadmap
- [x] Trino Container Running
- [x] Manual Table Creation/Insertion
- [ ] Refactor `translate_from_to.py` to fetch state from Trino
- [ ] Implement user-specific overrides
```

### Tips for your next steps:
*   **The "Double State" Problem:** Your `fetchall()` output shows multiple entries for 'terminal' (`on` and `off`). Trino's `memory` connector doesn't enforce primary keys. 
*   **Fix:** In your `translate_from_to.py`, always query the **newest** entry:
    `SELECT state FROM memory.aura.translation_state WHERE context = 'terminal' ORDER BY updated_at DESC LIMIT 1`
*   **Automation:** You should modify `scripts/py/func/determine_current_user.py` or a similar helper to provide a `get_trino_config(context)` function that you can call inside your translation plugins.
