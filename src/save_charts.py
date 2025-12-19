import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

REPORTS_DIR = Path("reports")
DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

def main():
    # --- Revenue chart ---
    df_rev = pd.read_csv(REPORTS_DIR / "revenue_per_day.csv")
    df_rev["order_date"] = pd.to_datetime(df_rev["order_date"])

    plt.figure()
    plt.plot(df_rev["order_date"], df_rev["revenue"], marker="o")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue per Day")
    plt.tight_layout()
    out1 = DOCS_DIR / "revenue_per_day.png"
    plt.savefig(out1)
    plt.close()

    # --- Top products chart ---
    df_top = pd.read_csv(REPORTS_DIR / "top_products_by_qty.csv")

    plt.figure()
    plt.bar(df_top["product_name"], df_top["qty_sold"])
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")
    plt.title("Top Products by Quantity Sold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    out2 = DOCS_DIR / "top_products.png"
    plt.savefig(out2)
    plt.close()

    print("Saved:", out1.resolve())
    print("Saved:", out2.resolve())

if __name__ == "__main__":
    main()
