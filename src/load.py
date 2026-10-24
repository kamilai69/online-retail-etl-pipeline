import pandas as pd

COLUMN_NAMES = {
    "Invoice" : "invoice",
    "StockCode" : "stock_code",
    "Description" : "description",
    "Quantity" : "quantity",
    "InvoiceDate" : "invoice_date",
    "Price" : "price",
    "Customer ID" : "customer_id",
    "Country" : "country",
    "Revenue" : "revenue"
}

def rename_columns(df):
    """Rename the colmums to fit with the standars naming column of PostgreSQL"""
    df = df.rename(columns=COLUMN_NAMES)
    return df

def load(df: pd.DataFrame, engine, table: str) -> None:
    """Send the dataframe to PostgreSQL"""
    df = rename_columns(df)
    df.to_sql(
        name=table,
        con=engine,
        if_exists="replace",
        index=False,
        chunksize=1000,
        method="multi",
    )
    print(f"{len(df)} lines created in {table}")