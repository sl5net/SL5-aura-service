# Test preview helper manually
# powershell -NoProfile -File ".\scripts\search_rules\fzf_helpers\preview.ps1" "C:\stt1\STT\config\maps\somefile.py" 12

param(
    [string]$file,
    [int]$line
)
$lines = Get-Content -LiteralPath $file -ErrorAction SilentlyContinue
if (-not $lines) { return }
$start = [Math]::Max(0, $line - 6)
$end   = [Math]::Min($lines.Count - 1, $line + 4)
for ($i = $start; $i -le $end; $i++) {
    if ($i -eq $line - 1) {
        Write-Output ("> {0,4}: {1}" -f ($i + 1), $lines[$i])
    } else {
        Write-Output ("  {0,4}: {1}" -f ($i + 1), $lines[$i])
    }
}
