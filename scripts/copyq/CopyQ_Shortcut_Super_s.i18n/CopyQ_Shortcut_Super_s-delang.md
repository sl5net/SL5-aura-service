# Globale Verknüpfung von CopyQ zu Super+s

## Aufstellen
1. Öffnen Sie CopyQ und drücken Sie „F6“.
2. Klicken Sie auf Hinzufügen -> Neuer Befehl.
3. Fügen Sie dieses JavaScript-Beispiel ein: search_rules.sh funktioniert unter Linux:
```javascript

copyq:
var isWin = false, f = File('/tmp/sl5_aura/sl5net_aura_project_root');
var r = f.open() ? str(f.readAll()).trim() : (isWin ? 'C:/projects/py/STT' : '~/projects/py/STT');
f.close();
if (isWin) {
    execute('cmd.exe', '/c', 'start', r + '/scripts/search_rules/search_rules.bat');
} else {
    var cmd = 'export LANG="de_DE.UTF-8" LC_ALL="de_DE.UTF-8" PYTHONUTF8=1 DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus" SEARCH_FILES_FILTER="*.py|*.txt|*.md"; setsid konsole -e bash "' + r + '/scripts/search_rules/search_rules.sh" </dev/null >/dev/null 2>&1 &';
    execute('bash', '-c', cmd);
}

```

4. Stellen Sie die globale Verknüpfung auf „Super+s“ ein.
5. Klicken Sie auf OK.


run_rule.sh nur für Linux:
```
copyq:

// Testen mit:
//   copyq eval "$(cat /tmp/run_rule.js)"

var tmp_dir = '/tmp';
var rootFile = File(tmp_dir + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';

if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}

var search_script = project_root + '/scripts/search_rules/run_rule.sh';

var cmd = ''
    + 'export LANG="de_DE.UTF-8"; '
    + 'export LC_ALL="de_DE.UTF-8"; '
    + 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
    + 'export SEARCH_FILES_FILTER="*.py|*.txt|*.md"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

execute('bash', '-c', cmd);

```


4. Stellen Sie die globale Verknüpfung auf „Super+y“ ein.
5. Klicken Sie auf OK.

## Kompatibilität
- Getestet auf Manjaro Linux (KDE Plasma, X11).
- Nicht unter Windows oder macOS getestet.