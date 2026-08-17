# اختصار CopyQ العالمي لـ Super+s

                                                                  ## يثبت
                               1. افتح CopyQ، ثم اضغط على "F6".
                            2. انقر فوق إضافة -> أمر جديد.
3. الصق مثال جافا سكريبت هذا، حيث يعمل search_rules.sh لنظام التشغيل Linux:
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

     4. قم بتعيين الاختصار العالمي على "Super + s".
                                               5. انقر فوق موافق.


                          run_rule.sh لنظام التشغيل Linux فقط:
```javascript
copyq:

// Testen mit:
//   copyq eval "$(cat /tmp/run_rule.js)"

var tmp_dir = '/tmp';
var rootFile = File(tmp_dir + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';g

if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}

var search_script = project_root + '/scripts/search_rules/run_rule.sh';

var cmd = ''
    + 'export LANG="de_DE.UTF-8"; '
    + 'export LC_ALL="de_DE.UTF-8"; '
    + 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
    + 'export SEARCH_FILES_FILTER="FUZZY_MAP*.py"; '
    + 'setsid konsole -e bash "' + search_script + '" '
    + '</dev/null >/dev/null 2>&1 & disown';

execute('bash', '-c', cmd);

```


       4. قم بتعيين الاختصار العالمي على "Super+y".
                                               5. انقر فوق موافق.

                                                            ## التوافق
       - تم اختباره على نظام Manjaro Linux (KDE Plasma, X11).
- لم يتم اختباره على نظام التشغيل Windows أو macOS.