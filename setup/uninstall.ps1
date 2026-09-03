<#
.SYNOPSIS
    SL5 Aura Service Uninstaller for Windows
#>

param(
    [switch]$Purge = $false,
    [switch]$Yes = $false
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$PythonScript = Join-Path $ProjectRoot "scripts\py\uninstall.py"

# Try Python execution via virtualenv or system Python
$PythonExe = "python"
if (Test-Path (Join-Path $ProjectRoot ".venv\Scripts\python.exe")) {
    $PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
}

$Arguments = @()
if ($Purge) { $Arguments += "--purge" }
if ($Yes) { $Arguments += "--yes" }

if (Test-Path $PythonScript) {
    & $PythonExe $PythonScript @Arguments
} else {
    Write-Warning "Uninstaller python script not found at $PythonScript"
}
