var tmp_dir = '/tmp';
var rootFile = File(tmp_dir + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';

if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}

var search_script = project_root + '/scripts/search_rules/run_rule.sh';

var active_win_title = str(execute('bash', '-c', 'xdotool getactivewindow getwindowname 2>/dev/null || true').stdout).trim();

var cmd = ''
+ 'export LANG="de_DE.UTF-8"; '
+ 'export LC_ALL="de_DE.UTF-8"; '
+ 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"; '
+ 'export SEARCH_FILES_FILTER="FUZZY_MAP*.py"; '
+ 'export AURA_ACTIVE_WINDOW_TITLE="' + active_win_title + '"; '
+ 'TERM_BIN=$(command -v x-terminal-emulator || command -v gnome-terminal || command -v konsole || command -v xfce4-terminal || command -v mate-terminal || command -v xterm); '
+ 'if [ -n "$TERM_BIN" ]; then '
+ '  if [[ "$TERM_BIN" == *gnome-terminal* ]]; then '
+ '    setsid "$TERM_BIN" -- bash "' + search_script + '" </dev/null >/dev/null 2>&1 & disown; '
+ '  else '
+ '    setsid "$TERM_BIN" -e bash "' + search_script + '" </dev/null >/dev/null 2>&1 & disown; '
+ '  fi; '
+ 'fi';

execute('bash', '-c', cmd);
