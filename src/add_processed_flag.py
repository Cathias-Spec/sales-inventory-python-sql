import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path("data/sales.db"))
cur = conn.cursor()

# Add a processed column if it doesn't exist (SQLite doesn't support IF NOT EXISTS for columns)
# So we check table info first.
cols = cur.execute("PRAGMA table_info(Orders);").fetchall()
col_names = [c[1] for c in cols]

if "processed" not in col_names:
    cur.execute("ALTER TABLE Orders ADD COLUMN processed INTEGER NOT NULL DEFAULT 0;")
    conn.commit()
    print("Added 'processed' column to Orders.")
else:
    print("'processed' column already exists.")

conn.close()
