import sqlite3
from pathlib import Path

db_path = Path("data/sales.db")

# Choose an existing customer
customer_id = 1  # Alice Johnson

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO Orders (customer_id)
    VALUES (?)
    """,
    (customer_id,)
)

conn.commit()

print("Order created successfully.")
conn.close()
