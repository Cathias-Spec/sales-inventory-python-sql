import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n--- Products with low stock (stock < 15) ---")
for row in cursor.execute(
    "SELECT product_name, stock FROM Products WHERE stock < 15"
):
    print(row)

print("\n--- Customers in New York ---")
for row in cursor.execute(
    "SELECT name, email FROM Customers WHERE city = 'New York'"
):
    print(row)

print("\n--- Electronics products sorted by price (high to low) ---")
for row in cursor.execute(
    """
    SELECT product_name, price
    FROM Products
    WHERE category = 'Electronics'
    ORDER BY price DESC
    """
):
    print(row)

conn.close()
