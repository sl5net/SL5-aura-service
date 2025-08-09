# cleanup of failed github workflow
echo "--> Searching for all failed workflow runs..."

gh run list --status=failure --limit=500 --json databaseId --jq '.[].databaseId' | \
while read run_id; do
  echo "Deleting failed run ID: $run_id"
  # gh run delete "$run_id" # This is commented out for safety
  gh run delete "$run_id"
done

echo "--> Cleanup of failed github failed workflow runs complete."
