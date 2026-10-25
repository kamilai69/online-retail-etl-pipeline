from pathlib import Path
from sqlalchemy import text

SQL_DIR = Path(__file__).parent.parent / "sql"

def build_model(engine):
    """Create tables and procedures, then fill the model."""
    with engine.begin() as conn:
        for file in sorted(SQL_DIR.glob("*.sql")):
            conn.exec_driver_sql(file.read_text(encoding="utf-8"))
        conn.execute(text("call refresh()"))
    print("Model refreshed")