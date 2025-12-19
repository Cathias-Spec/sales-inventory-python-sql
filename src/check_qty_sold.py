import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path("data/sales.db"))
cur = conn.cursor()

rows = cur.execute("""
    SELECT product_id, SUM(quantity) AS total_qty
    FROM Order_Items
    WHERE product_id IN (1, 2)
    GROUP BY product_id
    ORDER BY product_id;
""").fetchall()

print("product_id -> total_qty_sold")
for r in rows:
    print(r)

conn.close()
