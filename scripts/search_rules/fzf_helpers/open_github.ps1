# scripts/search_rules/fzf_helpers/open_github.ps1
param(
    [string]$file,
    [string]$line,
    [string]$repo
)
# Make the path relative to project root (adjust $projectRoot if needed)
$projectRoot = "C:\stt1\STT"  # oder dynamisch setzen
$rel = $file.Replace($projectRoot + [IO.Path]::DirectorySeparatorChar, '').Replace('\','/')
$url = "$repo/$rel#L$line"
Start-Process $url
