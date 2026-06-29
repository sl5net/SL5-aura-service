# scripts/search_rules/search_rules.ps1
# CODE_LANGUAGE_DIRECTIVE: ENGLISH_ONLY
param(
    [string]$MAPS_DIR = ""
)

# -----------------------------------------------------------------------------
# CONFIGURATION & DEFAULTS
# -----------------------------------------------------------------------------
$MY_HOME = [Environment]::GetFolderPath("UserProfile")
$SCRIPT_DIR   = Split-Path -Parent $MyInvocation.MyCommand.Definition
$PROJECT_ROOT = Split-Path -Parent (Split-Path -Parent $SCRIPT_DIR)

$ErrorActionPreference = 'Stop'
$LOG_DIR = Join-Path $PROJECT_ROOT "log"
if (-not (Test-Path $LOG_DIR)) { [void](New-Item -ItemType Directory -Path $LOG_DIR -Force) }
$LOGFILE = Join-Path $LOG_DIR "search_rules_ps1_debug.log"
function DBG { param($m) "$(Get-Date -Format o) - $m" | Out-File -FilePath $LOGFILE -Append -Encoding utf8 }

DBG "Script started."
DBG "EXACT RUNNING PATH: $($MyInvocation.MyCommand.Definition)"


$PYTHON_BIN = Join-Path $PROJECT_ROOT ".venv\Scripts\python.exe"
if (-not (Test-Path $PYTHON_BIN)) { $PYTHON_BIN = "python.exe" }
$PYTHONW_BIN = Join-Path $PROJECT_ROOT ".venv\Scripts\pythonw.exe"
if (-not (Test-Path $PYTHONW_BIN)) { $PYTHONW_BIN = $PYTHON_BIN }



# MAPS_DIR priority: param > env MAPS_DIR > default relative to project root
if (-not $MAPS_DIR) { $MAPS_DIR = $env:MAPS_DIR }
if (-not $MAPS_DIR) { $MAPS_DIR = Join-Path $PROJECT_ROOT "config\maps" }
$MAPS_DIR = (Resolve-Path -Path $MAPS_DIR -ErrorAction SilentlyContinue).ProviderPath
if (-not $MAPS_DIR) {
    Write-Error "MAPS_DIR not found: $MAPS_DIR"
    exit 1
}

$HISTORY_FILE   = Join-Path $MY_HOME ".search_rules_history"

# If the file doesn't exist, create an empty UTF8 file (no BOM)
if (-not (Test-Path $HISTORY_FILE)) {
    # On older PowerShell versions -Encoding utf8 may add BOM; try utf8NoBOM when available
    try {
        # pwsh/core supports utf8NoBOM
        "" | Out-File -FilePath $HISTORY_FILE -Encoding utf8NoBOM -Force
    } catch {
        # fallback for Windows PowerShell
        "" | Out-File -FilePath $HISTORY_FILE -Encoding utf8 -Force
    }
}

# Debug: print the path so you can verify (remove in production)
Write-Host "Using history file: $HISTORY_FILE"

$DEFAULT_QUERY  = "# EXAMPLE:"
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
$EDITOR = Get-PreferredEditor
logger_info "Editor configured: $EDITOR"

if (-not (Get-Command "fzf.exe" -ErrorAction SilentlyContinue)) {
    Write-Error "fzf.exe not found in PATH. Please install fzf."
    exit 1
}


# --- Load initial query from history, but ignore overly long / suspicious entries ---
$DEFAULT_QUERY = "# EXAMPLE:"
$QUERY = $DEFAULT_QUERY

# Ensure HISTORY_FILE is set; example: $HISTORY_FILE = Join-Path $PROJECT_ROOT ".search_rules_history"
if (-not $HISTORY_FILE) {
    $HISTORY_FILE = Join-Path $env:USERPROFILE ".search_rules_history"
}

try {
    if (Test-Path $HISTORY_FILE) {
        # Read with UTF-8 (avoid encoding gibberish)
        $lines = Get-Content -Path $HISTORY_FILE -Encoding utf8 -ErrorAction SilentlyContinue
        if ($lines) {
            # Select the last non-empty line
            $last = $lines | Where-Object { $_.Trim().Length -gt 0 } | Select-Object -Last 1
            if ($last) {
                $trimmed = $last.Trim()
                # Only accept history entries of reasonable length
                $maxLen = 60
                if ($trimmed.Length -le $maxLen) {
                    $QUERY = $trimmed
                } else {
                    Write-Verbose "History entry too long ($($trimmed.Length) chars); using default query."
                    $QUERY = $DEFAULT_QUERY
                }
            }
        }
    }
} catch {
    Write-Warning ("Could not read history file {0}: {1}" -f $HISTORY_FILE, $_.Exception.Message)
    $QUERY = $DEFAULT_QUERY
}

