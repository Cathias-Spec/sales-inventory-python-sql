import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")
order_id = 2

conn = sqlite3.connect(db_path)

try:
    cursor = conn.cursor()

    # Begin transaction
    conn.execute("BEGIN")

    # Get order items
    items = cursor.execute(
        """
        SELECT product_id, quantity, price
        FROM Order_Items
        WHERE order_id = ?
        """,
        (order_id,)
    ).fetchall()

    if not items:
        raise ValueError("No items found for this order.")

    # Check stock first (important!)
    for product_id, quantity, price in items:
        current_stock = cursor.execute(
            "SELECT stock FROM Products WHERE product_id = ?",
            (product_id,)
        ).fetchone()

        if current_stock is None:
            raise ValueError(f"Product {product_id} does not exist.")

        if current_stock[0] < quantity:
            raise ValueError(
                f"Not enough stock for product {product_id}. "
                f"Stock={current_stock[0]}, Needed={quantity}"
            )

    # Update stock
    for product_id, quantity, price in items:
        cursor.execute(
            """
            UPDATE Products
            SET stock = stock - ?
            WHERE product_id = ?
            """,
            (quantity, product_id)
        )

    # Calculate total
    total_amount = sum(quantity * price for product_id, quantity, price in items)

    # Update order total
    cursor.execute(
        """
        UPDATE Orders
        SET total_amount = ?
        WHERE order_id = ?
        """,
        (total_amount, order_id)
    )

    # Commit if everything succeeds
    conn.commit()
    print(f"Order {order_id} processed with transaction. Total = {total_amount:.2f}")

except Exception as e:
    # Rollback if anything fails
    conn.rollback()
    print("Transaction failed. Changes rolled back.")
    print("Error:", e)

finally:
    conn.close()
