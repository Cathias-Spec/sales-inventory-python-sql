import sqlite3
from pathlib import Path

# Paths
db_path = Path("data/sales.db")
schema_path = Path("schema.sql")

# Connect to database
connection = sqlite3.connect(db_path)

# Read SQL schema
with open(schema_path, "r", encoding="utf-8") as file:
    schema_sql = file.read()

# Execute schema
connection.executescript(schema_sql)

print("Database tables created successfully.")

# Close connection
connection.close()
