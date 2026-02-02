from sqlalchemy import create_engine
import pandas as pd

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
engine = create_engine(
    "mysql+pymysql://root:password@localhost/grocery_analytics"
)

def check_inventory():
    query = """
    SELECT 
        p.product_name,
        SUM(s.quantity) AS total_sold
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY total_sold DESC
    LIMIT 10;
    """

    df = pd.read_sql(query, engine)
    print("\nTop 10 products by quantity sold:\n")
    print(df)

if __name__ == "__main__":
    print("Running inventory analysis...")
    check_inventory()
