copyq:
// test with: copyq eval "$(cat test_win_v2.js)"
var isWin = !!String(env("WINDIR"));
var tmpBase = isWin ? 'C:/tmp' : '/tmp';
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
var r = '';
if (rootFile.open()) {
    r = str(rootFile.readAll()).trim();
    rootFile.close();
}
if (isWin) {
    execute('cmd.exe', '/c', 'start', '', r.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat');
}
