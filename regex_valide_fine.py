import re, pathlib
root = pathlib.Path('config/maps')
found = 0
for f in root.rglob('FUZZY_MAP_pre.py'):
    text = f.read_text(encoding='utf-8', errors='replace')
    for m in re.finditer(r\"r(['\\\"])((?:[^\\\\]|\\\\.)*?)\1\", text):
        pat = m.group(2)
        try:
            re.compile(pat)
        except re.error as e:
            line = text[:m.start()].count(chr(10)) + 1
            print(f'{f}:{line}: {e} -> {pat!r}')
            found += 1
    print(f'--- {found} broken pattern(s) found ---')
