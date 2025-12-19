import sqlite3
from pathlib import Path

DB_PATH = Path("data/sales.db")
SCHEMA_PATH = Path("schema.sql")

CUSTOMERS = [
    ("Alice Johnson", "alice@example.com", "New York"),
    ("Bob Smith", "bob@example.com", "Los Angeles"),
    ("Charlie Brown", "charlie@example.com", "Chicago"),
    ("Diana Prince", "diana@example.com", "New York"),
    ("Ethan Clark", "ethan@example.com", "Seattle"),
    ("Fiona Lee", "fiona@example.com", "San Francisco"),
    ("George Miller", "george@example.com", "Boston"),
    ("Hannah Davis", "hannah@example.com", "Austin"),
    ("Ian Wright", "ian@example.com", "Denver"),
    ("Julia Roberts", "julia@example.com", "Miami"),
]

PRODUCTS = [
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

def main():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.executescript(schema_sql)

    # Ensure processed column exists
    cols = cur.execute("PRAGMA table_info(Orders);").fetchall()
    col_names = [c[1] for c in cols]
    if "processed" not in col_names:
        cur.execute("ALTER TABLE Orders ADD COLUMN processed INTEGER NOT NULL DEFAULT 0;")

    # Seed customers (ignore duplicates)
    for name, email, city in CUSTOMERS:
        cur.execute(
            "INSERT OR IGNORE INTO Customers (name, email, city) VALUES (?, ?, ?)",
            (name, email, city)
        )

    # Seed products (avoid duplicates by name)
    for pname, category, price, stock in PRODUCTS:
        existing = cur.execute(
            "SELECT product_id FROM Products WHERE product_name = ?",
            (pname,)
        ).fetchone()

        if existing is None:
            cur.execute(
                "INSERT INTO Products (product_name, category, price, stock) VALUES (?, ?, ?, ?)",
                (pname, category, price, stock)
            )

    conn.commit()
    conn.close()

    print("Setup complete:")
    print(" - Database:", DB_PATH.resolve())
    print(" - Tables created")
    print(" - Customers seeded")
    print(" - Products seeded")

if __name__ == "__main__":
    main()
