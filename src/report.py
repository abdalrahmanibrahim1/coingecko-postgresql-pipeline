import logging
from src.load import get_connection
from pathlib import Path

logger = logging.getLogger(__name__)

def get_latest_bitcoin_price():
    """
    Return the latest Bitcoin price snapshot.

    Rows are ordered by ingestion_time because the latest report should use
    the most recent pipeline run.
    """
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, price_usd, snapshot_time, ingestion_time
        FROM crypto_prices
        WHERE coin_name = 'Bitcoin'
        ORDER BY ingestion_time DESC
        LIMIT 1;
    """
    )

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


def get_latest_ethereum_price():
    """
    Return the latest Ethereum price snapshot.

    Rows are ordered by ingestion_time because the latest report should use
    the most recent pipeline run.
    """
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, price_usd, snapshot_time, ingestion_time
        FROM crypto_prices
        WHERE coin_name = 'Ethereum'
        ORDER BY ingestion_time DESC
        LIMIT 1;
    """
    )

    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_highest_prices_by_coin():
    """
    Return the highest recorded USD price for each coin across all stored snapshots.
    """
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, MAX(price_usd)
        FROM crypto_prices
        GROUP BY coin_name
        ORDER BY coin_name
    """
    )

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_average_prices_by_coin():
    """
    Return the average USD price for each coin across all stored snapshots.
    """
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, AVG(price_usd)
        FROM crypto_prices
        GROUP BY coin_name
        ORDER BY coin_name;
    """
    )

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def get_daily_statistics():
    """
    Return daily min, max, and average prices for each coin.

    DATE(snapshot_time) groups API snapshots by calendar day so the report
    can summarize historical price movement by date.
    """
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT
            coin_name,
            DATE(snapshot_time) as snapshot_date,
            MIN(price_usd),
            MAX(price_usd),
            AVG(price_usd)
        FROM crypto_prices
        GROUP BY coin_name, DATE(snapshot_time)
        ORDER BY snapshot_date, coin_name;
    """
    )

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def format_datetime(value):
    """Format database timestamps without microseconds for report output."""
    return value.strftime("%Y-%m-%d %H:%M:%S")

def get_recent_snapshot():
    """
    Return the most recent stored crypto price snapshots.

    This helps prove the pipeline stores historical data over time.
    Results are ordered by ingestion_time so the newest pipeline-loaded
    records appear first.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Show the latest stored rows so users can inspect historical snapshots
    # created by previous pipeline runs.
    cursor.execute("""
        SELECT coin_name, price_usd, snapshot_time, ingestion_time
        FROM crypto_prices
        ORDER BY ingestion_time DESC
        LIMIT 10;
    """
    )

    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def generate_report():
    """
    Generate a human-readable crypto price report from PostgreSQL query results.

    The report is written to reports/crypto_report.txt so it can be viewed
    after local or Docker pipeline runs.
    """
    latest_bitcoin = get_latest_bitcoin_price()
    latest_ethereum = get_latest_ethereum_price()
    highest_prices = get_highest_prices_by_coin()
    average_prices = get_average_prices_by_coin()
    daily_stats = get_daily_statistics()
    recent_snapshot = get_recent_snapshot()

    lines = []

    lines.append("Crypto Price Report")
    lines.append("===================")
    lines.append("")

    coin_name, price, snapshot_time, ingestion_time = latest_bitcoin
    lines.append(f"Latest {coin_name} price: ${price:,.2f}")
    lines.append(f"API snapshot time: {snapshot_time}")
    lines.append(f"Ingested at: {format_datetime(ingestion_time)}")

    lines.append("")

    coin_name, price, snapshot_time, ingestion_time = latest_ethereum
    lines.append(f"Latest {coin_name} price: ${price:,.2f}")
    lines.append(f"API snapshot time: {snapshot_time}")
    lines.append(f"Ingested at: {format_datetime(ingestion_time)}")

    lines.append("")
    lines.append("Highest Recorded Prices")
    lines.append("-----------------------")

    for coin_name, highest_price in highest_prices:
        lines.append(f"{coin_name}: ${highest_price:,.2f}")

    lines.append("")
    lines.append("Average Prices")
    lines.append("--------------")

    for coin_name, average_price in average_prices:
        lines.append(f"{coin_name}: ${average_price:,.2f}")

    lines.append("")
    lines.append("Daily Summary Statistics")
    lines.append("------------------------")

    for coin_name, snapshot_date, min_price, max_price, avg_price in daily_stats:
        lines.append(
            f"{snapshot_date} | {coin_name} | "
            f"Min: ${min_price:,.2f} | "
            f"Max: ${max_price:,.2f} | "
            f"Avg: ${avg_price:,.2f}"
        )

    lines.append("")
    lines.append("Recent Historical Snapshots")
    lines.append("------------------------")

    for coin_name, price_usd, snapshot_time, ingestion_time in recent_snapshot:
        lines.append(
            f"{snapshot_time} | {coin_name} | "
            f"{price_usd} | Ingested: {format_datetime(ingestion_time)}"
        )
    
    report_path = Path("reports/crypto_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    logger.info("Report generated: %s", report_path)