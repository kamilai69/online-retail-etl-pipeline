"""
TRANSFORM step of the ETL project - Online Retail II dataset (Kaggle).

Each function takes a DataFrame and returns a transformed DataFrame.
No prints here: findings, measurements and checks are in the notebook.
Functions are listed in the order they must be applied (see STEPS at the bottom).
"""
import pandas as pd

COUNTRIES = {
    "EIRE": "Ireland",
    "RSA": "Republic of South Africa",
    "West Indies": "Caribbean",
    "USA": "United States of America",
    "Korea": "South Korea",
    "European Community": None,
    "Unspecified": None,
}

# Lines that are not products
NON_PRODUCT_WORDS = ("postage|discount|dotcom|manual|test|samples|debt|"
                     "bank charges|amazon|commission|adjustment")

# Order error categories.
ERROR_CATEGORIES = {
    "QUALITY_ERROR": "bad quality|damp|rusty|dirt|incorrectly made|mouldy|smudges|thrown|discoloured",
    "MIXING_ERROR": "mixed",
    "DAMAGE_ERROR": "damages|damaged|dagamed|smashed|wet|destroyed|crushed",
    "MISSING_ERROR": "missing|lost",
    "SOLD_ERROR": ("barecode|barcode|stock creditted wrongly|no stock|wrong barecode|"
                   "wrongly coded|wrongly marked|wrongly sold|wrongly mrked|mistake"),
}

# All error words combined
ERROR_WORDS = "|".join(ERROR_CATEGORIES.values())

# Inconsistent invoices
OUTLIER_INVOICES = ["581483", "C581484", "541431", "C541433", "556444", "C556448"]

def fix_types(df):
    """Customer ID float -> integer, dates to datetime."""
    result = df.copy()
    result["Customer ID"] = result["Customer ID"].astype("Int64")
    result["InvoiceDate"] = pd.to_datetime(
        result["InvoiceDate"], format="%Y-%m-%d %H:%M:%S")
    return result


def normalize_text(df):
    """Remove extra spaces and convert to uppercase."""
    result = df.copy()
    for column in ["StockCode", "Description"]:
        result[column] = result[column].str.strip().str.upper()
    return result


def standardize_countries(df):
    """Harmonized country names, non-geographic values -> missing."""
    result = df.copy()
    result["Country"] = result["Country"].replace(COUNTRIES)
    return result


def remove_duplicates(df):
    """Remove lines that are identical on every column."""
    result = df.copy()
    return result.drop_duplicates()


def remove_missing_descriptions(df):
    result = df.copy()
    return result[result["Description"].notna()]


def remove_non_products(df):
    """Remove lines that are not products (postage, bank charges, tests...)."""
    result = df.copy()
    return result[~result["Description"].str.contains(NON_PRODUCT_WORDS, case=False, na=False)]


def categorize_errors(df):
    """Replace the description of order errors (zero-price lines) with their category."""
    result = df.copy()
    zero_price = result["Price"] == 0
    for category, words in ERROR_CATEGORIES.items():
        is_category = result["Description"].str.contains(words, case=False, na=False)
        result.loc[zero_price & is_category, "Description"] = category
    return result


def remove_zero_prices(df):
    """Remove zero-price lines, except order errors (already categorized)."""
    result = df.copy()
    keep = (result["Price"] != 0) | result["Description"].isin(ERROR_CATEGORIES.keys())
    return result[keep]


def classify_lines(df):
    """Add line_type: error / refund (invoice starting with C) / sale."""
    result = df.copy()
    result["line_type"] = None
    result.loc[result["Description"].str.contains("ERROR", na=False), "line_type"] = "error"
    result.loc[result["Invoice"].str.startswith("C", na=False), "line_type"] = "refund"
    result.loc[
        (~result["Invoice"].str.startswith("C", na=False))
        & (~result["Description"].str.contains("ERROR")),
        "line_type"
    ] = "sale"
    return result


def unify_descriptions(df):
    """One description per StockCode: the most frequent one (except on error lines)."""
    result = df.copy()

    is_product = result["line_type"] != "error"

    reference = {}
    for code, group in result.groupby("StockCode"):
        counts = group["Description"].value_counts()
        most_frequent = counts.index[0]
        reference[code] = most_frequent

    codes = result.loc[is_product, "StockCode"]
    new_descriptions = codes.map(reference)
    result.loc[is_product, "Description"] = new_descriptions

    return result


def remove_outliers(df):
    """Remove the inconsistent invoices (sales and their refunds)."""
    result = df.copy()
    return result[~result["Invoice"].isin(OUTLIER_INVOICES)]


def fill_unknown_customers(df):
    """Missing Customer ID -> -1 (unknown customer)."""
    result = df.copy()
    result.loc[result["Customer ID"].isna(), "Customer ID"] = -1
    return result


def add_revenue(df):
    result = df.copy()
    result["Revenue"] = result["Price"] * result["Quantity"]
    return result


STEPS = [
    fix_types,
    normalize_text,
    standardize_countries,
    remove_duplicates,
    remove_missing_descriptions,
    remove_non_products,
    categorize_errors,
    remove_zero_prices,
    classify_lines,
    unify_descriptions,
    remove_outliers,
    fill_unknown_customers,
    add_revenue,
]


def transform(df):
    """Apply every step in order."""
    for step in STEPS:
        df = step(df)
    return df


