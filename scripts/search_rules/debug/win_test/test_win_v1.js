// test with:
// & copyq eval (Get-Content -Raw -Path scripts\search_rules\debug\win_test\test_win_v1.js)
print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')

// copyq:
var debugFile = File('C:\\tmp\\copyq_debug.txt');
if (debugFile.open('w')) {
    debugFile.write('test_win_v1.js:6 hi');
    // debugFile.close();
}
print('BBBBBBBBBBBBBBBBBBBBBBBBBBBB')
var isWin = !!String(env("WINDIR"));

var tmpBase = isWin ? 'C:\\tmp' : '/tmp';
var rootFile = '';
if (isWin) {
    rootFile = File(tmpBase + '\\sl5_aura\\sl5net_aura_project_root');
}else{
    rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
    debugFile.write('test_win_v1.js:6 hi);
}

var root = '';
if (rootFile.open()) {
    root = str(rootFile.readAll()).trim();
    rootFile.close();
}

if (isWin) {
    // var bat = root.replace(/\//g, '\\') + '\\scripts\\search_rules\\search_rules.bat';
    var bat = root + '/scripts/search_rules/search_rules.bat';
    execute('cmd.exe', '/c', 'start', '', bat);
}

