from fastapi import FastAPI
from pydantic import BaseModel

from rag.query import ask

app = FastAPI(title="Yelp Insight AI", description="Assistant RAG sur les avis clients Yelp (Philadelphia)")


class Question(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask")
def ask_endpoint(payload: Question):
    answer = ask(payload.question)
    return {"question": payload.question, "answer": answer}
