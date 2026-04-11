#!/bin/bash
# scripts/sh/check_translator_hijack.sh
#
# Guard: auto-unstages FUZZY_MAP_pre.py when a TRANSLATION_RULE is
# un-commented (= active), so it is silently dropped from the commit
# without blocking the developer's workflow.
#
# Called from .git/hooks/pre-commit — not meant to be run standalone.
#
# HOW IT WORKS
# ------------
# A rule is ACTIVE (dangerous) when the line immediately after a
#   # TRANSLATION_RULE
# header is NOT commented out (does not start with optional whitespace + #).
#
#   UNSTAGED  — rule is active:
#       # TRANSLATION_RULE
#       ("hallo", "hello"),        ← no leading #  →  file removed from commit
#
#   COMMITTED  — rule is safely commented out:
#       # TRANSLATION_RULE
#       # ("hallo", "hello"),      ← leading #     →  file committed normally
#
# WHY THIS EXISTS
# ---------------
# The TRANSLATION_RULE is needed during development to test language
# mappings. It is easy to forget to re-comment it before running
# "git add ." and committing. If it ships un-commented, every user
# gets silent automatic translation — which is not expected behavior.
#
# The file is quietly dropped from the staged list instead of blocking
# the commit, so the developer can continue working uninterrupted.
#
# STAGED-FILE CHECK
# -----------------
# The check only runs when FUZZY_MAP_pre.py is actually part of the
# current staged commit. Unrelated commits pass through untouched.
#
# TESTING WITHOUT A REAL COMMIT
# ------------------------------
# Run with --test to skip the staged-file check and scan directly:
#
#   bash scripts/sh/check_translator_hijack.sh --test
#
# This lets you verify detection logic at any time without staging
# or committing anything. In --test mode the file is never unstaged.

# ---------------------------------------------------------------------------
# 0. Argument parsing
# ---------------------------------------------------------------------------
TEST_MODE=0
for arg in "$@"; do
    case "$arg" in
        --test|--dry-run)
            TEST_MODE=1
            echo "[hijack-check] Running in TEST MODE — staged-file check skipped, no unstaging will occur."
            echo ""
            ;;
    esac
done

set -euo pipefail

# ---------------------------------------------------------------------------
# 1. Resolve PROJECT_ROOT from the /tmp marker file
# ---------------------------------------------------------------------------
if [ "${OS:-}" = "Windows_NT" ] || [ -n "${WINDIR:-}" ]; then
    tmp_dir='C:/tmp'
else
    tmp_dir='/tmp'
fi

MARKER_FILE="$tmp_dir/sl5_aura/sl5net_aura_project_root"

if [[ ! -f "$MARKER_FILE" ]]; then
    echo "[hijack-check] INFO: marker file not found: $MARKER_FILE"
    echo "[hijack-check] Skipping check (service not running / PROJECT_ROOT unknown)."
    exit 0
fi

PROJECT_ROOT="$(realpath "$(tr -d '\r' < "$MARKER_FILE")")"

echo "[hijack-check] PROJECT_ROOT = $PROJECT_ROOT"

# ---------------------------------------------------------------------------
# 2. Build path to the file we want to guard
# ---------------------------------------------------------------------------
FUZZY_MAP="$PROJECT_ROOT/config/maps/plugins/standard_actions/language_translator/de-DE/FUZZY_MAP_pre.py"

echo "[hijack-check] Target file : $FUZZY_MAP"

if [[ ! -f "$FUZZY_MAP" ]]; then
    echo "[hijack-check] INFO: FUZZY_MAP_pre.py not found at that path — skipping."
    exit 0
fi

# ---------------------------------------------------------------------------
# 3. Staged-file check (skipped in --test mode)
# ---------------------------------------------------------------------------
if [[ $TEST_MODE -eq 0 ]]; then
    REPO_ROOT="$(git rev-parse --show-toplevel)"
    RELATIVE_PATH="$(realpath --relative-to="$REPO_ROOT" "$FUZZY_MAP" 2>/dev/null || echo "$FUZZY_MAP")"

    if ! git diff --cached --name-only | grep -qF "$RELATIVE_PATH"; then
        echo "[hijack-check] FUZZY_MAP_pre.py is not staged — nothing to do."
        exit 0
    fi

    echo "[hijack-check] FUZZY_MAP_pre.py is staged — scanning for active rules..."
else
    echo "[hijack-check] Scanning file directly (test mode)..."
fi

# ---------------------------------------------------------------------------
# 4. Scan for active (un-commented) TRANSLATION_RULE entries
# ---------------------------------------------------------------------------
FOUND_HIJACK=0
ACTIVE_LINES=()
NEXT_IS_RULE=0
LINENO=0

while IFS= read -r line || [[ -n "$line" ]]; do
    (( LINENO++ )) || true

    if [[ $NEXT_IS_RULE -eq 1 ]]; then
        NEXT_IS_RULE=0
        # Rule line is ACTIVE if it does NOT start with optional whitespace + #
        if ! [[ "$line" =~ ^[[:space:]]*# ]]; then
            echo "[hijack-check] 🚨 Active rule at line $LINENO: $line"
            ACTIVE_LINES+=("$LINENO")
            FOUND_HIJACK=1
        else
            echo "[hijack-check] ✅ Rule at line $LINENO is safely commented out."
        fi
    fi

    # Detect the # TRANSLATION_RULE header (tolerates surrounding spaces)
    if [[ "$line" =~ ^[[:space:]]*#[[:space:]]*TRANSLATION_RULE[[:space:]]*$ ]]; then
        echo "[hijack-check] Found TRANSLATION_RULE header at line $LINENO"
        NEXT_IS_RULE=1
    fi

done < "$FUZZY_MAP"

# ---------------------------------------------------------------------------
# 5. Act on results
# ---------------------------------------------------------------------------
if [[ $FOUND_HIJACK -eq 0 ]]; then
    echo "[hijack-check] ✅ No active TRANSLATION_RULE found — all clear."
    exit 0
fi

SHORT_PATH="...${FUZZY_MAP: -50}"

if [[ $TEST_MODE -eq 0 ]]; then
    # Real commit — unstage the file, let the commit proceed with other files
    git reset HEAD "$FUZZY_MAP" 2>/dev/null
    ACTION_MSG="The file was automatically removed from this commit.
   Your other staged files are committed normally."
else
    # Test run — never touch the staging area
    ACTION_MSG="TEST MODE: file was NOT unstaged (dry run only)."
fi

echo ""
echo "============================================================"
echo "⚠️   TRANSLATOR HIJACK DETECTED — file auto-unstaged"
echo "============================================================"
echo "   File : $SHORT_PATH"
for lineno in "${ACTIVE_LINES[@]}"; do
    echo "   Line : $lineno  ← un-commented TRANSLATION_RULE"
done
echo ""
echo "   $ACTION_MSG"
echo ""
echo "   This rule auto-translates user input for ALL users after"
echo "   install — it is a dev-only setting. Comment it out when"
echo "   you are done testing:"
echo ""
echo "       # TRANSLATION_RULE"
echo "       # ('hallo', 'hello'),   ← add the leading #"
echo "============================================================"
echo ""

# Exit 0 — commit is NOT blocked, proceeds without this file
exit 0
