import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

customers = [
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

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.executemany(
    """
    INSERT INTO Customers (name, email, city)
    VALUES (?, ?, ?)
    """,
    customers
)

conn.commit()
conn.close()

print("Customers inserted successfully.")
