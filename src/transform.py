from datetime import datetime
def transform_data(data):
    """
    Transform the nested CoinGecko API response into database-ready rows.

    Each output row is a dictionary matching the crypto_prices table schema.
    snapshot_time comes from CoinGecko's last_updated_at timestamp.
    ingestion_time is shared across all rows from the same pipeline run.
    """
    rows = []

    symbols ={
        "bitcoin":"BTC",
        "ethereum":"ETH"
    }

    names = {
        "bitcoin":"Bitcoin",
        "ethereum":"Ethereum"
    }

    ingestion_time = datetime.now()

    for coin in data:
        snapshot_time = datetime.fromtimestamp(data[coin]["last_updated_at"])

        row = {
            "coin_name" : names[coin],
            "symbol": symbols[coin],
            "price_usd" : data[coin]["usd"],
            "market_cap": data[coin]["usd_market_cap"],
            "volume_24h": data[coin]["usd_24h_vol"],
            "snapshot_time": snapshot_time,
            "ingestion_time": ingestion_time
        }
        
        rows.append(row)

    return rows