Write-Host ("Initial fzf query: {0}" -f $QUERY)




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
#$SearchData = Get-ChildItem -Path $MAPS_DIR -Recurse -File -Include $IncludePatterns |
#    Select-String -Pattern ".*" |
#    ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }

$patterns = @('FUZZY_MAP_pre.py','OTHER_pre.py')
$files = foreach ($p in $patterns) {
    Get-ChildItem -Path $MAPS_DIR -Recurse -Filter $p -File -ErrorAction SilentlyContinue
}
$SearchData = $files | Select-String -Pattern ".*" | ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line.Trim() }

# Teste lokal, ob nur gewünschte Dateien gefunden werden:
# Get-ChildItem -Path $MAPS_DIR -Recurse -Filter 'FUZZY_MAP_pre.py' -File | Select-Object FullName

#Teste die ganze Pipeline:
# Get-ChildItem -Path $MAPS_DIR -Recurse -Filter 'FUZZY_MAP_pre.py' -File |
#  Select-String -Pattern ".*" |
#  ForEach-Object { "{0}:{1}:{2}" -f $_.Path, $_.LineNumber, $_.Line } | Out-Host

if (-not $SearchData) {
    logger_info "No searchable files found in $MAPS_DIR"
    exit 1
}

# -----------------------------------------------------------------------------
# Helper: Preview function content for fzf (PowerShell one-liner)
# -----------------------------------------------------------------------------
# We'll use a small inline powershell command that receives {1}={file} {2}={line}

$helperPreview = Join-Path $SCRIPT_DIR 'fzf_helpers\preview.ps1'
#$fzfArgs += @("--preview", "powershell -NoProfile -File `"$helperPreview`" '{1}' '{2}'", "--preview-window", "up:50%")
#    "--with-nth", "3..",

$fzfArgs = @(
    "--print-query",
    "--expect", "ctrl-r",
    "--delimiter", ":",
    "--with-nth", "4..",
    "--query", $QUERY,
    "--history", $HISTORY_FILE,
    "--header", "Enter: Edit | Ctrl+R: Execute | Ctrl+G: GitHub | Ctrl+A: Copy context | Ctrl+X: Copy line",
    "--preview", "powershell -NoProfile -File `"$helperPreview`" '{1}:{2}' '{3}'",
    "--preview-window", "up:50%"
)

#$PreviewCmd = 'powershell -NoProfile -Command "param($f,$l); $l=[int]$l; Get-Content -Raw -LiteralPath $f -ErrorAction SilentlyContinue -Encoding UTF8 | Out-String | Select-String -Pattern ''(?s).{0,0}'' | Out-Null; $lines=(Get-Content -LiteralPath $f -ErrorAction SilentlyContinue); $start=[Math]::Max(0,$l-6); $end=[Math]::Min($lines.Count-1,$l+4); for ($i=$start; $i -le $end; $i++){ if ($i -eq $l-1) {Write-Output ("> {0,4}: {1}" -f ($i+1), $lines[$i]) } else {Write-Output ("  {0,4}: {1}" -f ($i+1), $lines[$i]) } }" -- '

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





# safe: build binds as literal strings (single quotes) and avoid {3..} expansion by wrapping in single quotes
$binds = @()
# add word-editing keybinds for fzf query line editing
#$binds += 'ctrl-backspace:backward-kill-word' # unsupported key: ctrl-backspace
$binds += 'alt-backspace:backward-kill-word' # cmd.exe: unsupported key
#$binds += 'ctrl-left:backward-word' # cmd.exe: unsupported key
#$binds += 'ctrl-right:forward-word' # cmd.exe: unsupported key
# ctrl-\ as kill-line (note: backslash needs no extra escaping inside single-quoted PS string)
# $binds += 'ctrl-\\:kill-line'  # cmd.exe: unsupported key ctrl-\\
$binds += 'ctrl-z:previous-history'
$binds += 'ctrl-y:next-history'
# ctrl-g: open github (use double quotes inside execute-silent but escape for PS)

#$helperOpenGithub = Join-Path $SCRIPT_DIR 'fzf_helpers\open_github.ps1'
#$binds += "ctrl-g:execute-silent(powershell -NoProfile -File `"$helperOpenGithub`" '{1}' '{2}' '$REPO_URL')"

