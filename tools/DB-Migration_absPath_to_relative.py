import sqlite3
from pathlib import Path
tmp_dir = Path('/tmp')
project_root_file = tmp_dir / 'sl5_aura' / 'sl5net_aura_project_root'
PROJECT_ROOT = Path(project_root_file.read_text().strip())
print(f'PROJECT_ROOT: {PROJECT_ROOT}')
conn = sqlite3.connect('data/_aura_result_cache.db')
cursor = conn.execute('SELECT DISTINCT map_path FROM aura_result_cache')
rows = cursor.fetchall()
updated = 0
for (old_path,) in rows:
    try:
        new_path = str(Path(old_path).relative_to(PROJECT_ROOT))
        cur = conn.execute('UPDATE aura_result_cache SET map_path = ? WHERE map_path = ?', (new_path, old_path))
        updated += cur.rowcount
    except ValueError:
        pass
conn.commit()
print(f'Updated {updated} rows')
conn.close()
