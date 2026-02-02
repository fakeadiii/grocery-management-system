import pandas as pd
from sqlalchemy import create_engine

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
engine = create_engine(
    "mysql+pymysql://root:password@localhost/grocery_analytics"
)

# ---------------------------
# INITIAL STOCK SETUP
# ---------------------------
def initialize_inventory():
    products = pd.read_sql("SELECT product_id FROM dim_product", engine)

    inventory = products.copy()
    inventory["stock_qty"] = 100  # initial stock per product

    inventory.to_sql(
        "fact_inventory_snapshot",
        engine,
        if_exists="append",
        index=False
    )

# ---------------------------
# DAILY INVENTORY UPDATE
# ---------------------------
def update_inventory():
    sales = pd.read_sql("""
        SELECT date_id, product_id, store_id, SUM(quantity) as qty_sold
        FROM fact_sales
        GROUP BY date_id, product_id, store_id
    """, engine)

    inventory = sales.copy()
    inventory["stock_qty"] = 100 - inventory["qty_sold"]

    inventory = inventory[["date_id", "product_id", "store_id", "stock_qty"]]

    inventory.to_sql(
        "fact_inventory_snapshot",
        engine,
        if_exists="append",
        index=False
    )

# ---------------------------
# LOW STOCK ALERTS
# ---------------------------
def low_stock_alerts(threshold=20):
    query = f"""
        SELECT product_id, store_id, stock_qty
        FROM fact_inventory_snapshot
        WHERE stock_qty < {threshold}
    """
    return pd.read_sql(query, engine)

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    print("Updating inventory...")
    update_inventory()
    alerts = low_stock_alerts()
    print("Low stock items:")
    print(alerts.head())

