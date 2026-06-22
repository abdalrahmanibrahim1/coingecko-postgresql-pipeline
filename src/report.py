from load import get_connection

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




if __name__ == "__main__":
    result = get_daily_statistics()
    for coin_name, date, min_price, max_price,avg_price in result:
        print(f"{coin_name}, {date}, {min_price}, {max_price}, {avg_price}")