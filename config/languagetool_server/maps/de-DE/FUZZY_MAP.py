# file config/languagetool_server/PUNCTUATION_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#
"""

deutsch try:




english try:

git status git status
Gitta hat AT
womit Komm mit
Mit push git push
Geht Pool Bull


git status
Gitta hat
womit
git push
Pool

git status
Beat hebt
git commit
git push
Geht Pool Geht Pool Mit Pool

git status
Geht Duett
womit
git push
git pull

git status
Git AT Fiat AT Geht ab hat
git commit
git push
git pull

Geht Staates
Git AT  Mit AT  git add .
git commit
git push
git pull

git status
Drei Versuche: Kate AT Geht es git add .
Komm mit git commit
git push
git pull

git status
Dad geh tat ID AT geh tat geh tat Da hat Internet
git commit
git push
git pull

git status
git add .
git commit
git push
git pull
Geht tief
Peach juice
Good gifts
Good tips
"""
# Format: ('Text, der eingesetzt wird', 'Satz, mit dem verglichen wird', Mindest-Trefferquote)
FUZZY_MAP = [
    ('git status', 'git status', 85),
    ('git add .', 'git add', 85),
    ('git add .', 'geht duett', 85),

    ('git add .', 'fiat at', 85),
    ('git add .', 'geht ab hat', 85),
    ('git add .', 'gitta hat', 85),

    ('git add .', 'git at', 85),
    ('git add .', 'mit at', 85),

    ('git add .', 'kate at', 85),
#    ('git add .', 'geht es', 85), ToDo should be only work at line beginning

    ('git commit', 'git commit', 80),
    ('git commit', 'womit', 85),

    ('git push', 'git push', 80),
    ('git pull', 'git pull', 80),

    ('git pull', 'geht pool', 80),
    ('git pull', 'pool', 80),

    ('git diff', 'git diff', 75),
    ('git diff', 'Geht tief', 75),
    ('git diff', 'Peach juice', 75),

    ('git diff', 'Peach juice', 75),

    ('sierra d', '0 A.D.', 75),


]
