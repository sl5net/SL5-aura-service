# scripts/search_rules/search_rules.ps1
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
param(
    [string]$MAPS_DIR = ""
)

# -----------------------------------------------------------------------------
# CONFIGURATION & DEFAULTS
# -----------------------------------------------------------------------------
$HOME = [Environment]::GetFolderPath("UserProfile")
$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)

# MAPS_DIR priority: param > env MAPS_DIR > default relative to project root
if (-not $MAPS_DIR) { $MAPS_DIR = $env:MAPS_DIR }
if (-not $MAPS_DIR) { $MAPS_DIR = Join-Path $PROJECT_ROOT "config\maps" }
$MAPS_DIR = (Resolve-Path -Path $MAPS_DIR -ErrorAction SilentlyContinue).ProviderPath
if (-not $MAPS_DIR) {
    Write-Error "MAPS_DIR not found: $MAPS_DIR"
    exit 1
}

$HISTORY_FILE   = Join-Path $HOME ".search_rules_history"
$DEFAULT_QUERY  = ".py pre # EXAMPLE:"
$SEARCH_CLOSE_ON_OPEN = $env:SEARCH_CLOSE_ON_OPEN
if (-not $SEARCH_CLOSE_ON_OPEN) { $SEARCH_CLOSE_ON_OPEN = "True" }

try {

# Try to detect repo URL for GitHub open (prefer git remote)
$REPO_URL = $env:GITHUB_BASE_URL
if (-not $REPO_URL) {
    try {
        $remote = git -C $PROJECT_ROOT remote get-url origin 2>$null
        if ($remote) {
            # Convert git@github.com:org/repo.git to https://github.com/org/repo/blob/master
            if ($remote -match "^git@github\.com:(.+)\.git$") {
                $repoPath = $Matches[1]
                $REPO_URL = "https://github.com/$repoPath/blob/master"
            } elseif ($remote -match "github\.com/.+/.+(\.git)?$") {
                $repoHttp = $remote -replace "\.git$","" -replace "^git@github\.com:","https://github.com/" -replace "^https://","https://"
                $REPO_URL = "$repoHttp/blob/master"
            }
        }
    } catch { }
}
if (-not $REPO_URL) { $REPO_URL = "https://github.com/unknown/unknown/blob/master" }

function logger_info { param($m) Write-Host "INFO: $m" -ForegroundColor Cyan }

logger_info "Initializing search_rules.ps1..."
logger_info "Project root: $PROJECT_ROOT"
logger_info "Target maps dir: $MAPS_DIR"

# -----------------------------------------------------------------------------
# EDITOR FALLBACK LOGIC
# -----------------------------------------------------------------------------
function Get-PreferredEditor {
    if (Get-Command "kate.exe" -ErrorAction SilentlyContinue) { return "kate.exe" }
    if (Get-Command "code.cmd" -ErrorAction SilentlyContinue) { return "code" }
    if (Get-Command "code" -ErrorAction SilentlyContinue) { return "code" }
    if (Get-Command "nano" -ErrorAction SilentlyContinue) { return "nano" }
    return "notepad.exe"
}
$EDITOR = Get-PreferredEditor()
logger_info "Editor configured: $EDITOR"

if (-not (Get-Command "fzf.exe" -ErrorAction SilentlyContinue)) {
    Write-Error "fzf.exe not found in PATH. Please install fzf."
    exit 1
}

# -----------------------------------------------------------------------------
# INITIAL QUERY / HISTORY
# -----------------------------------------------------------------------------
$QUERY = $DEFAULT_QUERY
if (Test-Path $HISTORY_FILE) {
    $last = Get-Content $HISTORY_FILE -ErrorAction SilentlyContinue | Select-Object -Last 1
    if ($last) { $QUERY = $last }
}

# -----------------------------------------------------------------------------
# Prepare Search Data - use Get-ChildItem + Select-String to produce "path:line:content"
# -----------------------------------------------------------------------------
$SearchFilesFilter = $env:SEARCH_FILES_FILTER
if (-not $SearchFilesFilter) { $SearchFilesFilter = "*" } # user can set e.g. "*.py|*.md"

# Build include args for grep-like behavior (fzf --filtering is done by caller; we produce all matches)
$IncludePatterns = @()
foreach ($pat in $SearchFilesFilter -split '\|') {
    if ($pat) { $IncludePatterns += $pat.Trim() }
}

# Gather matches
$SearchData = Get-ChildItem -Path $MAPS_DIR -Recurse -File -Include $IncludePatterns |
    Select-String -Pattern ".*" |
    ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }

if (-not $SearchData) {
    logger_info "No searchable files found in $MAPS_DIR"
    exit 1
}

# -----------------------------------------------------------------------------
# Helper: Preview function content for fzf (PowerShell one-liner)
# -----------------------------------------------------------------------------
# We'll use a small inline powershell command that receives {1}={file} {2}={line}
$PreviewCmd = 'powershell -NoProfile -Command "param($f,$l); $l=[int]$l; Get-Content -Raw -LiteralPath $f -ErrorAction SilentlyContinue -Encoding UTF8 | Out-String | Select-String -Pattern ''(?s).{0,0}'' | Out-Null; $lines=(Get-Content -LiteralPath $f -ErrorAction SilentlyContinue); $start=[Math]::Max(0,$l-6); $end=[Math]::Min($lines.Count-1,$l+4); for ($i=$start; $i -le $end; $i++){ if ($i -eq $l-1) {Write-Output ("> {0,4}: {1}" -f ($i+1), $lines[$i]) } else {Write-Output ("  {0,4}: {1}" -f ($i+1), $lines[$i]) } }" -- '

