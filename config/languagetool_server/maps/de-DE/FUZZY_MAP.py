# FUZZY_MAP.py
# This map combines precise regex rules with flexible fuzzy matching.
#
# HOW IT WORKS:
# 1. Regex Rules (r'...') are checked first for an exact, prioritized match.
#    - We use r'^...' to anchor the match to the START of the phrase, which is
#      perfect for git commands.
# 2. Fuzzy Rules (plain strings) are used as a fallback if no regex matches.

"""
Mir geht es gut
﻿Geht gut
﻿git status
﻿git commit
﻿git add .
﻿Geht es gut
﻿Geht gut
Geht es gut
Geht gut
﻿Geht es gut
git add .
mitkomm mit
"""

FUZZY_MAP = [

    ('pull requests', r'^pull requests$', 82),
    ('pull requests', r'^Pullover Quest$', 82),

    ('Lauffer', r'\bLäufer\b', 100),

    # --- git status ---
    ('git status', r'^git status$', 82),
    ('git status', r'^geht status$', 82),
    ('git status', r'^gitter status$', 82),
    ('git status', r'^geht staates$', 82),

    # --- git add . ---
    ('git add .', r'^git add$', 82),
    ('git add .', r'^Geht hätte$', 82),
    ('git add .', r'^geht add punkt$', 82),
    ('git add .', r'^gittert punkt$', 82),
    ('git add .', r'^geht duett$', 82),
    ('git add .', r'^git at$', 82),
    ('git add .', r'^mit at$', 82),
    ('git add .', r'^kate at$', 82),
    ('git add .', r'^fiat at$', 82),
    ('git add .', r'^geht ab hat$', 82),
    ('git add .', r'^geht hat$', 82),
    ('git add .', r'^gitta hat$', 82),
    ('git add .', r'^dad geh$', 82),
    ('git add .', r'^tat id$', 82),
    ('git add .', r'^geh tat$', 82),
    ('git add .', r'^da hat$', 82),
    ('git add .', r'^geht es$', 82),

    # --- git commit ---
    ('git commit', r'^git commit$', 80),
    ('git commit', r'^mitkomm mit$', 80),
    ('git commit', r'^womit$', 85),           # Using '$' to match the whole word "womit"
    ('git commit -m "', r'^geht com mit$', 80),
    ('git commit -m "', r'^gitter mit$', 80),

    # --- git push ---
    ('git push', r'^git push$', 80),
    ('git push', r'^geht busch$', 85),
    ('git push', r'^gitter busch$', 85),

    # --- git pull ---
    ('git pull', r'^git pull$', 80),
    ('git pull', r'^geht pohl$', 82),
    ('git pull', r'^gitter pohl$', 82),
    ('git pull', r'^geht pool$', 80),
    # Note: 'pool' is a fuzzy rule without regex. It will only be checked
    # if no other regex rule for 'git pull' matches.
    ('git pull', '^pool$', 80),

    # --- git diff ---
    ('git diff', r'^git diff$', 75),
    ('git diff', r'^geht tief$', 75),
    ('git diff', r'^peach juice$', 75), # .lower() is used, so case doesn't matter

    # --- Other commands (Example) ---
    ('0 A.D.', 'sierra d', 75), # This is a good candidate for a non-regex fuzzy match
]