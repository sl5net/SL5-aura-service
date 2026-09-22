> ℹ️ *This is a machine-translated document. In case of discrepancies, refer to the [original document](../configuration_tasks.md).*

Configuration Koans

### 1. Koan 08: The Switchboard (Activating Plugins)
**Learning effect:** Participants learn how to unlock new features (plugins) in the `settings.py`.

*   **Task:** "Activate the Wikipedia plugin by changing the value of `False` to `True`."
*   **Benefit:** Understand that Aura is modular.

### 2. Koan 09: Your digital nameplate (variables)
**Learning effect:** Store your own data in the configuration that is used by plugins.
*   **Task:** "Enter your own name in the variable `USER_NAME`."
*   **Use:** Plugins can then write sentences like "With kind greetings, [your name]".

```py
from config import settings
user_name = getattr(settings, "USER_NAME", "[Name fehlt]")
```

Koan 10: Please be patient! (break times)
**Learning effect:** Adapting the speech recognition to your own speech mpo.
*   **Task:** "Increase the `SPEECH_PAUSE_TIMEOUT` so that Aura waits longer before processing your sentence."
*   **Use:** Especially if you think in peace.

