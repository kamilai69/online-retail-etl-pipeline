from db import get_engine
from extract import extract
from transform import transform
from load import load

def main() :
    engine = get_engine()
    df = transform(extract())
    load(df, engine, table="sales")

if __name__ == "__main__":
    main()