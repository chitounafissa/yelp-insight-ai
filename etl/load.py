import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_engine() -> Engine:
    return create_engine(os.environ["DATABASE_URL"])


def truncate_tables(engine: Engine) -> None:
    """Vide les tables avant un nouveau chargement, pour pouvoir relancer l'ETL sans erreur de clé dupliquée."""
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE review, business CASCADE"))


def load_businesses(df: pd.DataFrame, engine: Engine) -> None:
    df.to_sql("business", engine, if_exists="append", index=False, method="multi", chunksize=1000)


def load_reviews(df: pd.DataFrame, engine: Engine) -> None:
    df.to_sql("review", engine, if_exists="append", index=False, method="multi", chunksize=1000)
