# file config/languagetool_server/PUNCTUATION_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#

# the git statusgit status

"""
Gujarat
git add .
git commit
git push

git status
did
It's permits
git push
git pull'


"""

FUZZY_MAP = [
    ('git status', 'get status', 80),
    ('git status', 'the kids stayed', 85),
    ('git status', 'good it', 85),
    ('git status', 'good status', 85),
    ('git status', 'Good status', 85),

    ('git add .', 'stage all', 80),
    ('git add .', 'get add', 80),
    ('git add .', 'your debt dutch', 80),
    ('git add .', 'Get to it', 80),

    ('git commit', 'get commit', 80),

    ('git push', 'get push', 75),
    ('git push', 'it\'d push', 85),

    # ('git pull', 'good play', 80),
    ('git pull', 'get pull', 85),
    # ('git pull', 'good point', 85),
    # ('git pull', 'Good point', 85),
    ('git pull', 'Good pull', 85),
    ('git pull', 'Get poorer', 80),

    ('git diff', 'git diff', 80),




]
