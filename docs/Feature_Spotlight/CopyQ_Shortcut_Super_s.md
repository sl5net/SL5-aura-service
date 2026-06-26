# CopyQ Global Shortcut to Super+s

## Setup
1. Open CopyQ, press `F6`.
2. Click Add -> New Command.
3. Paste this JavaScript Example search_rules.sh works for Linux:
```javascript
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

var search_script = project_root + '/scripts/search_rules/search_rules.sh';

var cmd = ''
    + 'export LANG="de_DE.UTF-8"; '
    + 'export LC_ALL="de_DE.UTF-8"; '
    + 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
    + 'export SEARCH_FILES_FILTER=".*py|*.md"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

execute('bash', '-c', cmd);


```

4. Set Global Shortcut to `Super+s`.
5. Click OK.


run_rule.sh for liunx only:
```javascript
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
    + 'export SEARCH_FILES_FILTER="FUZZY_MAP_pre.py"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

execute('bash', '-c', cmd);

```


4. Set Global Shortcut to `Super+y`.
5. Click OK.

## Compatibility
- Tested on Manjaro Linux (KDE Plasma, X11).
- Not tested on Windows or macOS.
