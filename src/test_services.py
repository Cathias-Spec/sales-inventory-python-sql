from src.services import create_order, add_items_safe, process_order_safe, print_receipt

def main():
    # Create a NEW order (avoid touching old orders)
    order_id = create_order(customer_id=1)
    print("Created order:", order_id)

    # Add items safely (no duplicate rows)
    add_items_safe(order_id, [(1, 2), (2, 1)])
    add_items_safe(order_id, [(1, 2), (2, 1)])  # run twice to prove no duplicate rows
    print("Added items twice safely.")

    # Process safely (stock updated, total computed, processed flag set)
    total = process_order_safe(order_id)
    print("Processed order. Total =", total)

    # Print receipt
    print_receipt(order_id)

if __name__ == "__main__":
    main()
