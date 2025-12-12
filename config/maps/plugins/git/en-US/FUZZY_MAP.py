# file config/languagetool_server/maps/en-US/FUZZY_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#


# The REGEX_MAP is currently kept minimal as most logic moves to the more robust FUZZY_MAP.
# Todo: REGEX_MAP not implemented actually 21.7.'25 07:27 Mon
REGEX_MAP = {
    # This map is processed first for high-priority, exact matches.
}

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match_regex, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
# The regex is anchored (^...$) to ensure it matches the whole phrase.

FUZZY_MAP = [


    # EXAMPLE: kit
    ('Git', r'^kit$', 85),
    # EXAMPLE: get up
    ('GitHub', r'^get up$', 85),
    # EXAMPLE: good job
    ('GitHub', r'^good job$', 85),
    # EXAMPLE: keep it up
    ('GitHub', r'^keep it up$', 85),
    # EXAMPLE: q-tip
    ('GitHub', r'^q-tip$', 85),
    # EXAMPLE: due to its
    ('git add .', r'^due to its$', 85),
    # EXAMPLE: Get did
    ('git add .', r'^Get did$', 85),
    # EXAMPLE: get add
    ('git add .', r'^get add$', 80),
    # EXAMPLE: Get to it
    ('git add .', r'^Get to it$', 80),
    # EXAMPLE: good chat
    ('git add .', r'^good chat$', 85),
    # EXAMPLE: Good touch
    ('git add .', r'^Good touch$', 85),
    # EXAMPLE: stage all
    ('git add .', r'^stage all$', 80),
    # EXAMPLE: your debt dutch
    ('git add .', r'^your debt dutch$', 80),
    # EXAMPLE: get commit
    ('git commit', r'^get commit$', 80),
    # EXAMPLE: the commit
    ('git commit', r'^the commit$', 85),
    # EXAMPLE: git diff
    ('git diff', r'^git diff$', 80),
    # EXAMPLE: get point
    ('git pull', r'^get point$', 85),
    # EXAMPLE: get pull
    ('git pull', r'^get pull$', 85),
    # EXAMPLE: get the flu
    ('git pull', r'^get the flu$', 85),
    # EXAMPLE: Get poorer
    ('git pull', r'^Get poorer$', 80),
    # EXAMPLE: gg pool
    ('git pull', r'^gg pool$', 85),
    # EXAMPLE: good play
    ('git pull', r'^good play$', 85),
    # EXAMPLE: good point
    ('git pull', r'^good point$', 85),
    # EXAMPLE: good pool
    ('git pull', r'^good pool$', 85),
    # EXAMPLE: Good pull
    ('git pull', r'^Good pull$', 85),
    # EXAMPLE: get push
    ('git push', r'^get push$', 75),
    # EXAMPLE: it
    ('git push', r'^it\'d push$', 85),
    # EXAMPLE: push
    ('git push', r'^push$', 85),
    # EXAMPLE: get status
    ('git status', r'^get status$', 80),
    # EXAMPLE: good it
    ('git status', r'^good it$', 85),
    # EXAMPLE: good stages
    ('git status', r'^good stages$', 85),
    # EXAMPLE: good status
    ('git status', r'^good status$', 85),
    # EXAMPLE: Good stages
    ('git status', r'^Good stages$', 85),
    # EXAMPLE: Good status
    ('git status', r'^Good status$', 85),
    # EXAMPLE: it
    ('git status', r'^it\'s status$', 85),
    # EXAMPLE: the good status
    ('git status', r'^the good status$', 85),
    # EXAMPLE: the kids stayed
    ('git status', r'^the kids stayed$', 85),
]
