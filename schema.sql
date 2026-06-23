CREATE TABLE IF NOT EXISTS crypto_prices (
    id SERIAL PRIMARY KEY,
    coin_name VARCHAR(50) NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    price_usd NUMERIC NOT NULL,
    market_cap NUMERIC NOT NULL,
    volume_24h NUMERIC NOT NULL,
    snapshot_time TIMESTAMP NOT NULL,
    ingestion_time TIMESTAMP NOT NULL
);