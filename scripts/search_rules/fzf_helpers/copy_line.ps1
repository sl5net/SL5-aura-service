# scripts/search_rules/fzf_helpers/copy_line.ps1
param(
    [string]$file,
    [string]$line,
    [string]$text  # fzf liefert {3..} als drittes Argument (joined fields)
)

# Falls $text leer ist, erzeuge es aus Datei und Zeile
if (-not $text -or $text -eq '') {
    try {
        $l = [int]$line
        $lines = Get-Content -LiteralPath $file -ErrorAction Stop
        $text = $lines[$l - 1].Trim()
    } catch {
        # fallback: build a short description
        $text = "$file:$line"
    }
}

# Set clipboard (PowerShell builtin)
$text | Set-Clipboard
