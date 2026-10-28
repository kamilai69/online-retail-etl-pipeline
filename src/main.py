from db import get_engine
from extract import extract
from transform import transform
from load import load
from model import build_model


def main():
    engine = get_engine()
    print("Engine acquired.")
    df = transform(extract())
    print("Transformation done.")
    load(df, engine, table="sales")
    print("Loading done.")
    build_model(engine)
    print("SQL modification done.")
    print("End of the pipeline.")


if __name__ == "__main__":
    main()
