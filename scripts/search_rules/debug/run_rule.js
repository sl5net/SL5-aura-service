copyq:
// test with:
// PYTHONUTF8=1 LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 copyq eval "$(cat run_rule.js)"

var isWin = !!String(env("WINDIR"));      // Windows setSelectedItemData
var tmpBase  = isWin ? 'C:/tmp' : '/tmp';
// --- 1. Read project root from temp file ---
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');

var project_root = '';
if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}

// --- 3. Launch ---
if (isWin) {
     Convert to backslashes so cmd.exe/start handles the path correctly.
     The empty string '' is the required window-title arg when path has spaces.
     var bat = project_root.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat';
     execute('cmd.exe', '/c', 'start', '', bat);
} else {
    var search_script = project_root + '/scripts/search_rules/run_rule.sh';

    var cmd = ''
    + 'export LANG="de_DE.UTF-8"; '
    + 'export LC_ALL="de_DE.UTF-8"; '
    + 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
    + 'export SEARCH_FILES_FILTER="*.py|*.txt|*.md"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

    execute('bash', '-c', cmd);
}

