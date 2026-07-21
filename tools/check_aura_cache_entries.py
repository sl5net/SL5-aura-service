# tools/check_aura_cache_entries.py
import sqlite3
import os

DB_PATH = "data/_aura_result_cache.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    print("=== Entries for koans_deutsch/09_personal_signature ===")
    cursor = conn.execute(
        "SELECT cache_id, rule_output, final_result, map_path, validity_value "
        "FROM aura_result_cache WHERE map_path LIKE '%koans_deutsch/09_personal_signature%'"
    )
    rows = cursor.fetchall()
    print(f"Count: {len(rows)}")
    for r in rows:
        print(f"  rule={str(r['rule_output'])[:50]} | result={str(r['final_result'])[:50]} | v_val={r['validity_value']}")

    print("\n=== Simulate cleanup_cache_on_reload ===")
    map_path = "config/maps/koans_deutsch/09_personal_signature/de-DE/FUZZY_MAP_pre.py"
    new_mtime = str(os.path.getmtime(map_path)) if os.path.exists(map_path) else "N/A"
    print(f"map_path: {map_path}")
    print(f"new_mtime: {new_mtime}")

    cursor = conn.execute(
        "SELECT validity_value FROM aura_result_cache WHERE map_path = ? AND validity_type = 0",
        (map_path,)
    )
    rows = cursor.fetchall()
    print(f"Entries for this map: {len(rows)}")
    for r in rows:
        stored = r[0]
        would_delete = stored < new_mtime if new_mtime != "N/A" else "N/A"
        print(f"  stored v_val={stored} | new_mtime={new_mtime} | would_delete: {would_delete}")

    if new_mtime != "N/A":
        cursor = conn.execute(
            "DELETE FROM aura_result_cache WHERE map_path = ? AND validity_type = 0 AND validity_value < ?",
            (map_path, new_mtime)
        )
        print(f"Rows that would be deleted: {cursor.rowcount}")
        conn.rollback()

    conn.close()

if __name__ == "__main__":
    main()
