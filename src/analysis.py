import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

REPORTS_DIR = Path("reports")

def revenue_over_time():
    # Load CSV
    df = pd.read_csv(REPORTS_DIR / "revenue_per_day.csv")

    print("\n=== Revenue DataFrame ===")
    print(df)

    # Convert order_date to datetime
    df["order_date"] = pd.to_datetime(df["order_date"])

    # Plot
    plt.figure()
    plt.plot(df["order_date"], df["revenue"], marker="o")
    plt.xlabel("Date")
    plt.ylabel("Revenue")
    plt.title("Revenue per Day")
    plt.tight_layout()
    plt.show()

def main():
    revenue_over_time()

if __name__ == "__main__":
    main()