$helperOpenGithub = Join-Path $SCRIPT_DIR 'fzf_helpers\open_github.ps1'
$binds += "ctrl-g:execute-silent(powershell -NoProfile -File '$helperOpenGithub' '{1}:{2}' '{3}' '$REPO_URL')"

@"
param(\$file,\$line,\$repo)
\$rel = \$file.Replace('$PROJECT_ROOT' + [System.IO.Path]::DirectorySeparatorChar, '').Replace('\\','/')
\$url = \"{0}/\$rel#L\$line\" -f \$repo
Start-Process \$url
"@ | Out-File -FilePath $helperOpenGithub -Encoding utf8

$binds += "ctrl-g:execute-silent(powershell -NoProfile -File `"$helperOpenGithub`" '{1}' '{2}' '$REPO_URL')"

# ctrl-x: copy line -> use Set-Clipboard, keep fzf placeholder {3..} literal by wrapping in single quotes inside the executed PS command
#$helperCopyLine = Join-Path $SCRIPT_DIR 'fzf_helpers\copy_line.ps1'
#$binds += "ctrl-x:execute-silent(powershell -NoProfile -File `"$helperCopyLine`" '{1}' '{2}' '{3..}')"

$helperCopyLine = Join-Path $SCRIPT_DIR 'fzf_helpers\copy_line.ps1'
$binds += "ctrl-x:execute-silent(powershell -NoProfile -File '$helperCopyLine' '{1}:{2}' '{3}' '{4..}')"

# ctrl-a: copy preview/context -> call helper to extract context and pipe to clipboard
#$helperCopyPreview = Join-Path $SCRIPT_DIR 'fzf_helpers\copy_preview.ps1'

# ctrl-a: copy preview/context
$helperCopyPreview = Join-Path $SCRIPT_DIR 'fzf_helpers\copy_preview.ps1'
$binds += "ctrl-a:execute-silent(powershell -NoProfile -File '$helperCopyPreview' '{1}:{2}' '{3}')"

