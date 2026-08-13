#!/usr/bin/env bash
# Diagnosis script for Sphinx docs build failure after subdirectory move
# Run from repository root

OUTPUT_FILE="docs_diagnosis_report.txt"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Clear previous report
echo "Documentation Build Failure Diagnosis Report" > "$OUTPUT_FILE"
echo "Generated: $TIMESTAMP" >> "$OUTPUT_FILE"
echo "========================================" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 1. Git repository info
echo "SECTION 1: GIT REPOSITORY INFO" >> "$OUTPUT_FILE"
echo "------------------------------" >> "$OUTPUT_FILE"
echo "Remote URL:" >> "$OUTPUT_FILE"
git remote -v 2>/dev/null >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Current branch:" >> "$OUTPUT_FILE"
git branch --show-current 2>/dev/null >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Last 10 commits:" >> "$OUTPUT_FILE"
git log --oneline -10 2>/dev/null >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 2. Find commit nearest to move time (2026-08-13 14:00)
echo "SECTION 2: COMMIT NEAR MOVE TIME (2026-08-13 14:00)" >> "$OUTPUT_FILE"
echo "---------------------------------------------------" >> "$OUTPUT_FILE"
if [ -f "./tools/find-nearest-commit.sh" ]; then
    ./tools/find-nearest-commit.sh "2026-08-13 14:00" >> "$OUTPUT_FILE" 2>&1
else
    echo "find-nearest-commit.sh not found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 3. Git diff of workflow file since move
echo "SECTION 3: WORKFLOW FILE HISTORY" >> "$OUTPUT_FILE"
echo "--------------------------------" >> "$OUTPUT_FILE"
WORKFLOW_FILE=$(find .github/workflows -name "*deploy*doc*" -o -name "*docs*" 2>/dev/null | head -n 1)
if [ -n "$WORKFLOW_FILE" ]; then
    echo "Workflow file: $WORKFLOW_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "Current content:" >> "$OUTPUT_FILE"
    cat "$WORKFLOW_FILE" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    echo "Git log for this file:" >> "$OUTPUT_FILE"
    git log --oneline -5 -- "$WORKFLOW_FILE" 2>/dev/null >> "$OUTPUT_FILE"
else
    echo "No workflow file found matching *deploy*doc* or *docs*" >> "$OUTPUT_FILE"
    echo "All workflow files:" >> "$OUTPUT_FILE"
    find .github/workflows -type f 2>/dev/null >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 4. doc_sources directory structure
echo "SECTION 4: DOC_SOURCES STRUCTURE" >> "$OUTPUT_FILE"
echo "--------------------------------" >> "$OUTPUT_FILE"
if [ -d "doc_sources" ]; then
    find doc_sources -maxdepth 3 -type f | sort >> "$OUTPUT_FILE"
else
    echo "doc_sources directory not found" >> "$OUTPUT_FILE"
    echo "Directories in root:" >> "$OUTPUT_FILE"
    ls -la >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 5. Sphinx conf.py
echo "SECTION 5: SPHINX CONF.PY" >> "$OUTPUT_FILE"
echo "-------------------------" >> "$OUTPUT_FILE"
if [ -f "doc_sources/conf.py" ]; then
    cat "doc_sources/conf.py" >> "$OUTPUT_FILE"
else
    echo "doc_sources/conf.py not found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 6. Sphinx Makefile
echo "SECTION 6: SPHINX MAKEFILE" >> "$OUTPUT_FILE"
echo "--------------------------" >> "$OUTPUT_FILE"
if [ -f "doc_sources/Makefile" ]; then
    cat "doc_sources/Makefile" >> "$OUTPUT_FILE"
else
    echo "doc_sources/Makefile not found" >> "$OUTPUT_FILE"
fi
echo "" >> "$OUTPUT_FILE"

# 7. Local Python environment
echo "SECTION 7: LOCAL PYTHON ENVIRONMENT" >> "$OUTPUT_FILE"
echo "-----------------------------------" >> "$OUTPUT_FILE"
echo "Python version:" >> "$OUTPUT_FILE"
python3 --version 2>/dev/null >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "Installed sphinx packages:" >> "$OUTPUT_FILE"
pip list 2>/dev/null | grep -i -E "(sphinx|furo|myst|docutils)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "furo import test:" >> "$OUTPUT_FILE"
python3 -c "import furo; print('furo location:', furo.__file__)" 2>/dev/null >> "$OUTPUT_FILE" || echo "furo not importable locally" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 8. Git status
echo "SECTION 8: GIT STATUS" >> "$OUTPUT_FILE"
echo "---------------------" >> "$OUTPUT_FILE"
git status >> "$OUTPUT_FILE" 2>/dev/null
echo "" >> "$OUTPUT_FILE"

echo "Report written to: $OUTPUT_FILE"
echo "Please send $OUTPUT_FILE to the specialist."

