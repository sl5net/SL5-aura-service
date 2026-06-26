# CopyQ Atalho Global para Super+s

## Configurar
1. Abra CopyQ, pressione `F6`.
2. Clique em Adicionar -> Novo Comando.
3. Cole este exemplo de JavaScript que search_rules.sh funciona para Linux:
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

4. Defina o atalho global para `Super+s`.
5. Clique em OK.


run_rule.sh apenas para Linux:
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


4. Defina o atalho global para `Super+y`.
5. Clique em OK.

## Compatibilidade
- Testado em Manjaro Linux (KDE Plasma, X11).
- Não testado em Windows ou macOS.