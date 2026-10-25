from db import get_engine
from extract import extract
from transform import transform
from load import load
from model import build_model

def main() :
    engine = get_engine()
    df = transform(extract())
    load(df, engine, table="sales")
    build_model(engine)

if __name__ == "__main__":
    main()
