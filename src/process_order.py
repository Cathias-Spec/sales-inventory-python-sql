import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")
order_id = 1

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1) Get all items in the order
items = cursor.execute(
    """
    SELECT product_id, quantity, price
    FROM Order_Items
    WHERE order_id = ?
    """,
    (order_id,)
).fetchall()

if not items:
    print("No items found for this order.")
    conn.close()
    raise SystemExit

# 2) Update stock for each product
for product_id, quantity, price in items:
    cursor.execute(
        """
        UPDATE Products
        SET stock = stock - ?
        WHERE product_id = ?
        """,
        (quantity, product_id)
    )

# 3) Calculate total amount
total_amount = sum(quantity * price for product_id, quantity, price in items)

# 4) Update order total
cursor.execute(
    """
    UPDATE Orders
    SET total_amount = ?
    WHERE order_id = ?
    """,
    (total_amount, order_id)
)

conn.commit()
conn.close()

print(f"Order {order_id} processed. Total amount = {total_amount:.2f}")
