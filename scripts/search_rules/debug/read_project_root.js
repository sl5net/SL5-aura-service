copyq:
// test with:
//   PYTHONUTF8=1 LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 copyq eval "$(cat read_project_root.js)"
var isWin = !!String(env("WINDIR"));
var tmpBase = isWin ? 'C:/tmp' : '/tmp';
var rootFile = File(tmpBase + '/sl5_aura/sl5net_aura_project_root');
var project_root = '';
if (rootFile.open()) {
    project_root = str(rootFile.readAll()).trim();
    rootFile.close();
}
print("Project Root: [" + project_root + "]");
