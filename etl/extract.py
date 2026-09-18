import json
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
BUSINESS_FILE = RAW_DIR / "yelp_academic_dataset_business.json"
REVIEW_FILE = RAW_DIR / "yelp_academic_dataset_review.json"


def extract_businesses(city: str, state: str) -> list[dict]:
    """Charge business.json en mémoire (118 Mo) et filtre par ville/état."""
    businesses = []
    with open(BUSINESS_FILE, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record.get("city") == city and record.get("state") == state:
                businesses.append(record)
    return businesses


def extract_reviews(business_ids: set):
    """Parcourt review.json (5.3 Go) ligne par ligne sans le charger en mémoire."""
    with open(REVIEW_FILE, encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record.get("business_id") in business_ids:
                yield record
