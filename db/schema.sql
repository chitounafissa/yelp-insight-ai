-- Exécuté automatiquement par Postgres au premier démarrage du conteneur.

CREATE TABLE IF NOT EXISTS business (
    business_id   VARCHAR(32) PRIMARY KEY,
    name          TEXT NOT NULL,
    city          TEXT,
    state         VARCHAR(10),
    stars         NUMERIC(2,1),
    review_count  INTEGER,
    categories    TEXT
);

CREATE TABLE IF NOT EXISTS review (
    review_id     VARCHAR(32) PRIMARY KEY,
    business_id   VARCHAR(32) REFERENCES business(business_id),
    user_id       VARCHAR(32),
    stars         NUMERIC(2,1),
    text          TEXT,
    review_date   DATE,
    useful        INTEGER,
    funny         INTEGER,
    cool          INTEGER
);

CREATE INDEX IF NOT EXISTS idx_review_business_id ON review(business_id);
