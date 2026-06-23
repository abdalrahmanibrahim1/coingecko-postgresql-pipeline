from src.load import get_connection
from pathlib import Path
def get_latest_bitcoin_price():
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, price_usd, snapshot_time
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
    conn = get_connection()
    cursor = conn.cursor()    
    cursor.execute("""
        SELECT coin_name, price_usd, snapshot_time
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


def generate_report():
    latest_bitcoin = get_latest_bitcoin_price()
    latest_ethereum = get_latest_ethereum_price()
    highest_prices = get_highest_prices_by_coin()
    average_prices = get_average_prices_by_coin()
    daily_stats = get_daily_statistics()

    lines = []

    lines.append("Crypto Price Report")
    lines.append("===================")
    lines.append("")

    coin_name, price, snapshot_time = latest_bitcoin
    lines.append(f"Latest {coin_name} price: ${price:,.2f}")
    lines.append(f"API snapshot time: {snapshot_time}")

    lines.append("")

    coin_name, price, snapshot_time = latest_ethereum
    lines.append(f"Latest {coin_name} price: ${price:,.2f}")
    lines.append(f"API snapshot time: {snapshot_time}")

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

    report_path = Path("reports/crypto_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Report generated: {report_path}")
if __name__ == "__main__":
    generate_report()