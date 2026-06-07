# s.ps1
param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$ArgsList
)
$query = $ArgsList -join " "
if (-not $query) {
    Write-Host "question <your question>"
    exit 1
}

$tmp_dir = "C:\tmp"
$pointerFile = "$tmp_dir\sl5_aura\sl5net_aura_project_root"
$PROJECT_ROOT = (Get-Content -Path $pointerFile -Raw).Trim()

$env:PYTHONUTF8 = "1"
$env:PYTHONPATH = $PROJECT_ROOT
$rootFile = $PROJECT_ROOT

$pyExec = "$PROJECT_ROOT\.venv\Scripts\python.exe"
$cliScript = "$PROJECT_ROOT\scripts\py\cli_client.py"

Write-Host "Setze PYTHONPATH auf: $env:PYTHONPATH"
Write-Host "Starte Python mit: $pyExec"

# Helper function to run the python query with a native PowerShell timeout
function Invoke-AuraQuery($timeout) {
    $job = Start-Job -ScriptBlock {
        param($py, $script, $q)
        & $py -u $script $q --lang "de-DE" --unmasked 2>&1
    } -ArgumentList $pyExec, $cliScript, $query

    $completed = Wait-Job $job -Timeout $timeout
    $out = if ($completed) { Receive-Job $job } else { Stop-Job $job; $null }
    Remove-Job $job
    return @(if ($completed) { 0 } else { 124 }, ($out -join "`n"))
}


# 1. Microsecond TCP port check to detect offline API instantly
$socket = New-Object System.Net.Sockets.TcpClient
$apiOpen = $false
try {
    $socket.Connect("127.0.0.1", 8830)
    if ($socket.Connected) {
        $apiOpen = $true
    }
    $socket.Close()
} catch {
    $apiOpen = $false
}

# 2. Wake up API on-demand if port 8830 is closed
if (-not $apiOpen) {
    Write-Host "Aura API is offline. Waking up background services..."
    $startScript = "$PROJECT_ROOT\scripts\py\start_uvicorn_service.py"
    if (Test-Path $startScript) {
        # Start the Uvicorn/FastAPI service silently in the background
        # Start-Process -FilePath $pyExec -ArgumentList $startScript -NoNewWindow

#       Start-Process -FilePath $pyExec -ArgumentList "-X utf8 `"$startScript`"" -NoNewWindow -WorkingDirectory $PROJECT_ROOT
        Start-Process -FilePath $pyExec -ArgumentList "-X utf8 `"$startScript`"" -NoNewWindow -WorkingDirectory $PROJECT_ROOT

        Start-Sleep -Seconds 2
    } else {
        Write-Host "Error: Uvicorn startup script not found."
        exit 1
    }
}

# 1. Try with short timeout (2 seconds)
$res = Invoke-AuraQuery 2
$exitCode = $res[0]
$output = $res[1]


if ($exitCode -eq 0) {
    Write-Host $output
    exit 0
}

# 2. Try with long timeout (70 seconds) if first run timed out
Write-Host "answer > 2 sec. setting Timeout = 70 s..."
$resLong = Invoke-AuraQuery 70
Write-Host $resLong[1]
if ($resLong[0] -ne 0) {
    Write-Host "WARNING: Timeout > 70 seconds."
}
exit 0
