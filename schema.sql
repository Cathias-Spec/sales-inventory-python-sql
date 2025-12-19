-- Customers table
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    email       TEXT UNIQUE,
    city        TEXT
);

-- Products table
CREATE TABLE IF NOT EXISTS Products (
    product_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category     TEXT,
    price        REAL NOT NULL CHECK (price >= 0),
    stock        INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

-- Orders table
CREATE TABLE IF NOT EXISTS Orders (
    order_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id  INTEGER NOT NULL,
    order_date   TEXT NOT NULL DEFAULT (DATE('now')),
    total_amount REAL NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Order items table
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL CHECK (quantity > 0),
    price         REAL NOT NULL CHECK (price >= 0),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
