import pandas as pd
import kagglehub
import os

def extract():
    """Load the CSV. Download the latest version from Kaggle."""
    folder = kagglehub.dataset_download("mashlyn/online-retail-ii-uci")
    path = os.path.join(folder, "online_retail_II.csv")
    return pd.read_csv(path, dtype={"Invoice": str, "StockCode": str})