copyq:
var isWin = false, f = File('/tmp/sl5_aura/sl5net_aura_project_root');
var r = f.open() ? str(f.readAll()).trim() : (isWin ? 'C:/projects/py/STT' : '~/projects/py/STT');
f.close();
if (isWin) {
    execute('cmd.exe', '/c', 'start', '', r.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat');
} else {
    var cmd = 'export LANG="de_DE.UTF-8" LC_ALL="de_DE.UTF-8" PYTHONUTF8=1 DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus" SEARCH_FILES_FILTER="*.py|*.txt|*.md"; setsid konsole -e bash "' + r + '/scripts/search_rules/search_rules.sh" </dev/null >/dev/null 2>&1 &';
    execute('bash', '-c', cmd);
}

