# scripts\search_rules\debug\win_test\pull_and_test.ps1
while ($true) {
    Clear-Host
    # Write-Host "=== [$(Get-Date -Format 'HH:mm:ss')] Starting Update & Test Cycle ===" -ForegroundColor Cyan

    # Write-Host "1. Running git pull..." -ForegroundColor Yellow
    git pull

    # Write-Host "2. Running CopyQ test script..." -ForegroundColor Yellow
    & "C:\Program Files\CopyQ\copyq.exe" eval (Get-Content -Raw -Path scripts\search_rules\debug\win_test\test_win_v1.js)

    # Write-Host "3. Verification log:" -ForegroundColor Yellow
    if (Test-Path C:\tmp\copyq_debug.txt) {
        Get-Content C:\tmp\copyq_debug.txt
        Remove-Item C:\tmp\copyq_debug.txt -Force
    } else {
        Write-Host "Warning: C:\tmp\copyq_debug.txt was not created. CopyQ script failed or crashed." -ForegroundColor Red
    }

    Write-Host "Waiting 10 seconds..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}
