import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CHROMA_PATH = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "yelp_reviews"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
SAMPLE_SIZE = 50_000
BATCH_SIZE = 256


def fetch_review_sample(engine, limit: int):
    query = text("""
        SELECT r.review_id, r.business_id, r.stars, r.text, r.review_date,
               b.name AS business_name, b.categories
        FROM review r
        JOIN business b ON b.business_id = r.business_id
        ORDER BY random()
        LIMIT :limit
    """)
    with engine.connect() as conn:
        return conn.execute(query, {"limit": limit}).mappings().all()


def build_index() -> None:
    engine = create_engine(os.environ["DATABASE_URL"])

    print(f"Échantillonnage de {SAMPLE_SIZE} avis depuis PostgreSQL...")
    rows = fetch_review_sample(engine, SAMPLE_SIZE)
    print(f"  {len(rows)} avis récupérés.")

    print(f"Chargement du modèle d'embeddings ({EMBEDDING_MODEL})...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    print("Génération des embeddings et indexation dans ChromaDB...")
    total = len(rows)
    for i in range(0, total, BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        texts = [r["text"] or "" for r in batch]
        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            ids=[r["review_id"] for r in batch],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "business_id": r["business_id"],
                    "business_name": r["business_name"],
                    "categories": r["categories"] or "",
                    "stars": float(r["stars"]),
                    "review_date": str(r["review_date"]),
                }
                for r in batch
            ],
        )
        print(f"  {min(i + BATCH_SIZE, total)}/{total} avis indexés")

    print(f"Terminé. Index ChromaDB sauvegardé dans {CHROMA_PATH}")


if __name__ == "__main__":
    build_index()
