# search_rules.ps1
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# fzf for Windows: To make the script work, you will need to have fzf installed on
# your Windows machine (you can get it via scoop install fzf, choco install fzf, or by downloading the .exe).


# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
$HISTORY_FILE = "$HOME\.search_rules_history"
$DEFAULT_QUERY = ".py pre # EXAMPLE:"
$REPO_URL = "https://github.com/sl5net/SL5-aura-service/blob/master"

# -----------------------------------------------------------------------------
# EDITOR FALLBACK LOGIC
# -----------------------------------------------------------------------------
function Get-PreferredEditor {
    if (Get-Command "kate.exe" -ErrorAction SilentlyContinue) { return "kate" }
    if (Get-Command "code" -ErrorAction SilentlyContinue) { return "code" }
    return "notepad.exe"
}

$PREFERRED_EDITOR = Get-PreferredEditor

function logger_info {
    param($msg)
    Write-Host "INFO: $msg" -ForegroundColor Cyan
}

logger_info "Initializing search_rules.ps1..."

# -----------------------------------------------------------------------------
# SETUP PATHS
# -----------------------------------------------------------------------------
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Definition
# PROJECT_ROOT is two levels up from script dir based on your bash script
$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)
$MAPS_DIR = Join-Path $PROJECT_ROOT "config\maps"

logger_info "Editor configured: $PREFERRED_EDITOR"
logger_info "Target maps directory: $MAPS_DIR"

if (-not (Get-Command "fzf" -ErrorAction SilentlyContinue)) {
    logger_info "Error: fzf is not installed. Please install it (e.g., scoop install fzf)."
    exit 1
}

if (-not (Test-Path $MAPS_DIR)) {
    logger_info "Error: Maps directory not found at $MAPS_DIR"
    exit 1
}

# -----------------------------------------------------------------------------
# PREVIEW COMMAND
# -----------------------------------------------------------------------------
# We use a PowerShell one-liner for the preview to replace awk.
# It reads the file, skips to the target line area, and adds the ">" marker.
$PREVIEW_CMD = 'powershell -NoProfile -Command "' +
    '$line = {2}; $file = ''{1}''; ' +
    'Get-Content $file | ForEach-Object -Begin {$i=1} -Process {' +
    '  if ($i -gt ($line-5) -and $i -lt ($line+5)) {' +
    '    $mark = if ($i -eq $line) {\">\"} else {\" \"};' +
    '    \"{0}{1,4}: {2}\" -f $mark, $i, $_' +
    '  }; $i++' +
    '}"'

# -----------------------------------------------------------------------------
# HISTORY LOGIC
# -----------------------------------------------------------------------------
$INITIAL_QUERY = $DEFAULT_QUERY
if (Test-Path $HISTORY_FILE) {
    $LastEntry = Get-Content $HISTORY_FILE | Select-Object -Last 1
    if ($null -ne $LastEntry -and $LastEntry -ne "") {
        $INITIAL_QUERY = $LastEntry
    }
}

logger_info "Starting interactive search..."

# -----------------------------------------------------------------------------
# SEARCH & SELECT
# -----------------------------------------------------------------------------
# Note: Using Select-String as a native replacement for grep -r
# We format it to match the file:line:text format fzf expects
$SearchData = Get-ChildItem -Path $MAPS_DIR -Recurse -File |
              Select-String -Pattern ".*" |
              ForEach-Object { "$($_.Path):$($_.LineNumber):$($_.Line)" }

$SELECTED_LINE = $SearchData | fzf --delimiter ":" `
    --history "$HISTORY_FILE" `
    --query "$INITIAL_QUERY" `
    --bind 'ctrl-c:cancel' `
    --bind 'ctrl-z:previous-history' `
    --bind 'ctrl-y:next-history' `
    --bind 'ctrl-p:previous-history' `
    --bind 'ctrl-n:next-history' `
    --bind 'ctrl-a:select-all' `
    --bind 'ctrl-left:backward-word' `
    --bind 'ctrl-right:forward-word' `
    --bind 'ctrl-backspace:backward-kill-word' `
    --bind 'ctrl-delete:kill-word' `
    --bind "ctrl-g:execute-silent(powershell -NoProfile -Command ""$f = '{1}'; `$rel = `$f.Replace('$PROJECT_ROOT', '').Replace('\', '/').TrimStart('/'); Start-Process '$REPO_URL/`$rel#L{2}'"")" `
    --preview $PREVIEW_CMD `
    --preview-window="up:50%"

# -----------------------------------------------------------------------------
# EXECUTION
# -----------------------------------------------------------------------------
if ($null -ne $SELECTED_LINE -and $SELECTED_LINE -ne "") {
    $parts = $SELECTED_LINE.Split(":")
    $FILE_PATH = $parts[0]
    $LINE_NUM = $parts[1]

    logger_info "Opening: $FILE_PATH at line $LINE_NUM"

    if ($PREFERRED_EDITOR -eq "kate") {
        Start-Process "kate" "--line $LINE_NUM $FILE_PATH"
    } elseif ($PREFERRED_EDITOR -eq "code") {
        Start-Process "code" "-g `"$FILE_PATH:$LINE_NUM`""
    } else {
        Start-Process "notepad.exe" "`"$FILE_PATH`""
    }
    exit 0
} else {
    logger_info "No selection made."
}
