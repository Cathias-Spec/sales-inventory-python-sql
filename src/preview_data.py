import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n--- Customers ---")
for row in cursor.execute("SELECT * FROM Customers"):
    print(row)

print("\n--- Products ---")
for row in cursor.execute("SELECT * FROM Products"):
    print(row)

conn.close()
