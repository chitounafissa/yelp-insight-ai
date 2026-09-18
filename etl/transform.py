import pandas as pd

BUSINESS_COLUMNS = ["business_id", "name", "city", "state", "stars", "review_count", "categories"]
REVIEW_COLUMNS = ["review_id", "business_id", "user_id", "stars", "text", "review_date", "useful", "funny", "cool"]


def transform_businesses(businesses: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(businesses)
    df = df[BUSINESS_COLUMNS]
    df = df.dropna(subset=["business_id"])
    df = df.drop_duplicates(subset=["business_id"])
    return df


def transform_reviews(reviews) -> pd.DataFrame:
    df = pd.DataFrame(reviews)
    df = df.rename(columns={"date": "review_date"})
    df = df[REVIEW_COLUMNS]
    df["review_date"] = pd.to_datetime(df["review_date"]).dt.date
    df = df.dropna(subset=["review_id", "business_id"])
    df = df.drop_duplicates(subset=["review_id"])
    return df
