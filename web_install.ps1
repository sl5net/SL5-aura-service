$ErrorActionPreference = 'Stop'

$appName = "sl5-aura-service"
$installDir = Join-Path $env:LOCALAPPDATA $appName
$repoBranch = if ($env:AURA_BRANCH) { $env:AURA_BRANCH } else { "master" }
$zipUrl = "https://github.com/sl5net/SL5-aura-service/archive/$repoBranch.zip"
$tempZip = Join-Path $env:TEMP "$appName-master.zip"
$tempExtract = Join-Path $env:TEMP "$appName-extract"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   SL5 Aura Service - Windows Web Setup     " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "[INFO] Installation target: $installDir"
Write-Host "[INFO] Alternative setups are available in setup/"

if (Test-Path $tempExtract) {
    Remove-Item -Recurse -Force $tempExtract
}
if (Test-Path $tempZip) {
    Remove-Item -Force $tempZip
}

#Write-Host "[INFO] Downloading latest repository archive…"
#Invoke-RestMethod -Uri $zipUrl -OutFile $tempZip


$headers = @{}
$token = if ($env:GITHUB_TOKEN) { $env:GITHUB_TOKEN } else { $env:GH_TOKEN }
if ($token) {
    $headers["Authorization"] = "Bearer $token"
}

$urlsToTry = @(
    "https://github.com/sl5net/SL5-aura-service/archive/refs/heads/$repoBranch.zip",
    "https://github.com/sl5net/SL5-aura-service/archive/refs/tags/$repoBranch.zip",
    "https://github.com/sl5net/SL5-aura-service/archive/refs/heads/master.zip"
)

$downloadSuccess = $false
foreach ($url in $urlsToTry) {
    try {
        Write-Host "[INFO] Trying to download archive from $url"
        Invoke-RestMethod -Uri $url -OutFile $tempZip -Headers $headers
        $downloadSuccess = $true
        break
    } catch {
        Write-Host "[WARN] Download failed for $url"
    }
}

if (-not $downloadSuccess) {
    throw "Failed to download repository archive from all candidate URLs."
}


Write-Host "[INFO] Extracting archive…"
Expand-Archive -Path $tempZip -DestinationPath $tempExtract -Force

$extractedRoot = Get-ChildItem -Path $tempExtract -Directory | Select-Object -First 1
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

Copy-Item -Path "$($extractedRoot.FullName)\*" -Destination $installDir -Recurse -Force

Remove-Item -Force $tempZip
Remove-Item -Recurse -Force $tempExtract

Write-Host "[INFO] Launching Windows setup…" -ForegroundColor Green
Set-Location -Path $installDir

$batPath = Join-Path $installDir "setup\windows11_setup.bat"
if (Test-Path $batPath) {
    & cmd.exe /c $batPath
} else {
    $ps1Path = Join-Path $installDir "setup\windows11_setup.ps1"
    & powershell.exe -ExecutionPolicy Bypass -File $ps1Path
}
