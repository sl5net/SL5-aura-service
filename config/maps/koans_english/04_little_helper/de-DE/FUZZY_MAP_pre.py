# config/maps/koans_english/04_little_helper/de-DE/FUZZY_MAP_pre.py
import re # noqa: F401

littleHelpers = """
Aura can serve as a quick reference tool.
We are using famous international Area Codes for this Koan.

Try to ask:
- 'Area code of Silicon Valley'
- 'Area code of New York'
- 'Area code of Tokyo'

Can you find your own city's code?
Check log/aura_engine.log to see the transcription!
"""

FUZZY_MAP_pre = [
    # Tech Hubs & Global Cities
    # EXAMPLE: area code of Silicon Valley
    ('408', r'^area code (of )?Silicon Valley$', 90, {'flags': re.IGNORECASE}),
    # EXAMPLE: area code of New York Manhattan
    ('212', r'^area code (of )?New York( Manhattan)?$', 90, {'flags': re.IGNORECASE}),
    # EXAMPLE: area code of London
    ('020', r'^area code (of )?London$', 90, {'flags': re.IGNORECASE}),
    # EXAMPLE: area code of Tokyo
    ('03', r'^area code (of )?Tokyo$', 90, {'flags': re.IGNORECASE}),
    # EXAMPLE: area code of Seattle
    ('206', r'^area code (of )?Seattle$', 90, {'flags': re.IGNORECASE}),
    # EXAMPLE: area code of Paris
    ('01', r'^area code (of )?Paris$', 90, {'flags': re.IGNORECASE}),
]

#
