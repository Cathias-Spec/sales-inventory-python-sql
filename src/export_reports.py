import csv
from pathlib import Path

from src.db import get_connection
import src.queries as queries

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def export_revenue_per_day():
    with get_connection() as conn:
        rows = conn.execute(queries.SQL_REVENUE_PER_DAY).fetchall()

    out_path = REPORTS_DIR / "revenue_per_day.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_date", "revenue"])
        for r in rows:
            writer.writerow([r["order_date"], float(r["revenue"])])

    print("Saved:", out_path)

def export_top_products(limit: int = 10):
    with get_connection() as conn:
        rows = conn.execute(queries.SQL_TOP_PRODUCTS_BY_QTY, (limit,)).fetchall()

    out_path = REPORTS_DIR / "top_products_by_qty.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id", "product_name", "qty_sold"])
        for r in rows:
            writer.writerow([r["product_id"], r["product_name"], int(r["qty_sold"])])

    print("Saved:", out_path)

def export_top_customers(limit: int = 10):
    with get_connection() as conn:
        rows = conn.execute(queries.SQL_TOP_CUSTOMERS_BY_SPEND, (limit,)).fetchall()

    out_path = REPORTS_DIR / "top_customers_by_spend.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "customer_name", "total_spent"])
        for r in rows:
            writer.writerow([r["customer_id"], r["name"], float(r["total_spent"])])

    print("Saved:", out_path)

def main():
    export_revenue_per_day()
    export_top_products(limit=10)
    export_top_customers(limit=10)

if __name__ == "__main__":
    main()
