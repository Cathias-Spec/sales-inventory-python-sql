from src.services import(
    create_order,
    add_items_safe,
    process_order_safe,
    print_receipt,
)
def read_int(prompt: str) -> int:
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Please enter a valid number.")

def read_choice(prompt: str, choices: set[str]) -> str:
    while True:
        value = input(prompt).strip()
        if value in choices:
            return value
        print("Invalid choice. Try again.")

from src.db import get_connection
import src.queries as queries


def list_customers():
    with get_connection() as conn:
        rows = conn.execute(queries.SQL_LIST_CUSTOMERS).fetchall()
    print("\n--- Customers ---")
    for r in rows:
        print(f"{r['customer_id']}: {r['name']} | {r['email']} | {r['city']}")


def list_products():
    with get_connection() as conn:
        rows = conn.execute(queries.SQL_LIST_PRODUCTS).fetchall()
    print("\n--- Products ---")
    for r in rows:
        print(f"{r['product_id']}: {r['product_name']} | {r['category']} | {r['price']:.2f} | stock={r['stock']}")


def low_stock():
    threshold = read_int("Low-stock threshold (e.g. 10): ")

    with get_connection() as conn:
        rows = conn.execute(queries.SQL_LOW_STOCK, (threshold,)).fetchall()
    print(f"\n--- Low stock (stock < {threshold}) ---")
    for r in rows:
        print(f"{r['product_id']}: {r['product_name']} | stock={r['stock']}")


def create_order_flow():
    customer_id = read_int("Enter customer_id: ")

    order_id = create_order(customer_id)
    print("Created order:", order_id)

    items = []
    print("\nAdd items. Type product_id and quantity. Type 'done' to finish.")
    while True:
        entry = input("product_id qty (or 'done'): ").strip().lower()
        if entry == "done":
            break
        parts = entry.split()
        if len(parts) != 2:
            print("Please enter: product_id qty  (example: 1 2)")
            continue
        try:
            product_id = int(parts[0])
            qty = int(parts[1])
            if qty <= 0:
                print("Quantity must be greater than 0")
                continue
            items.append((product_id, qty))
        except ValueError:
            print("Please enter numbers only, like: 1 2")

    if items:
        add_items_safe(order_id, items)
        print("Items added.")
    else:
        print("No items added.")

    return order_id


def process_order_flow():
    order_id = read_int("Enter order_id to print receipt: ")


    total = process_order_safe(order_id)
    print(f"Processed order {order_id}. Total = {total:.2f}")


def receipt_flow():
    order_id = int(input("Enter order_id to print receipt: ").strip())
    print_receipt(order_id)


def main():
    while True:
        print("\n==============================")
        print("Sales System (Python + SQL)")
        print("==============================")
        print("1) List customers")
        print("2) List products")
        print("3) Create new order")
        print("4) Process order")
        print("5) Print receipt")
        print("6) Low stock report")
        print("0) Exit")

        choice = read_choice("Choose an option: ", {"0","1","2","3","4","5","6"})


        try:
            if choice == "1":
                list_customers()
            elif choice == "2":
                list_products()
            elif choice == "3":
                order_id = create_order_flow()
                print(f"Your new order_id is {order_id}.")
            elif choice == "4":
                process_order_flow()
            elif choice == "5":
                receipt_flow()
            elif choice == "6":
                low_stock()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
