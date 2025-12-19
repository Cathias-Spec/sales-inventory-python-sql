import sqlite3
from pathlib import Path

DB_PATH = Path("data/sales.db")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    # Optional: makes rows behave like dicts (row["name"])
    conn.row_factory = sqlite3.Row
    return conn
