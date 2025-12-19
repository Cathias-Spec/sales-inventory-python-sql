import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")
order_id = 2

conn = sqlite3.connect(db_path)
cur = conn.cursor()

header = cur.execute(
    """
    SELECT o.order_id, o.order_date, c.name, c.email, c.city, o.total_amount
    FROM Orders o
    JOIN Customers c ON c.customer_id = o.customer_id
    WHERE o.order_id = ?
    """,
    (order_id,)
).fetchone()

if header is None:
    print("Order not found.")
    conn.close()
    raise SystemExit

order_id, order_date, cust_name, cust_email, cust_city, total_amount = header

print("\n==============================")
print("RECEIPT (GROUPED)")
print("==============================")
print(f"Order ID:   {order_id}")
print(f"Order Date: {order_date}")
print(f"Customer:   {cust_name} ({cust_email})")
print(f"City:       {cust_city}")
print("------------------------------")

items = cur.execute(
    """
    SELECT
        p.product_name,
        SUM(oi.quantity) AS total_qty,
        oi.price,
        SUM(oi.quantity * oi.price) AS line_total
    FROM Order_Items oi
    JOIN Products p ON p.product_id = oi.product_id
    WHERE oi.order_id = ?
    GROUP BY p.product_name, oi.price
    ORDER BY p.product_name
    """,
    (order_id,)
).fetchall()

for product_name, total_qty, price, line_total in items:
    print(f"{product_name}")
    print(f"  Qty: {total_qty}  Price: {price:.2f}  Line Total: {line_total:.2f}")

print("------------------------------")
print(f"TOTAL: {total_amount:.2f}")
print("==============================\n")

conn.close()
