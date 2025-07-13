# file config/languagetool_server/PUNCTUATION_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#
"""

deutsch try:

english try:

The kids stayed
Good it
git commit
get push
Good point

Good status Good status
Your debt Dutch
git commit git commit
it'd push get push
Good play Good point

It's status Good status
cadets Gujarat
The commit git commit
get push push
Good point Good point

The good status the   It's status   It's status   git status   git status   git status  git status Good stages
Good touch You touch Pizza Hut Get your hitch       Get it  You touch  touch   Get it
git commit
get push
Good point Good point Get point Good point Good pool Good point

Good status git status
Good chat Due to its
git commit
get push
GG pool Get the flu Good point Good point Good point

Good touch It's New to it Get did
git commit
get push
Good point Get poorer Get poorer get push Gets put Good point Good point


Good status
Get to it
It's commit
git commit
get push'
Good pull
"""


FUZZY_MAP = [
    ('git status', 'get status', 85),
    ('git status', 'the kids stayed', 85),
    ('git status', 'good it', 85),
    ('git status', 'good status', 85),
    ('git status', 'Good status', 85),

    ('git add .', 'stage all', 80),
    ('git add .', 'get add', 80),
    ('git add .', 'your debt dutch', 75),
    ('git add .', 'Get to it', 75),

    ('git commit', 'get commit', 85),

    ('git push', 'get push', 90),
    ('git push', 'it\'d push', 85),

    ('git pull', 'good play', 80),
    ('git pull', 'get pull', 80),
    ('git pull', 'good point', 80),
    ('git pull', 'Good pull', 80),
    ('git pull', 'Get poorer', 80),


]
