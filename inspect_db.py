# inspect_db.py
import sqlite3
import pathlib
import sys

db_path = pathlib.Path("instance/edumentor_dev.db")

if not db_path.exists():
    print("DB file not found at:", db_path.resolve())
    sys.exit(1)

print("Inspecting DB:", db_path.resolve())
print("=" * 60)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

print("\nTables in DB:")
for row in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"):
    print(" -", row[0])

print("\n" + "=" * 60)

candidates = [
    "users", "user", "Users", "User",
    "marks", "mark", "Marks", "Mark",
    "attendance", "attendances", "Attendance", "Attendances"
]

print("Row counts (attempting common table names):")
found_any = False
for t in candidates:
    try:
        c = cur.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
        print(f" {t}: {c}")
        found_any = True
    except Exception:
        pass

if not found_any:
    print(" No counts available for the candidate table names (tables may have different names).")

print("\n" + "=" * 60)

print("Showing up to 5 sample rows from each table found:")
tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")]
for t in tables:
    try:
        print(f"\nTable: {t}")
        rows = cur.execute(f"SELECT * FROM {t} LIMIT 5").fetchall()
        if not rows:
            print("  (no rows)")
            continue
        for r in rows:
            print(" ", r)
    except Exception as e:
        print(f"  (could not read rows from {t}: {e})")

conn.close()
print("\nDone.")
