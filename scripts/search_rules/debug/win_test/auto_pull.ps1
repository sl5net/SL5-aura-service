# scripts\search_rules\debug\win_test\pull_and_test.ps1
while ($true) {
    git pull
    Write-Host "Waiting 10 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}
