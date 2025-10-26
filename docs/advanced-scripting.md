# Advanced Rule Actions: Executing Python Scripts

This document describes how to extend the functionality of simple text replacement rules by executing custom Python scripts. This powerful feature allows you to create dynamic responses, interact with files, call external APIs, and implement complex logic directly within your speech recognition workflow.

## The Core Concept: `on_match_exec`

Instead of just replacing text, you can now tell a rule to execute one or more Python scripts when its pattern matches. This is done by adding an `on_match_exec` key to the rule's options dictionary.

The Service's primary job is to receive information about the match:

```
match_data = {
    'original_text': original_text_for_script,
    'text_after_replacement': new_current_text,
    'regex_match_obj': match_obj,  # Wir haben es bereits von re.fullmatch
    'rule_options': options_dict
}
```

And then, perform an action, and return a final string that will be used as the new text.


### Rule Structure

A rule with a script action looks like this:

```python
# In your map file (e.g., config/maps/.../de-DE/my_rules.py)
from pathlib import Path

# It's best practice to define the directory path once at the top
CONFIG_DIR = Path(__file__).parent

FUZZY_MAP_pre = [
    (
        '',  # The replacement string is often , as the script generates the final text.
        r'what time is it', # The regex pattern to match.
        95, # The confidence threshold.
        {
            'flags': re.IGNORECASE,
            # The new key: a list of script files to execute.
            'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
        }
    ),
]
```
**Key Points:**
- The `on_match_exec` value must be a **list**.
- Scripts are located in the same directory as the map file, which is why `CONFIG_DIR / 'script_name.py'` is the recommended way to define the path.

---

## Creating an Executable Script

For the system to use your script, it must follow two simple rules:
1.  It must be a valid Python file (e.g., `my_script.py`).
2.  It must contain a function named `execute(match_data)`.

### The `execute(match_data)` Function

This is the standard entry point for all executable scripts. The system will automatically call this function when the rule matches.

- **`match_data` (dict):** A dictionary containing all the context about the match.
- **Return Value (str):** The function **must** return a string. This string will become the new processed text.

### The `match_data` Dictionary

This dictionary is the bridge between the main application and your script. It contains the following keys:

*   `'original_text'` (str): The full text string *before* any replacement from the current rule was applied.
*   `'text_after_replacement'` (str): The text *after* the rule's basic replacement string was applied, but *before* your script was called. (If the replacement is ``, this will be the same as `original_text`).
*   `'regex_match_obj'` (re.Match): The official Python regex match object. This is extremely powerful for accessing **capture groups**. You can use `match_obj.group(1)`, `match_obj.group(2)`, etc.
*   `'rule_options'` (dict): The complete options dictionary for the rule that triggered the script.

---

## Examples

### Example 1: Getting the Current Time (Dynamic Response)

This script returns a personalized greeting based on the time of day.

**1. The Rule (in your map file):**
```python
('', r'\b(what time is it|uhrzeit)\b', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'get_current_time.py']
}),
```

**2. The Script (`get_current_time.py`):**
```python
from datetime import datetime
import random

def execute(match_data):
    """Returns a friendly, time-aware response."""
    now = datetime.now()
    hour = now.hour
    time_str = now.strftime('%H:%M')

    if hour < 12:
        greeting = "Good morning!"
    elif hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    
    responses = [
        f"{greeting} It's currently {time_str}.",
        f"Right now, the time is {time_str}. Hope you're having a great day!",
    ]
    return random.choice(responses)
```
**Usage:**
> **Input:** "what time is it"
> **Output:** "Good afternoon! It's currently 14:30."

### Example 2: Simple Calculator (Using Capture Groups)

This script uses capture groups from the regex to perform a calculation.

**1. The Rule (in your map file):**
```python
('', r'calculate (\d+) (plus|minus) (\d+)', 98, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'calculator.py']
}),
```

**2. The Script (`calculator.py`):**
```python
def execute(match_data):
    """Performs a simple calculation based on regex capture groups."""
    try:
        match_obj = match_data['regex_match_obj']
        
        num1 = int(match_obj.group(1))
        operator = match_obj.group(2).lower()
        num2 = int(match_obj.group(3))

        if operator == "plus":
            result = num1 + num2
        elif operator == "minus":
            result = num1 - num2
        else:
            return "I didn't understand that operator."
            
        return f"The result is {result}."
    except (ValueError, IndexError):
        return "I couldn't understand the numbers in your request."
```
**Usage:**
> **Input:** "calculate 55 plus 10"
> **Output:** "The result is 65."

### Example 3: Persistent Shopping List (File I/O)

This example shows how one script can handle multiple commands (adding, showing) by inspecting the user's original text, and how it can persist data by writing to a file.

**1. The Rules (in your map file):**
```python
# Rule for adding items
('', r'add (.*) to the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),

# Rule for showing the list
('', r'show the shopping list', 95, {
    'flags': re.IGNORECASE,
    'on_match_exec': [CONFIG_DIR / 'shopping_list.py']
}),
```

**2. The Script (`shopping_list.py`):**
```python
from pathlib import Path

LIST_FILE = Path(__file__).parent / "shopping_list.txt"

def execute(match_data):
    """Manages a shopping list stored in a text file."""
    original_text = match_data['original_text'].lower()
    
    # --- Add Item Command ---
    if "add" in original_text:
        item = match_data['regex_match_obj'].group(1).strip()
        with open(LIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{item}\n")
        return f"Okay, I've added '{item}' to the shopping list."
    
    # --- Show List Command ---
    elif "show" in original_text:
        if not LIST_FILE.exists() or LIST_FILE.stat().st_size == 0:
            return "The shopping list is empty."
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            items = f.read().strip().splitlines()
        
        item_str = ", ".join(items)
        return f"On the list you have: {item_str}."
        
    return "I'm not sure what to do with the shopping list."
```
**Usage:**
> **Input 1:** "add milk to the shopping list"
> **Output 1:** "Okay, I've added 'milk' to the shopping list."
>
> **Input 2:** "show the shopping list"
> **Output 2:** "On the list you have: milk."

---

## Best Practices

-   **One Job Per Script:** Keep scripts focused on a single task (e.g., `calculator.py` only calculates).
-   **Error Handling:** Always wrap your script's logic in a `try...except` block to prevent it from crashing the entire application. Return a user-friendly error message from the `except` block.
-   **External Libraries:** You can use external libraries (like `requests` or `wikipedia-api`), but you must ensure they are installed in your Python environment (`pip install <library-name>`).
-   **Security:** Be aware that this feature can execute any Python code. Only use scripts from trusted sources.


