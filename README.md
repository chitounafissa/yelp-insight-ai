# Yelp Insight AI

![CI](https://github.com/chitounafissa/yelp-insight-ai/actions/workflows/ci.yml/badge.svg)

Pipeline data + assistant IA (RAG) sur des avis clients réels (Yelp Open Dataset).
Projet construit pour illustrer une chaîne complète : **ETL → base de données relationnelle → recherche sémantique → génération de réponse en langage naturel**, exposée via une API et conteneurisée.

## Ce que fait le projet

1. **ETL** : extrait les commerces et avis de Philadelphia depuis le Yelp Open Dataset (5+ Go de JSON Lines) et les charge dans PostgreSQL.
2. **RAG (Retrieval-Augmented Generation)** : indexe un échantillon d'avis dans une base vectorielle (ChromaDB) via des embeddings locaux, puis répond à des questions en langage naturel en combinant recherche sémantique + génération par un LLM local (Ollama / Llama 3.2).
3. **API** : expose l'assistant via FastAPI (`POST /ask`).
4. **Qualité & CI** : tests automatisés (intégrité des données, contraintes métier) exécutés à chaque push via GitHub Actions.

## Architecture

```
yelp_academic_dataset_*.json (Yelp Open Dataset)
        │
        ▼
   etl/extract.py  →  etl/transform.py  →  etl/load.py
        │                                       │
        │                                       ▼
        │                              PostgreSQL (Docker)
        │
        ▼
  rag/embed.py  (sentence-transformers)
        │
        ▼
   ChromaDB (index vectoriel local)
        │
        ▼
  rag/query.py  →  Ollama (Llama 3.2, local)
        │
        ▼
   app/api.py  (FastAPI : /ask, /health)
```

## Stack technique

| Domaine | Outil |
|---|---|
| Langage | Python 3.11 |
| Base de données | PostgreSQL (Docker) |
| ORM / connexion DB | SQLAlchemy |
| Index vectoriel | ChromaDB |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`, local, gratuit) |
| Génération de réponses | Ollama (`llama3.2:3b`, local, gratuit) |
| API | FastAPI |
| Conteneurisation | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Tests | pytest |

## Choix techniques et compromis

- **Filtrage sur une seule ville (Philadelphia)** : le dataset complet contient 150k+ commerces et 7M+ avis. Philadelphia est la ville la plus représentée (14 567 commerces), offrant un volume réaliste sans nécessiter d'infrastructure distribuée.
- **Échantillon de 50 000 avis indexés dans ChromaDB** (sur 967 517 chargés en base) : compromis entre couverture sémantique et temps d'indexation sur CPU. Les 967 517 avis, eux, sont bien tous en base PostgreSQL (utilisables pour des analyses SQL classiques).
- **Ollama plutôt qu'une API LLM cloud payante** : permet de faire tourner tout le pipeline gratuitement et hors-ligne après installation, au prix d'une génération plus lente et d'un modèle moins puissant qu'un LLM propriétaire de pointe.
- **Streaming du fichier `review.json` (5,3 Go)** ligne par ligne plutôt que chargement complet en mémoire, pour rester utilisable sur une machine avec des ressources standards.
- **CI sur données fictives** : GitHub Actions ne redistribue pas le dataset Yelp (contraintes de licence) ; la CI valide donc la logique des tests de qualité sur un petit jeu de données synthétique respectant les mêmes règles métier.

## Lancer le projet

### Prérequis
- Python 3.11
- Docker Desktop
- [Ollama](https://ollama.com) avec le modèle `llama3.2:3b` (`ollama pull llama3.2:3b`)
- Le [Yelp Open Dataset](https://www.yelp.com/dataset) (fichiers `yelp_academic_dataset_business.json` et `yelp_academic_dataset_review.json` à placer dans `data/raw/`)

### Installation

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
cp .env.example .env            # puis renseigner les valeurs
```

### Base de données

```bash
docker compose up -d postgres
```

### Pipeline ETL (extraction → transformation → chargement PostgreSQL)

```bash
python run_etl.py
```

### Indexation RAG (embeddings → ChromaDB)

```bash
python rag/embed.py
```

### Lancer l'API

En local :
```bash
uvicorn app.api:app --reload
```

Ou entièrement conteneurisé (Postgres + API) :
```bash
docker compose up -d --build
```

L'API est alors disponible sur `http://localhost:8000/docs` (documentation interactive Swagger).

### Exemple d'utilisation

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Quels sont les meilleurs restaurants de sushis à Philadelphia ?"}'
```

## Tests

```bash
python -m pytest tests/ -v
```

Les tests vérifient : absence de valeurs nulles sur les clés primaires, plage de notes valide (1-5), intégrité référentielle (pas d'avis orphelin), cohérence du filtre géographique. Exécutés automatiquement à chaque push via GitHub Actions.

## Structure du projet

```
yelp-insight-ai/
├── data/raw/          # Données brutes Yelp (non versionnées)
├── etl/               # Extraction, transformation, chargement
├── db/                # Schéma PostgreSQL
├── rag/               # Embeddings + recherche/génération RAG
├── app/                # API FastAPI
├── tests/              # Tests de qualité des données
├── .github/workflows/  # CI/CD
├── run_etl.py           # Point d'entrée du pipeline ETL
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
