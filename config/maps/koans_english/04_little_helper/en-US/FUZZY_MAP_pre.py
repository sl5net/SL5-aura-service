import re  # noqa: F401

# ============================================================
# Koan 04: Little Helpers – Numbers & Codes by Voice
# ============================================================
#
# LEARNING GOAL:
#   Rules can output numbers and codes that Vosk cannot
#   recognize directly – triggered by spoken phrases.
#
# TASK:
#   Say: "area code of Tokyo"
#   Expected result: "03"
#
#   Then add your own city's area code!
#   Check log/aura_engine.log to see the raw transcription.
#
# NEXT STEP: Koan 05
# ============================================================

FUZZY_MAP_pre = [
    ('408', r'^area code (of )?Silicon Valley$'),
    ('212', r'^area code (of )?New York( Manhattan)?$'),
    ('020', r'^area code (of )?London$'),
    ('03',  r'^area code (of )?Tokyo$'),
    ('206', r'^area code (of )?Seattle$'),
    ('01',  r'^area code (of )?Paris$'),
]
