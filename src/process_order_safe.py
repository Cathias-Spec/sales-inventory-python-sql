import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")
order_id = 3  # <-- use a NEW order id going forward

conn = sqlite3.connect(db_path)

try:
    cur = conn.cursor()
    conn.execute("BEGIN")

    # Check if already processed
    processed = cur.execute(
        "SELECT processed FROM Orders WHERE order_id = ?",
        (order_id,)
    ).fetchone()

    if processed is None:
        raise ValueError("Order not found.")

    if processed[0] == 1:
        raise ValueError("This order is already processed. No changes made.")

    # Get items
    items = cur.execute(
        """
        SELECT product_id, quantity, price
        FROM Order_Items
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchall()

    if not items:
        raise ValueError("No items found for this order.")

    # Stock check
    for product_id, qty, price in items:
        stock = cur.execute(
            "SELECT stock FROM Products WHERE product_id = ?",
            (product_id,)
        ).fetchone()

        if stock is None:
            raise ValueError(f"Product {product_id} not found.")
        if stock[0] < qty:
            raise ValueError(f"Not enough stock for product {product_id} (have {stock[0]}, need {qty}).")

    # Update stock
    for product_id, qty, price in items:
        cur.execute(
            "UPDATE Products SET stock = stock - ? WHERE product_id = ?",
            (qty, product_id)
        )

    # Update total
    total = sum(qty * price for product_id, qty, price in items)
    cur.execute(
        "UPDATE Orders SET total_amount = ?, processed = 1 WHERE order_id = ?",
        (total, order_id)
    )

    conn.commit()
    print(f"Order {order_id} processed safely. Total = {total:.2f}")

except Exception as e:
    conn.rollback()
    print("Failed. Rolled back.")
    print("Error:", e)

finally:
    conn.close()
