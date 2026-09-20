import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


@pytest.fixture(scope="session")
def engine():
    return create_engine(os.environ["DATABASE_URL"])


def test_business_table_not_empty(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM business")).scalar()
    assert count > 0


def test_review_table_not_empty(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM review")).scalar()
    assert count > 0


def test_no_null_business_ids(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM business WHERE business_id IS NULL")).scalar()
    assert count == 0


def test_review_stars_within_valid_range(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM review WHERE stars < 1 OR stars > 5")).scalar()
    assert count == 0


def test_no_orphan_reviews(engine):
    """Chaque avis doit être rattaché à un commerce existant (intégrité référentielle)."""
    query = """
        SELECT count(*) FROM review r
        LEFT JOIN business b ON r.business_id = b.business_id
        WHERE b.business_id IS NULL
    """
    with engine.connect() as conn:
        count = conn.execute(text(query)).scalar()
    assert count == 0


def test_all_businesses_are_philadelphia(engine):
    with engine.connect() as conn:
        count = conn.execute(text("SELECT count(*) FROM business WHERE city != 'Philadelphia'")).scalar()
    assert count == 0
