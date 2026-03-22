import re  # noqa: F401

# ============================================================
# Koan 02: Your First Regex Rule – On or Off?
# ============================================================
#
# LEARNING GOAL:
#   Regex rules can map multiple spoken words to one command.
#   Here: letter groups control "on"/"off".
#
# TASK:
#   Remove '#' from ONE rule below.
#   Save – Aura reloads on the next hotkey trigger.
#   Say a word starting with a-m (e.g. "hello")
#   or one starting with n-z (e.g. "water").
#
# EXPECTED RESULT:
#   "hello" → "on"
#   "water" → "off"
#
# QUESTION TO THINK ABOUT:
#   What happens if you activate both rules?
#   Which one wins – and why?
#
# NEXT STEP: Koan 03
# ============================================================

FUZZY_MAP_pre = [
    # ('on',  r'^[a-m]+.*$', 80, {'flags': re.IGNORECASE}),
    # ('off', r'^[n-z]+.*$', 80, {'flags': re.IGNORECASE}),
]
