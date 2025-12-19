from typing import List, Tuple
from src.db import get_connection
import src.queries as queries

# items_to_add: List of (product_id, qty)
def create_order(customer_id: int) -> int:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO Orders (customer_id) VALUES (?)", (customer_id,))
        order_id = cur.lastrowid
        conn.commit()
        return int(order_id)

def add_items_safe(order_id: int, items_to_add: List[Tuple[int, int]]) -> None:
    with get_connection() as conn:
        cur = conn.cursor()

        for product_id, qty in items_to_add:
            # get product price
            price_row = cur.execute(
                "SELECT price FROM Products WHERE product_id = ?",
                (product_id,)
            ).fetchone()
            if price_row is None:
                raise ValueError(f"Product {product_id} not found.")

            price = float(price_row["price"])

            existing = cur.execute(
                """
                SELECT order_item_id, quantity
                FROM Order_Items
                WHERE order_id = ? AND product_id = ?
                """,
                (order_id, product_id)
            ).fetchone()

            if existing:
                new_qty = int(existing["quantity"]) + qty
                cur.execute(
                    "UPDATE Order_Items SET quantity = ? WHERE order_item_id = ?",
                    (new_qty, existing["order_item_id"])
                )
            else:
                cur.execute(
                    """
                    INSERT INTO Order_Items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """,
                    (order_id, product_id, qty, price)
                )

        conn.commit()

def process_order_safe(order_id: int) -> float:
    """
    Updates stock, computes total, marks order processed=1.
    Rolls back if anything fails.
    Returns total.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        conn.execute("BEGIN")

        row = cur.execute(
            "SELECT processed FROM Orders WHERE order_id = ?",
            (order_id,)
        ).fetchone()

        if row is None:
            raise ValueError("Order not found.")
        if int(row["processed"]) == 1:
            raise ValueError("Order already processed.")

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

        # stock check
        for it in items:
            product_id = int(it["product_id"])
            qty = int(it["quantity"])

            stock_row = cur.execute(
                "SELECT stock FROM Products WHERE product_id = ?",
                (product_id,)
            ).fetchone()

            if stock_row is None:
                raise ValueError(f"Product {product_id} not found.")
            if int(stock_row["stock"]) < qty:
                raise ValueError(f"Not enough stock for product {product_id}.")

        # update stock
        for it in items:
            product_id = int(it["product_id"])
            qty = int(it["quantity"])
            cur.execute(
                "UPDATE Products SET stock = stock - ? WHERE product_id = ?",
                (qty, product_id)
            )

        total = sum(int(it["quantity"]) * float(it["price"]) for it in items)

        cur.execute(
            "UPDATE Orders SET total_amount = ?, processed = 1 WHERE order_id = ?",
            (total, order_id)
        )

        conn.commit()
        return float(total)

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def print_receipt(order_id: int) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        header = cur.execute(queries.SQL_ORDER_HEADER, (order_id,)).fetchone()
        if header is None:
            print("Order not found.")
            return

        print("\n==============================")
        print("RECEIPT")
        print("==============================")
        print(f"Order ID:   {header['order_id']}")
        print(f"Order Date: {header['order_date']}")
        print(f"Customer:   {header['name']} ({header['email']})")
        print(f"City:       {header['city']}")
        print(f"Processed:  {header['processed']}")
        print("------------------------------")

        items = cur.execute(queries.SQL_ORDER_ITEMS_GROUPED, (order_id,)).fetchall()
        for it in items:
            print(f"{it['product_name']}")
            print(f"  Qty: {it['total_qty']}  Price: {float(it['price']):.2f}  Line Total: {float(it['line_total']):.2f}")

        print("------------------------------")
        print(f"TOTAL: {float(header['total_amount']):.2f}")
        print("==============================\n")
