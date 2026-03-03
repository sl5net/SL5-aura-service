# User-Specific Voice Commands

Aura allows you to define custom commands that are **only active for you** (or specific team members). This prevents personal shortcuts or experimental features from being triggered by other users.

## Setup

You can apply these rules in any mapping file, such as `FUZZY_MAP_pre.py` (raw input) or `FUZZY_MAP.py` (after correction).

Target file: `config/maps/plugins/internals/de-DE/FUZZY_MAP_pre.py`

### Code Example

Add this block to the end of the file:

```python
from scripts.py.func.determine_current_user import determine_current_user

# 1. Who am I?
current_user, _ = determine_current_user()

# 2. Activate specific commands for 'misterx' only
if current_user in ['misterx']:
    MY_USER_RULES = [
        # Syntax: (Response/Action, Regex-Pattern, Min-Accuracy, Options)
        (f"Hello {current_user}", r'^(hi)$') 
    ]
    FUZZY_MAP_pre.extend(MY_USER_RULES)
    
