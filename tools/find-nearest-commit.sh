#!/usr/bin/env bash
# find-nearest-commit.sh
# Usage: ./find-nearest-commit.sh "YYYY-MM-DD HH:MM"

set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 \"YYYY-MM-DD HH:MM\""
  exit 2
fi

TARGET_STR="$1"

# convert target to unix timestamp (seconds since epoch)
TARGET_TS=$(date -d "$TARGET_STR" +%s) || { echo "Ungültiges Datum: $TARGET_STR"; exit 3; }

# iterate over all commits and print hash + unix timestamp, then find minimal abs diff
# git log --all liefert commits in commit-time Reihenfolge, --format='%H %at' gibt hash und autor-time (unix)
git log --all --pretty=format:"%H %at" |
awk -v target="$TARGET_TS" '
{
  hash=$1; ts=$2;
  diff = ts - target; if(diff<0) diff = -diff;
  if(min=="" || diff < min){ min=diff; best_hash=hash; best_ts=ts }
}
END{
  if(best_hash==""){ print "Kein Commit gefunden" > "/dev/stderr"; exit 1 }
  # Format best_ts lesbar ausgeben
  cmd = "date -d @" best_ts " +\"%Y-%m-%d %H:%M:%S %z\""
  cmd | getline timestr; close(cmd)
  print best_hash, timestr
}'
