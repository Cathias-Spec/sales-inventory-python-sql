import sqlite3
from pathlib import Path

# Path to the database file
db_path = Path("data/sales.db")

# Create the data folder if it doesn't exist
db_path.parent.mkdir(exist_ok=True)

# Connect to the database (this creates the file)
connection = sqlite3.connect(db_path)

print("Database created at:", db_path.resolve())
# Close the connection
connection.close()

