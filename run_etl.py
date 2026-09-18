from etl.extract import extract_businesses, extract_reviews
from etl.load import get_engine, load_businesses, load_reviews, truncate_tables
from etl.transform import transform_businesses, transform_reviews

CITY = "Philadelphia"
STATE = "PA"


def main() -> None:
    print(f"Extraction des commerces de {CITY}, {STATE}...")
    businesses = extract_businesses(CITY, STATE)
    print(f"  {len(businesses)} commerces trouvés.")

    business_ids = {b["business_id"] for b in businesses}

    print("Extraction des avis correspondants (lecture de review.json, ~5.3 Go, peut prendre 1-2 min)...")
    reviews = list(extract_reviews(business_ids))
    print(f"  {len(reviews)} avis trouvés.")

    print("Transformation des données...")
    business_df = transform_businesses(businesses)
    review_df = transform_reviews(reviews)

    print("Chargement dans PostgreSQL...")
    engine = get_engine()
    truncate_tables(engine)
    load_businesses(business_df, engine)
    load_reviews(review_df, engine)

    print("Terminé.")
    print(f"  business : {len(business_df)} lignes chargées")
    print(f"  review   : {len(review_df)} lignes chargées")


if __name__ == "__main__":
    main()
