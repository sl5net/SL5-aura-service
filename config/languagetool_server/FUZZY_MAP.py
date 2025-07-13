# file config/languagetool_server/PUNCTUATION_MAP.py

# Map for fuzzy matching. More flexible but slightly slower.
# Format: (replacement_text, text_to_match, required_similarity_score_%)
# A higher score means the typo must be closer to the original text.
#
"""

deutsch try:

gut Status
gut Commit
Geht push
gut feig
gut brach

Getriebe Byes

english try:

It's that truth
Git commit
Get push
Good.'

"""
FUZZY_MAP = [
    # --- Basic Workflow ---
    # High scores for short commands to avoid ambiguity.
    ('git status', 'git status', 85),
    ('git add .', 'git add .', 90),
    ('git add -p', 'git add -p', 85),
    ('git commit', 'git commit', 85),
    ('git commit -m', 'git commit -m', 85),
    ('git commit --amend', 'git commit --amend', 80),
    ('git push', 'git push', 90),
    ('git push --force', 'git push --force', 80),
    ('git pull', 'git pull', 90),
    ('git pull --rebase', 'git pull --rebase', 80),
    ('git fetch', 'git fetch', 85),
    ('git fetch --all', 'git fetch --all', 85),

    # --- Branching & Merging ---
    ('git branch', 'git branch', 85),
    ('git branch -d', 'git branch -d', 85),
    ('git branch -D', 'git branch -D', 85),
    ('git branch -a', 'git branch -a', 85),
    ('git checkout', 'git checkout', 85),
    ('git checkout -b', 'git checkout -b', 85),
    ('git switch', 'git switch', 85),
    ('git switch -c', 'git switch -c', 85),
    ('git merge', 'git merge', 85),
    ('git rebase', 'git rebase', 85),
    ('git rebase -i', 'git rebase -i', 85),
    ('git rebase --continue', 'git rebase --continue', 80),

    # --- Inspection & History ---
    ('git log', 'git log', 90),
    ('git log --oneline', 'git log --oneline', 80),
    ('git log --graph', 'git log --graph', 80),
    ('git diff', 'git diff', 85),
    ('git diff --staged', 'git diff --staged', 80),
    ('git diff --cached', 'git diff --cached', 80), # Alias for --staged
    ('git show', 'git show', 90),

    # --- Stashing ---
    ('git stash', 'git stash', 85),
    ('git stash pop', 'git stash pop', 85),
    ('git stash apply', 'git stash apply', 85),
    ('git stash list', 'git stash list', 85),
    ('git stash save', 'git stash save', 85),

    # --- Resetting & Reverting ---
    ('git reset', 'git reset', 85),
    ('git reset --hard', 'git reset --hard', 80),
    ('git reset --soft', 'git reset --soft', 80),
    ('git revert', 'git revert', 85),
    ('git clean -fd', 'git clean -fd', 85),

    # --- Remote Repositories ---
    ('git remote -v', 'git remote -v', 85),
    ('git remote add', 'git remote add', 85),
    ('git remote remove', 'git remote remove', 80),
]
