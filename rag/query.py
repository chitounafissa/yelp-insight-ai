import os
import sys
from pathlib import Path

import chromadb
import ollama
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

CHROMA_PATH = Path(__file__).resolve().parent.parent / "chroma_db"
COLLECTION_NAME = "yelp_reviews"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
TOP_K = 5

SYSTEM_PROMPT = (
    "Tu es un assistant qui répond à des questions sur des commerces de Philadelphia "
    "en te basant UNIQUEMENT sur les avis clients fournis ci-dessous. "
    "Si les avis ne permettent pas de répondre, dis-le clairement plutôt que d'inventer."
)


def retrieve(question: str, embedder: SentenceTransformer, collection, top_k: int = TOP_K):
    query_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=top_k)
    return list(zip(results["documents"][0], results["metadatas"][0]))


def build_context(retrieved) -> str:
    blocks = [
        f"- Commerce : {meta['business_name']} ({meta['stars']}★) — Avis : {text}"
        for text, meta in retrieved
    ]
    return "\n".join(blocks)


def ask(question: str) -> str:
    embedder = SentenceTransformer(EMBEDDING_MODEL)
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_collection(COLLECTION_NAME)

    retrieved = retrieve(question, embedder, collection)
    context = build_context(retrieved)

    response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Avis clients pertinents :\n{context}\n\nQuestion : {question}"},
        ],
    )
    return response["message"]["content"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python rag/query.py "ta question"')
        sys.exit(1)

    print(ask(sys.argv[1]))
