// copyq:
// test with:
//   PYTHONUTF8=1 LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 copyq eval "$(cat launch_terminal.js)"

var isWin = !!String(env("WINDIR"));
var tmpBase = isWin ? 'C:/tmp' : '/tmp';
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';

if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}

if (isWin) {
    // Windows branch (currently empty/stub)
    print("Windows launch stub triggered");
} else {
    var search_script = project_root + '/scripts/search_rules/run_rule.sh';
    var cmd = ''
    + 'export LANG="de_DE.UTF-8"; '
    + 'export LC_ALL="de_DE.UTF-8"; '
    + 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
    + 'export SEARCH_FILES_FILTER="*.py|*.txt|*.md"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

    print("Launching Linux terminal via bash setsid...");
    execute('bash', '-c', cmd);
}
