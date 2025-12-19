import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

REPORTS_DIR = Path("reports")

def main():
    df_rev = pd.read_csv(REPORTS_DIR / "revenue_per_day.csv")
    df_rev["order_date"] = pd.to_datetime(df_rev["order_date"])

    df_top = pd.read_csv(REPORTS_DIR / "top_products.csv")

    print("\n=== Revenue DataFrame ===")
    print(df_rev)

    print("\n=== Top Products DataFrame ===")
    print(df_top.head())

    # Figure 1
    plt.figure(1)
    plt.plot(df_rev["order_date"], df_rev["revenue"], marker="o")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue per Day")
    plt.tight_layout()

    # Figure 2
    plt.figure(2)
    plt.bar(df_top["product_name"], df_top["qty_sold"])
    plt.xlabel("Product")
    plt.ylabel("Quantity Sold")
    plt.title("Top Products by Quantity Sold")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    print("\nFigures created:", plt.get_fignums())  # should print [1, 2]

    plt.show()

if __name__ == "__main__":
    main()
