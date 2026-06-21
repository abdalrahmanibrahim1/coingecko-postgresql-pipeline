# CoinGecko -> PostgreSQL ETL Pipeline

Extracts Bitcoin and Ethereum market data from the CoinGecko API, validates and
transforms it, loads it into PostgreSQL, and generates reports.

## Pipeline

REST API -> JSON -> Validation -> Transformation -> PostgreSQL -> Reports

## Setup

```
pip install -r requirements.txt
cp .env.example .env  # fill in DB credentials
```

## Usage

```
python src/main.py
```

## Schema

Table `crypto_prices`: id, coin_name, symbol, price_usd, market_cap, volume_24h, snapshot_time