@"
param(\$file,\$line)
\$l = [int]\$line
\$lines = Get-Content -LiteralPath \$file -ErrorAction SilentlyContinue
\$start = [Math]::Max(0,\$l-6)
\$end = [Math]::Min(\$lines.Count-1,\$l+4)
\$out = for (\$i=\$start; \$i -le \$end; \$i++) {
    if (\$i -eq \$l-1) { \"> {0,4}: {1}\" -f (\$i+1), \$lines[\$i] } else { \"  {0,4}: {1}\" -f (\$i+1), \$lines[\$i] }
}
\$out -join \"`n\" | Set-Clipboard
"@ | Out-File -FilePath $helperCopyPreview -Encoding utf8

$binds += "ctrl-a:execute-silent(powershell -NoProfile -File `"$helperCopyPreview`" '{1}' '{2}')"




$fzfArgs += @("--bind", ($binds -join ","))


#------------------------------------------------------------------------
# Interactive loop
#------------------------------------------------------------------------

while ($true) {
    # Out-String bewahrt alle Roh-Newlines und Leerzeilen der FZF-Ausgabe
    $F_OUT_RAW = $SearchData | fzf.exe @fzfArgs | Out-String
    if ($LASTEXITCODE -eq 130 -or [string]::IsNullOrEmpty($F_OUT_RAW)) {
        DBG "DEBUG: FZF cancelled or returned empty."
        break
    }


    # Explizites Aufsplitten stellt sicher, dass Leerzeilen als leere Strings im Array verbleiben
    $F_OUT = $F_OUT_RAW -split '\r?\n'

    $QUERY_TYPED   = if ($F_OUT.Count -gt 0) { $F_OUT[0] } else { "" }
    $KEY           = if ($F_OUT.Count -gt 1) { $F_OUT[1] } else { "" }
    $SELECTED_LINE = if ($F_OUT.Count -gt 2) { $F_OUT[2] } else { "" }

    $SELECTION_LOG = Join-Path $PROJECT_ROOT "log\search_rules_selections.log"
    if ($SELECTED_LINE) {
        $SELECTED_LINE | Out-File -FilePath $SELECTION_LOG -Append -Encoding utf8
    }

    DBG "DEBUG: QUERY_TYPED='$QUERY_TYPED' | KEY='$KEY' | SELECTED_LINE='$SELECTED_LINE'"

    if (-not $SELECTED_LINE -and -not ($KEY -eq "ctrl-r" -and $QUERY_TYPED)) {
        DBG "DEBUG: Exit due to no valid selection."
        break
    }

    if ($SELECTED_LINE) {
        $SELECTED_LINE | Out-File -FilePath (Join-Path $HOME "search_rules_selections.log") -Append -Encoding utf8
    }

    if ($KEY -eq "ctrl-r") {
        DBG "DEBUG: Ctrl-R keypress detected! Entering execution block."

        $EXEC_QUERY = ""

        if ($SELECTED_LINE -and ($SELECTED_LINE -match '^([A-Za-z]:\\.+?):(\d+):(.*)$' -or $SELECTED_LINE -match '^(.+?):(\d+):(.*)$')) {
            $FILE_PATH = $Matches[1]
            $LINE_NUM  = $Matches[2]
            DBG "DEBUG: Regex match success. File: $FILE_PATH | Line: $LINE_NUM"

            $PREVIEW_PY = Join-Path $SCRIPT_DIR "preview_rule.py"
            $PY = Join-Path $PROJECT_ROOT ".venv\Scripts\python.exe"
            if (Test-Path $PREVIEW_PY) {
                $PY_EXE = if (Test-Path $PY) { $PY } else { "python" }
                DBG "DEBUG: Running: $PY_EXE $PREVIEW_PY --extract $FILE_PATH $LINE_NUM"
                try {
                    $EXEC_QUERY = (& $PY_EXE "$PREVIEW_PY" --extract $FILE_PATH $LINE_NUM).Trim()
                    DBG "DEBUG: Extracted query outcome: '$EXEC_QUERY'"
                } catch {
                    DBG "DEBUG: Python extract execution failed: $_"
                }
            } else {
                DBG "DEBUG: preview_rule.py NOT found at path $PREVIEW_PY"
            }
        }

        if (-not $EXEC_QUERY) {
            $EXEC_QUERY = $QUERY_TYPED
            DBG "DEBUG: Fallback to typed query: '$EXEC_QUERY'"
        }

       if ($EXEC_QUERY) {
            $RUN_CMD = Join-Path $SCRIPT_DIR "run_palette_command.py"
            $PYW = Join-Path $PROJECT_ROOT ".venv\Scripts\pythonw.exe"
            $PYW_EXE = if (Test-Path $PYW) { $PYW } else { "python" }
            DBG "DEBUG: Executing run_palette_command: $PYW_EXE $RUN_CMD with query: '$EXEC_QUERY'"
            try {
                Start-Process -FilePath $PYW_EXE -ArgumentList "`"$RUN_CMD`"", "`"$EXEC_QUERY`"" -WindowStyle Hidden
            } catch {
                DBG "DEBUG: Start-Process failed: $_"
            }
        }
        if ($SEARCH_CLOSE_ON_OPEN -eq "True") { break } else { Start-Sleep -Milliseconds 300; continue }
    }
    # parse path:line:content
    if ($SELECTED_LINE -match '^([A-Za-z]:\\.+?):(\d+):(.*)$' -or $SELECTED_LINE -match '^(.+?):(\d+):(.*)$') {




        $FILE_PATH = $Matches[1]
        $LINE_NUM  = [int]$Matches[2]
#         logger_info "Selected: $FILE_PATH:$LINE_NUM"
        logger_info "Selected: $($FILE_PATH):$LINE_NUM".

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
    DBG "UNHANDLED ERROR: $($_.Exception.Message)"
    DBG "STACK: $($_.Exception.StackTrace)"

    logger_info  "UNHANDLED ERROR: $($_.Exception.Message)"
    logger_info  "STACK: $($_.Exception.StackTrace)"
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press ENTER to exit (debug)"
    exit 1
}

# Pause at the end so GUI-launched runs don't close immediately
#try {
#    # Only prompt if this session is interactive or specifically launched via GUI wrapper.
#    # You can set an env var (e.g. AHK_LAUNCHED=1) in the .bat if you only want it then.
#    $ahkLaunched = $env:AHK_LAUNCHED -eq '1'
#    if ($ahkLaunched -or -not $Host.UI.RawUI.KeyAvailable) {
#        Write-Host ""
#        Write-Host "Press ENTER to exit..." -ForegroundColor Yellow
#        [void][System.Console]::ReadLine()
#    }
#} catch {
#    # fallback: always wait for Enter
#    Write-Host "Press ENTER to exit..."
#    [void][System.Console]::ReadLine()
#}


logger_info "Done."
