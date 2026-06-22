import os
import psycopg2
from dotenv import load_dotenv

def get_connection():

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
    conn = get_connection()
    cursor = conn.cursor()
    for row in rows:
        cursor.execute("""
            INSERT INTO crypto_prices (
                coin_name,
                symbol,
                price_usd,
                market_cap,
                volume_24h,
                snapshot_time,
                ingestion_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
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
    conn.close()

if __name__ == "__main__":
    pass