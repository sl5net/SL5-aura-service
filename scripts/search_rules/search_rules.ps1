# search_rules.ps1
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
$HISTORY_FILE   = "$HOME\.search_rules_history"
$DEFAULT_QUERY  = ".py pre # EXAMPLE:"

# -----------------------------------------------------------------------------
# EDITOR FALLBACK LOGIC
# -----------------------------------------------------------------------------
function Get-PreferredEditor {
    if (Get-Command "kate.exe" -ErrorAction SilentlyContinue) { return "kate.exe" }
    if (Get-Command "code.cmd" -ErrorAction SilentlyContinue) { return "code" }
    if (Get-Command "code" -ErrorAction SilentlyContinue) { return "code" }
    return "notepad.exe"
}
$EDITOR = Get-PreferredEditor

function logger_info { param($msg); Write-Host "INFO: $msg" -ForegroundColor Cyan }

logger_info "Initializing search_rules.ps1..."

# -----------------------------------------------------------------------------
# SETUP PATHS
# -----------------------------------------------------------------------------
$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)
$MAPS_DIR     = Join-Path $PROJECT_ROOT "config\maps"

if (-not (Get-Command "fzf.exe" -ErrorAction SilentlyContinue)) {
    Write-Error "fzf.exe not found in PATH."
    exit 1
}

# -----------------------------------------------------------------------------
# SIMPLE HISTORY LOGIC
# -----------------------------------------------------------------------------
$QUERY = $DEFAULT_QUERY
if (Test-Path $HISTORY_FILE) {
    $last = Get-Content $HISTORY_FILE | Select-Object -Last 1
    if ($last) { $QUERY = $last }
}

# -----------------------------------------------------------------------------
# DATA GATHERING
# -----------------------------------------------------------------------------
logger_info "Scanning $MAPS_DIR ..."
$SearchData = Get-ChildItem -Path $MAPS_DIR -Recurse -File |
              Select-String -Pattern ".*" |
              ForEach-Object { "$($_.Path):$($_.LineNumber):$($_.Line)" }

# -----------------------------------------------------------------------------
# EXECUTE FZF (Minimum Arguments)
# -----------------------------------------------------------------------------
# We use simple string variables to avoid parsing errors.
$SELECTED_LINE = $SearchData | fzf.exe --delimiter ":" --query "$QUERY"

# -----------------------------------------------------------------------------
# RESULT PROCESSING
# -----------------------------------------------------------------------------
if ($SELECTED_LINE) {
    # Save selection to history file (simple way)
    $SELECTED_LINE | Out-File -FilePath $HISTORY_FILE -Append

    # Parse Windows Path (C:\...), Line, and Text
    if ($SELECTED_LINE -match '^([a-zA-Z]:[^:]+):(\d+):(.*)$') {
        $FILE_PATH = $Matches[1]
        $LINE_NUM  = $Matches[2]

        logger_info "Opening: $FILE_PATH at line $LINE_NUM"

        if ($EDITOR -eq "kate.exe") {
            Start-Process "kate.exe" -ArgumentList "--line", $LINE_NUM, "`"$FILE_PATH`""
        } elseif ($EDITOR -eq "code") {
            Start-Process "code" -ArgumentList "-g", "`"${FILE_PATH}:${LINE_NUM}`""
        } else {
            Start-Process "notepad.exe" -ArgumentList "`"$FILE_PATH`""
        }
    }
} else {
    logger_info "No selection made."
}
