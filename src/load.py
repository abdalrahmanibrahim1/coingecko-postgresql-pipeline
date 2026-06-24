import os
import psycopg2
from dotenv import load_dotenv

def get_connection():
    """
    Create a PostgreSQL connection using environment variables.

    load_dotenv() supports local development by reading values from .env.
    In Docker, the same variables are provided by docker-compose.yml.
    """

    load_dotenv()

    conn = psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
        )
        
    return conn

def insert_crypto_prices(rows):
    """
    Insert transformed crypto price rows into PostgreSQL.

    Each row is a dictionary produced by transform_data() and matches
    the crypto_prices table columns.

    snapshot_time represents the API's as-of time.
    ingestion_time represents when this pipeline run loaded the row.
    """
    conn = get_connection()
    cursor = conn.cursor()

    for row in rows:
        # Use parameterized SQL to pass values safely and let psycopg2 handle type conversion.
        # ON CONFLICT skips duplicate coin/snapshot pairs, making the load incremental.
        cursor.execute("""
            INSERT INTO crypto_prices (
                coin_name,
                symbol,
                price_usd,
                market_cap,
                volume_24h,
                snapshot_time,
                ingestion_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (coin_name, snapshot_time) DO NOTHING;
        """,
            (
                row["coin_name"],
                row["symbol"],
                row["price_usd"],
                row["market_cap"],
                row["volume_24h"],
                row["snapshot_time"],
                row["ingestion_time"],
            )
        )

    conn.commit()
    cursor.close()
    conn.close()