copyq:
// test with: copyq eval "$(cat test_win_v3.js)"
var isWin = !!String(env("WINDIR"));
var tmpBase = isWin ? 'C:/tmp' : '/tmp';
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';
if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}
if (isWin) {
    var bat = project_root.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat';
    execute('cmd.exe', '/c', 'start', '', bat);
}
