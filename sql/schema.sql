-- =========================
-- DATABASE
-- =========================
CREATE DATABASE IF NOT EXISTS grocery_analytics;
USE grocery_analytics;

-- =========================
-- DATE DIMENSION
-- =========================
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE NOT NULL,
    day INT,
    month INT,
    month_name VARCHAR(15),
    quarter INT,
    year INT,
    is_weekend BOOLEAN
);

-- =========================
-- CATEGORY
-- =========================
CREATE TABLE dim_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL
);

-- =========================
-- PRODUCT
-- =========================
CREATE TABLE dim_product (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    brand VARCHAR(100),
    unit VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES dim_category(category_id)
);

-- =========================
-- CUSTOMER
-- =========================
CREATE TABLE dim_customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_type ENUM('Retail','Wholesale'),
    location VARCHAR(100),
    loyalty_member BOOLEAN
);

-- =========================
-- STORE
-- =========================
CREATE TABLE dim_store (
    store_id INT AUTO_INCREMENT PRIMARY KEY,
    store_name VARCHAR(100),
    city VARCHAR(100),
    state VARCHAR(100)
);

-- =========================
-- SUPPLIER
-- =========================
CREATE TABLE dim_supplier (
    supplier_id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(150),
    lead_time_days INT,
    reliability_score DECIMAL(3,2)
);

-- =========================
-- SALES FACT TABLE
-- =========================
CREATE TABLE fact_sales (
    sale_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_id INT,
    product_id INT,
    customer_id INT,
    store_id INT,
    quantity INT,
    revenue DECIMAL(10,2),
    cost DECIMAL(10,2),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- =========================
-- INVENTORY SNAPSHOT
-- =========================
CREATE TABLE fact_inventory_snapshot (
    snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    date_id INT,
    product_id INT,
    store_id INT,
    stock_qty INT,
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id)
);

-- =========================
-- PURCHASE ORDERS
-- =========================
CREATE TABLE fact_purchase_orders (
    po_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    product_id INT,
    order_date_id INT,
    expected_delivery_date_id INT,
    quantity INT,
    total_cost DECIMAL(10,2),
    status ENUM('Ordered','Delivered','Delayed'),
    FOREIGN KEY (supplier_id) REFERENCES dim_supplier(supplier_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

-- =========================
-- PRICE HISTORY
-- =========================
CREATE TABLE price_history (
    price_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    effective_date DATE,
    cost_price DECIMAL(10,2),
    selling_price DECIMAL(10,2),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

-- =========================
-- REORDER RULES
-- =========================
CREATE TABLE inventory_reorder_rules (
    product_id INT PRIMARY KEY,
    reorder_level INT,
    reorder_quantity INT,
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id)
);

