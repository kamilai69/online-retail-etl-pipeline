import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL

load_dotenv() 


def get_engine():
    """Crée l'engine SQLAlchemy à partir des infos du .env."""
    url = URL.create(
        drivername="postgresql+psycopg",
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        database=os.getenv("POSTGRES_DB"),
    )
    return create_engine(url)