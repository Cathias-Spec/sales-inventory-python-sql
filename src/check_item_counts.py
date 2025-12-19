import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path("data/sales.db"))
cur = conn.cursor()

rows = cur.execute("""
    SELECT order_id, COUNT(*) AS item_rows
    FROM Order_Items
    GROUP BY order_id
    ORDER BY order_id;
""").fetchall()

print("order_id -> item_rows")
for r in rows:
    print(r)

conn.close()
