import random
import pandas as pd
import numpy as np
from faker import Faker
from sqlalchemy import create_engine
from datetime import datetime, timedelta

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
engine = create_engine(
    "mysql+pymysql://root:password@localhost/grocery_analytics"
)

fake = Faker()

# ---------------------------
# DATE DIMENSION
# ---------------------------
def generate_dates(start_date, end_date):
    dates = []
    current = start_date
    while current <= end_date:
        dates.append({
            "date_id": int(current.strftime("%Y%m%d")),
            "full_date": current,
            "day": current.day,
            "month": current.month,
            "month_name": current.strftime("%B"),
            "quarter": (current.month - 1) // 3 + 1,
            "year": current.year,
            "is_weekend": current.weekday() >= 5
        })
        current += timedelta(days=1)
    return pd.DataFrame(dates)

# ---------------------------
# STATIC DIMENSIONS
# ---------------------------
def generate_categories():
    return pd.DataFrame({
        "category_name": [
            "Vegetables", "Fruits", "Dairy", "Bakery",
            "Beverages", "Snacks", "Frozen", "Grains"
        ]
    })

def generate_products(categories):
    products = []
    for _ in range(60):
        products.append({
            "product_name": fake.word().capitalize(),
            "category_id": random.choice(categories),
            "brand": fake.company(),
            "unit": random.choice(["kg", "litre", "pack"])
        })
    return pd.DataFrame(products)

def generate_customers(n=200):
    return pd.DataFrame([{
        "customer_type": random.choice(["Retail", "Wholesale"]),
        "location": fake.city(),
        "loyalty_member": random.choice([True, False])
    } for _ in range(n)])

def generate_stores():
    return pd.DataFrame([
        {"store_name": "Main Store", "city": "Delhi", "state": "Delhi"},
        {"store_name": "Branch Store", "city": "Noida", "state": "UP"}
    ])

def generate_suppliers():
    return pd.DataFrame([{
        "supplier_name": fake.company(),
        "lead_time_days": random.randint(2, 10),
        "reliability_score": round(random.uniform(0.7, 0.98), 2)
    } for _ in range(15)])

# ---------------------------
# SALES FACT TABLE
# ---------------------------
def generate_sales(dates, products, customers, stores):
    sales = []
    for date in dates:
        daily_sales = random.randint(20, 60)
        for _ in range(daily_sales):
            qty = random.randint(1, 5)
            price = round(random.uniform(20, 200), 2)
            cost = round(price * random.uniform(0.6, 0.8), 2)
            sales.append({
                "date_id": date,
                "product_id": random.choice(products),
                "customer_id": random.choice(customers),
                "store_id": random.choice(stores),
                "quantity": qty,
                "revenue": qty * price,
                "cost": qty * cost
            })
    return pd.DataFrame(sales)

# ---------------------------
# MAIN EXECUTION
# ---------------------------
if __name__ == "__main__":
    print("Generating data...")

    dates_df = generate_dates(
        datetime(2024, 1, 1),
        datetime(2024, 12, 31)
    )
    dates_df.to_sql("dim_date", engine, if_exists="append", index=False)

    categories_df = generate_categories()
    categories_df.to_sql("dim_category", engine, if_exists="append", index=False)

    category_ids = pd.read_sql("SELECT category_id FROM dim_category", engine)["category_id"].tolist()

    products_df = generate_products(category_ids)
    products_df.to_sql("dim_product", engine, if_exists="append", index=False)

    customers_df = generate_customers()
    customers_df.to_sql("dim_customer", engine, if_exists="append", index=False)

    stores_df = generate_stores()
    stores_df.to_sql("dim_store", engine, if_exists="append", index=False)

    suppliers_df = generate_suppliers()
    suppliers_df.to_sql("dim_supplier", engine, if_exists="append", index=False)

    sales_df = generate_sales(
        dates_df["date_id"].tolist(),
        pd.read_sql("SELECT product_id FROM dim_product", engine)["product_id"].tolist(),
        pd.read_sql("SELECT customer_id FROM dim_customer", engine)["customer_id"].tolist(),
        pd.read_sql("SELECT store_id FROM dim_store", engine)["store_id"].tolist()
    )

    sales_df.to_sql("fact_sales", engine, if_exists="append", index=False)

    print("Data generation completed successfully!")

