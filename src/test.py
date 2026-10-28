import pandas as pd
from sqlalchemy import text
 
 
def query_value(conn, sql):
    """Run a query that returns a single value (ex: a count)."""
    return conn.execute(text(sql)).scalar()
 
 
def run_test(df, engine):
    """Compare the DataFrame coming out of transform with the data in PostgreSQL."""
    results = {}
 
    with engine.connect() as conn:
        # 1
        n_fact = query_value(conn, "select count(*) from fact_sales")
        results["fact_sales lines = df lines"] = n_fact == len(df)

        #2
        n_products = query_value(conn, "select count(*) from product")
        n_customers = query_value(conn, "select count(*) from customer")
        n_unknown = query_value(conn, "select count(*) from customer where customer_id = -1")
        results["product = distinct StockCode"] = n_products == df["StockCode"].nunique()
        results["customer = distinct Customer ID"] = n_customers == df["Customer ID"].nunique()
        results["unknown customer -1 exists"] = n_unknown == 1

    for name, passed in results.items():
        print(f"{name}: {passed}")
 
    if not all(results.values()):
        raise ValueError("Some checks failed")
    print("All checks passed")
