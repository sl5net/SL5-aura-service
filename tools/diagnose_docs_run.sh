#!/usr/bin/env bash
set -uo pipefail

RUN_ID="${1:?Usage: tools/diagnose_docs_run.sh RUN_ID}"
LOG_FILE="/tmp/run_${RUN_ID}.log"
OUT_FILE="/tmp/run_${RUN_ID}_summary.txt"

gh run view "$RUN_ID" --log > "$LOG_FILE" || {
  echo "gh run view failed" >&2
  exit 1
}

{
  echo "=== LOG LINE COUNT ==="
  wc -l "$LOG_FILE"

  echo ""
  echo "=== STEP BOUNDARIES ==="
  grep -n -E "Build documentation|Get latest release version|Verify furo installation|Install dependencies" "$LOG_FILE" || echo "no step boundaries matched"

  echo ""
  echo "=== ERROR CONTEXT ==="
  grep -n -i -E "error|traceback|exception|fatal" "$LOG_FILE" | head -50 || echo "no error lines matched"

  echo ""
  echo "=== FULL BUILD DOCUMENTATION STEP ==="
  awk '/Build documentation/{flag=1} /Upload artifact/{flag=0} flag' "$LOG_FILE" || echo "no build step block matched"
} > "$OUT_FILE"

cat "$OUT_FILE"

