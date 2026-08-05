# tools/inspect_aura_cache.py
# PYTHONUTF8=1 python3 tools/inspect_aura_cache.py

import sqlite3
import sys


def inspect_database(db_path: str) -> None:
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        tables = [
            row[0]
            for row in cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()
        ]
        print(f"Database: {db_path}")
        print(f"Tables found: {tables}\n")

        for table in tables:
            schema = cursor.execute(f"PRAGMA table_info({table});").fetchall()
            count = cursor.execute(
                f"SELECT COUNT(*) FROM {table};"
            ).fetchone()[0]
            print(f"=== Table: {table} (Total rows: {count}) ===")
            print("Columns:")
            for col in schema:
                print(f"  - {col[1]} ({col[2]})")

            print("\nSample rows (up to 3):")
            sample = cursor.execute(f"SELECT * FROM {table} LIMIT 3;").fetchall()
            for row in sample:
                print(f"  {row}")

            print("\nSearching for 'pull requests':")
            matches = 0
            for row in cursor.execute(f"SELECT * FROM {table};").fetchall():
                if "pull requests" in str(row).lower():
                    print(f"  MATCH: {row}")
                    matches += 1
            if matches == 0:
                print("  No matches found for 'pull requests'.")
            print("-" * 50)

        conn.close()
    except Exception as exc:
        print(f"Error inspecting database {db_path}: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    inspect_database("data/_aura_result_cache.db")

