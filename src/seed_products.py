import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

products = [
    ("USB Flash Drive 32GB", "Electronics", 8.99, 40),
    ("Wireless Mouse", "Electronics", 12.50, 25),
    ("Notebook A5", "Stationery", 2.00, 100),
    ("Ballpoint Pen (Pack of 10)", "Stationery", 3.50, 60),
    ("Water Bottle 1L", "Home", 6.75, 30),
    ("Dish Soap 500ml", "Home", 2.80, 15),
    ("Rice 5kg", "Groceries", 9.90, 20),
    ("Cooking Oil 2L", "Groceries", 7.20, 18),
    ("T-Shirt (Medium)", "Clothing", 10.00, 12),
    ("Jeans (32)", "Clothing", 22.00, 8),
    ("Phone Charger", "Electronics", 6.00, 35),
    ("Headphones (Wired)", "Electronics", 9.50, 22),
]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executemany(
    """
    INSERT INTO Products (product_name, category, price, stock)
    VALUES (?, ?, ?, ?)
    """,
    products
)

conn.commit()
conn.close()

print("Products inserted successfully.")
