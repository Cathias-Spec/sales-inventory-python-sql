import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

order_id = 2  # the order you created yesterday

items = [
    (order_id, 1, 2, 8.99),   # 2 USB Flash Drives
    (order_id, 2, 1, 12.50),  # 1 Wireless Mouse
]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executemany(
    """
    INSERT INTO Order_Items (order_id, product_id, quantity, price)
    VALUES (?, ?, ?, ?)
    """,
    items
)

conn.commit()
conn.close()

print("Order items added successfully.")
