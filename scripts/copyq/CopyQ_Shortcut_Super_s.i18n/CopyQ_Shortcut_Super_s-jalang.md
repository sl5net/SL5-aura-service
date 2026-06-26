# CopyQ Super+ へのグローバル ショートカット

＃＃ 設定
1. CopyQ を開き、「F6」を押します。
2. 「追加」→「新規コマンド」をクリックします。
3. この JavaScript の例を貼り付けます。search_rules.sh は Linux で動作します。
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

4. グローバル ショートカットを「Super+s」に設定します。
5. 「OK」をクリックします。


run_rule.sh (Linux のみ):
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


4. グローバル ショートカットを「Super+y」に設定します。
5. 「OK」をクリックします。

## 互換性
- Manjaro Linux (KDE Plasma、X11) でテスト済み。
- Windows または macOS ではテストされていません。