# --- Customers ---
SQL_LIST_CUSTOMERS = """
SELECT customer_id, name, email, city
FROM Customers
ORDER BY customer_id;
"""

# --- Products ---
SQL_LIST_PRODUCTS = """
SELECT product_id, product_name, category, price, stock
FROM Products
ORDER BY product_id;
"""

SQL_LOW_STOCK = """
SELECT product_id, product_name, stock
FROM Products
WHERE stock < ?
ORDER BY stock ASC;
"""

# --- Orders / Receipts ---
SQL_ORDER_HEADER = """
SELECT o.order_id, o.order_date, o.total_amount, o.processed,
       c.customer_id, c.name, c.email, c.city
FROM Orders o
JOIN Customers c ON c.customer_id = o.customer_id
WHERE o.order_id = ?;
"""

SQL_ORDER_ITEMS_GROUPED = """
SELECT p.product_id,
       p.product_name,
       SUM(oi.quantity) AS total_qty,
       oi.price,
       SUM(oi.quantity * oi.price) AS line_total
FROM Order_Items oi
JOIN Products p ON p.product_id = oi.product_id
WHERE oi.order_id = ?
GROUP BY p.product_id, p.product_name, oi.price
ORDER BY p.product_name;
"""
# --- Analytics ---
SQL_REVENUE_PER_DAY = """
SELECT order_date, ROUND(SUM(total_amount), 2) AS revenue
FROM Orders
WHERE processed = 1
GROUP BY order_date
ORDER BY order_date;
"""

SQL_TOP_PRODUCTS_BY_QTY = """
SELECT p.product_id, p.product_name, SUM(oi.quantity) AS qty_sold
FROM Order_Items oi
JOIN Products p ON p.product_id = oi.product_id
JOIN Orders o ON o.order_id = oi.order_id
WHERE o.processed = 1
GROUP BY p.product_id, p.product_name
ORDER BY qty_sold DESC, p.product_name ASC
LIMIT ?;
"""

SQL_TOP_CUSTOMERS_BY_SPEND = """
SELECT c.customer_id, c.name, ROUND(SUM(o.total_amount), 2) AS total_spent
FROM Orders o
JOIN Customers c ON c.customer_id = o.customer_id
WHERE o.processed = 1
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC, c.name ASC
LIMIT ?;
"""
