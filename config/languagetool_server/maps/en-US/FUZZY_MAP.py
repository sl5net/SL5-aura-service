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
    ('Git', r'^kit$', 85),
    ('GitHub', r'^get up$', 85),
    ('GitHub', r'^good job$', 85),
    ('GitHub', r'^keep it up$', 85),
    ('GitHub', r'^q-tip$', 85),
    ('git add .', r'^due to its$', 85),
    ('git add .', r'^Get did$', 85),
    ('git add .', r'^get add$', 80),
    ('git add .', r'^Get to it$', 80),
    ('git add .', r'^good chat$', 85),
    ('git add .', r'^Good touch$', 85),
    ('git add .', r'^stage all$', 80),
    ('git add .', r'^your debt dutch$', 80),
    ('git commit', r'^get commit$', 80),
    ('git commit', r'^the commit$', 85),
    ('git diff', r'^git diff$', 80),
    ('git pull', r'^get point$', 85),
    ('git pull', r'^get pull$', 85),
    ('git pull', r'^get the flu$', 85),
    ('git pull', r'^Get poorer$', 80),
    ('git pull', r'^gg pool$', 85),
    ('git pull', r'^good play$', 85),
    ('git pull', r'^good point$', 85),
    ('git pull', r'^good pool$', 85),
    ('git pull', r'^Good pull$', 85),
    ('git push', r'^get push$', 75),
    ('git push', r'^it\'d push$', 85),
    ('git push', r'^push$', 85),
    ('git status', r'^get status$', 80),
    ('git status', r'^good it$', 85),
    ('git status', r'^good stages$', 85),
    ('git status', r'^good status$', 85),
    ('git status', r'^Good stages$', 85),
    ('git status', r'^Good status$', 85),
    ('git status', r'^it\'s status$', 85),
    ('git status', r'^the good status$', 85),
    ('git status', r'^the kids stayed$', 85),
]
