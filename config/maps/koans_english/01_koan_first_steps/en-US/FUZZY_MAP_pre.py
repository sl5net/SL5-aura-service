import re  # noqa: F401

# ============================================================
# Koan 01: Your First Rule – Welcome to Aura!
# ============================================================
#
# PREREQUISITE: Aura is running and your hotkey is configured.
# If not: see docs/GettingStarted.md
#
# TASK:
#   Remove the '#' before the rule below.
#   Save – Aura reloads on the next hotkey trigger.
#   Press your hotkey and say: "hello world"
#
# EXPECTED RESULT:
#   Aura types: "Hello World 01"
#
# WHY DOES THE PIPELINE STOP?
#   The pattern r'^.*$' matches EVERYTHING – no further rules
#   are checked after a full match. See docs/FuzzyMapRuleGuide.md
#
# NEXT STEP: Koan 02
# ============================================================

FUZZY_MAP_pre = [
    #('Hello World 01', r'^hello world$', 0, {'flags': re.IGNORECASE}),
]