# -----------------------------------------------------------------------------
# FZF command arguments (with history, preview, binds)
# -----------------------------------------------------------------------------
$fzfArgs = @(
    "--delimiter", ":",
    "--with-nth", "3..",              # show matched line content primarily
    "--query", $QUERY,
    "--history", $HISTORY_FILE,
    "--header", "Enter: Edit | Ctrl+G: GitHub | Ctrl+A: Copy context | Ctrl+X: Copy line",
    "--preview", $PreviewCmd + '{1} {2}',
    "--preview-window", "up:50%"
)

# Bind keys:
# - ctrl-z / ctrl-y history navigation (fzf builtin names: previous-history/next-history)
# - ctrl-g: open GitHub (execute-silent Start-Process)
# - ctrl-x: copy whole matched line to clipboard (clip.exe)
# - ctrl-a: copy preview context (we use the same preview code to output to clipboard)
$binds = @()
$binds += "ctrl-z:previous-history"
$binds += "ctrl-y:next-history"
# ctrl-g: open github in background
$openGithubCmd = "execute-silent(powerShell -NoProfile -Command `"param(\$f,\$l,\$repo) \$rel = (Resolve-Path -LiteralPath \$f).ProviderPath.Replace((Resolve-Path -LiteralPath '$PROJECT_ROOT').ProviderPath + [System.IO.Path]::DirectorySeparatorChar,''); \$url = '{0}' -f (\$repo + '/' + \$rel -replace '\\','/' + '#L' + \$l); Start-Process \$url`" -f $REPO_URL
$binds += "ctrl-g:$openGithubCmd"
# ctrl-x: copy line
$binds += "ctrl-x:execute-silent(echo {3..} | clip.exe)"
# ctrl-a: copy preview context
$binds += "ctrl-a:execute-silent(powershell -NoProfile -Command {0})" -f ('"{0} {1} | clip.exe"' -f $PreviewCmd.TrimEnd(' '), '{1} {2}')

$fzfArgs += @("--bind", ($binds -join ","))


# -----------------------------------------------------------------------------
# Interactive loop
# -----------------------------------------------------------------------------
while ($true) {
    $SELECTED_LINE = $SearchData | fzf.exe @fzfArgs

    if (-not $SELECTED_LINE) {
        logger_info "No selection made. Exiting."
        break
    }

    # append to history file
    $SELECTED_LINE | Out-File -FilePath $HISTORY_FILE -Append -Encoding UTF8

    # parse path:line:content
    if ($SELECTED_LINE -match '^([A-Za-z]:\\.+?):(\d+):(.*)$' -or $SELECTED_LINE -match '^(.+?):(\d+):(.*)$') {
        $FILE_PATH = $Matches[1]
        $LINE_NUM  = [int]$Matches[2]
        logger_info "Selected: $FILE_PATH:$LINE_NUM"

        # extension based binary check
        $ext = [System.IO.Path]::GetExtension($FILE_PATH).TrimStart('.').ToLower()
        $binExts = "pdf","png","jpg","jpeg","gif","webp","mp4","mp3","zip","tar","gz","7z","exe","dll"
        $isBinary = $false
        if ($binExts -contains $ext) { $isBinary = $true }

        # best-effort mime check: try 'file' from WSL if present
        try {
            $fileCmd = Get-Command file -ErrorAction SilentlyContinue
            if ($fileCmd) {
                $mime = (& file --mime-type -b -- "$FILE_PATH") 2>$null
                if ($mime -and $mime -notmatch '^text/') { $isBinary = $true }
            }
        } catch { }

        if ($isBinary) {
            logger_info "Binary detected, opening with system default viewer..."
            Start-Process -FilePath $FILE_PATH
        } else {
            # open in editor at line if supported
            switch ($EDITOR) {
                "kate.exe" { Start-Process "kate.exe" -ArgumentList "--line",$LINE_NUM,"`"$FILE_PATH`"" }
                "code"      { Start-Process "code" -ArgumentList "--goto","$FILE_PATH`:$LINE_NUM" }
                "nano"      { # try opening in Windows Terminal / WSL? fallback: open notepad if not available
                    if (Get-Command "wt.exe" -ErrorAction SilentlyContinue) {
                        Start-Process "wt.exe" -ArgumentList "powershell -NoProfile -Command nano `"$FILE_PATH`""
                    } else {
                        Start-Process "notepad.exe" -ArgumentList "`"$FILE_PATH`""
                    }
                }
                default     { Start-Process $EDITOR -ArgumentList "`"$FILE_PATH`"" }
            }
        }

        if ($SEARCH_CLOSE_ON_OPEN -eq "True") { break }
        else { Start-Sleep -Milliseconds 300 } # small sleep then reopen fzf
    } else {
        logger_info "Could not parse selection: $SELECTED_LINE"
        break
    }
}


} catch {
    logger_info  "UNHANDLED ERROR: $($_.Exception.Message)"
    logger_info  "STACK: $($_.Exception.StackTrace)"
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press ENTER to exit (debug)"
    exit 1
}


logger_info "Done."
