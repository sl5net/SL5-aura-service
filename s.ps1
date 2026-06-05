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

# Resolve project root dynamically from the bootstrap pointer
$rootFile = "C:\tmp\sl5_aura\sl5net_aura_project_root"

$projectRoot = if (Test-Path $rootFile) {
    $rawPath = (Get-Content $rootFile).Trim()
    # If the path ends with \setup, dynamically resolve the parent directory
    if ($rawPath.EndsWith("\setup")) { Split-Path -Parent $rawPath } else { $rawPath }
} else {
    $PSScriptRoot
}

$pyExec = "$projectRoot\.venv\Scripts\python.exe"
$cliScript = "$projectRoot\scripts\py\cli_client.py"

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

# 1. Try with short timeout (2 seconds)
$res = Invoke-AuraQuery 2
$exitCode = $res[0]
$output = $res[1]

# Service Check: Verify if connection failed or if Streamlit is missing
$engineProc = Get-Process -Name "python" -ErrorAction SilentlyContinue |
    Where-Object { $_.CommandLine -like "*aura_engine.py*" }

if ($output -like "*Verbindungsfehler*" -or -not $engineProc) {
    Write-Host "Service-Check: Backend or Frontend missing. Restarting..."
    & "$projectRoot\setup\windows11_setup_with_ahk_copyq_fzf_glogg.bat"

    $kiwix = "$projectRoot\config\maps\plugins\standard_actions\wikipedia_local\de-DE\kiwix-docker-start-if-not-running.sh"
    if (Test-Path $kiwix) { bash $kiwix }

    Write-Host "--------------------------------------------------"
    Write-Host "PLEASE RE-ENTER: s $query"
    exit 1
}

if ($exitCode -eq 0) {
    Write-Host $output
    exit 0
}

# 2. Try with long timeout (70 seconds)
Write-Host "answer > 2 sec. setting Timeout = 70 s..."
$resLong = Invoke-AuraQuery 70
Write-Host $resLong[1]
if ($resLong[0] -ne 0) {
    Write-Host "WARNING: Timeout > 70 seconds."
}
exit 0
