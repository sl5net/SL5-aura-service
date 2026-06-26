// copyq: Launch search_rules on Linux and Windows
// Auto-detects platform — no manual isWin toggle needed.

var isWin = !!String(env("WINDIR"));      // Windows sets WINDIR, Linux does not
var tmpBase  = isWin ? 'C:/tmp' : '/tmp';

// --- 1. Read project root from temp file ---
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
var root = '';
if (rootFile.open()) {
    root = str(rootFile.readAll()).trim();
    rootFile.close();
}

// --- 2. Fallback if file missing or empty ---
if (!root) {
    root = isWin
        ? 'C:/projects/py/STT'
        : (env('HOME') + '/projects/py/STT');   // env('HOME') avoids unexpanded ~
}

// --- 3. Launch ---
if (isWin) {
    // Convert to backslashes so cmd.exe/start handles the path correctly.
    // The empty string '' is the required window-title arg when path has spaces.
    var bat = root.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat';
    execute('cmd.exe', '/c', 'start', '', bat);
} else {
    var cmd = 'export LANG="de_DE.UTF-8" LC_ALL="de_DE.UTF-8" PYTHONUTF8=1'
            + ' DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"'
            + ' SEARCH_FILES_FILTER="*.py|*.txt|*.md";'
            + ' setsid konsole -e bash "' + root + '/scripts/search_rules/search_rules.sh"'
            + ' </dev/null >/dev/null 2>&1 &';
    execute('bash', '-c', cmd);
}
