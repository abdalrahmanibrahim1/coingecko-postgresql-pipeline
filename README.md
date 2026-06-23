# CoinGecko PostgreSQL ETL Pipeline

A Python data engineering project that extracts cryptocurrency market data from the CoinGecko API, validates and transforms the response, loads historical snapshots into PostgreSQL, and generates SQL-based reports.

This project demonstrates a small but realistic ETL workflow:

```text
CoinGecko API → JSON Extraction → Validation → Transformation → PostgreSQL → SQL Reports
```

---

## Project Overview

The pipeline collects market data for:

* Bitcoin
* Ethereum

For each coin, the pipeline stores:

* coin name
* symbol
* USD price
* market cap
* 24-hour volume
* API snapshot time
* ingestion time

Each pipeline run inserts a new snapshot into PostgreSQL, allowing historical price tracking over time.

---

## Tech Stack

* Python
* PostgreSQL
* Docker
* Docker Compose
* CoinGecko API
* pytest
* psycopg2
* python-dotenv
* requests

---

## Project Structure

```text
coingecko-postgresql-pipeline/
├── data/
├── reports/
│   └── crypto_report.txt
├── src/
│   ├── __init__.py
│   ├── extract.py
│   ├── validate.py
│   ├── transform.py
│   ├── load.py
│   ├── report.py
│   └── main.py
├── tests/
│   ├── __init__.py
│   ├── test_validate.py
│   └── test_transform.py
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── schema.sql
└── README.md
```

---

## Database Schema

The pipeline loads data into the `crypto_prices` table.

```sql
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
```

### Time Columns

`timestamp_time` and `ingestion_time` are intentionally different concepts:

* `snapshot_time`: when CoinGecko says the market data was last updated
* `ingestion_time`: when this pipeline inserted the row into PostgreSQL

---

## Pipeline Steps

### 1. Extract

`src/extract.py` sends a request to the CoinGecko API and returns JSON market data for Bitcoin and Ethereum.

The extraction step uses:

```python
response.raise_for_status()
```

to fail clearly if the API request is unsuccessful.

### 2. Validate

`src/validate.py` validates the API response before loading it.

Validation checks include:

* top-level response must be a dictionary
* expected coins must be exactly Bitcoin and Ethereum
* each coin must contain all required fields
* values must be numeric
* numeric values must not be negative

### 3. Transform

`src/transform.py` converts the nested API JSON into database-ready rows.

Example transformed row:

```python
{
    "coin_name": "Bitcoin",
    "symbol": "BTC",
    "price_usd": 62507.00,
    "market_cap": 123456789,
    "volume_24h": 987654321,
    "snapshot_time": datetime(...),
    "ingestion_time": datetime(...)
}
```

### 4. Load

`src/load.py` connects to PostgreSQL and inserts the transformed rows into the `crypto_prices` table.

### 5. Report

`src/report.py` queries PostgreSQL and writes a text report to:

```text
reports/crypto_report.txt
```

The report includes:

* latest Bitcoin price
* latest Ethereum price
* highest recorded price by coin
* average price by coin
* daily summary statistics

---

## Running with Docker

Docker is the recommended way to run this project.

The Docker setup creates:

* a PostgreSQL container
* a Python ETL app container

### 1. Build and run the pipeline

From the project root:

```bash
docker compose up --build
```

The Python app will:

1. wait for PostgreSQL to become healthy
2. run the ETL pipeline
3. insert Bitcoin and Ethereum rows
4. generate the report
5. exit successfully

The app container exiting with code `0` is expected because this is a batch ETL job, not a web server.

---

### 2. Check the generated report

```bash
cat reports/crypto_report.txt
```

On Windows PowerShell:

```powershell
Get-Content reports/crypto_report.txt
```

---

### 3. Inspect the Docker PostgreSQL database

```bash
docker exec -it crypto-postgres psql -U postgres -d crypto_db
```

Then run:

```sql
SELECT * FROM crypto_prices;
```

Exit PostgreSQL:

```sql
\q
```

---

### 4. Stop the containers

```bash
docker compose down
```

To fully reset the Docker database volume:

```bash
docker compose down -v
```

Use `-v` only when you want to delete the Docker PostgreSQL data and start from a fresh database.

---

## Running Locally Without Docker

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Create a local `.env` file

Copy `.env.example` into `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=crypto_db
DB_USER=postgres
DB_PASSWORD=your_password_here
```

Do not commit `.env`.

---

### 4. Create the PostgreSQL table

Run the SQL inside `schema.sql` against your local PostgreSQL database.

---

### 5. Run the pipeline

```bash
python -m src.main
```

---

## Running Tests

Run tests from the project root:

```bash
python -m pytest
```

Current test coverage includes:

* validation logic
* transformation logic

The tests check that:

* valid API data passes validation
* invalid API structures fail validation
* missing fields are rejected
* non-numeric values are rejected
* negative values are rejected
* transformed rows contain the expected fields
* timestamps are converted into Python `datetime` objects

---

## Example Report Output

```text
Crypto Price Report
===================

Latest Bitcoin price: $62,507.00
API snapshot time: 2026-06-23 14:41:33
Ingested at: 2026-06-23 14:41:36

Latest Ethereum price: $1,663.36
API snapshot time: 2026-06-23 14:41:33
Ingested at: 2026-06-23 14:41:36

Highest Recorded Prices
-----------------------
Bitcoin: $62,507.00
Ethereum: $1,663.36

Average Prices
--------------
Bitcoin: $62,507.00
Ethereum: $1,663.36

Daily Summary Statistics
------------------------
2026-06-23 | Bitcoin | Min: $62,507.00 | Max: $62,507.00 | Avg: $62,507.00
2026-06-23 | Ethereum | Min: $1,663.36 | Max: $1,663.36 | Avg: $1,663.36
```

---

## Environment Variables

| Variable      | Description       | Example                             |
| ------------- | ----------------- | ----------------------------------- |
| `DB_HOST`     | PostgreSQL host   | `localhost` locally, `db` in Docker |
| `DB_PORT`     | PostgreSQL port   | `5432`                              |
| `DB_NAME`     | Database name     | `crypto_db`                         |
| `DB_USER`     | Database user     | `postgres`                          |
| `DB_PASSWORD` | Database password | `postgres`                          |

---

## Skills Demonstrated

This project demonstrates:

* REST API extraction
* JSON validation
* data transformation
* PostgreSQL loading
* SQL reporting
* Dockerized development
* environment variable management
* Python package-style imports
* unit testing with pytest
* basic data engineering project structure

---

## Future Improvements

Possible next improvements:

* schedule the pipeline to run automatically
* add integration tests for PostgreSQL loading
* add logging instead of print statements
* export reports as CSV
* load data into a data warehouse
* deploy the pipeline to a cloud environment
