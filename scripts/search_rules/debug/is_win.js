// copyq:
// test with:
// PYTHONUTF8=1 LANG=de_DE.UTF-8 LC_ALL=de_DE.UTF-8 copyq eval "$(cat is_win.js)"
var isWin = !!String(env("WINDIR"));

print("isWin: " + isWin);
