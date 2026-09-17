-- Idempotent: safe to re-run against a database that already has the visits table
-- (important since this runs against RDS, which already has production data,
-- not just against a fresh local container).

CREATE TABLE IF NOT EXISTS visits (
    id SERIAL PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0
);

INSERT INTO visits (id, count)
VALUES (1, 0)
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
