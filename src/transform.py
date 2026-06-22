from extract import fetch_crypto_data
from validate import validate_data
from datetime import datetime
def transform_data(data):
    rows = []
    symbols ={
        "bitcoin":"BTC",
        "ethereum":"ETH"
              }
    name = {
        "bitcoin":"Bitcoin",
        "ethereum":"Ethereum"
    }
    ingestion_time = datetime.now()

    for coin in data:
        snapshot_time = datetime.fromtimestamp(data[coin]["last_updated_at"])
        row = {
            "coin_name" : name[coin],
            "symbol": symbols[coin],
            "price_usd" : data[coin]["usd"],
            "market_cap": data[coin]["usd_market_cap"],
            "volume_24h": data[coin]["usd_24h_vol"],
            "snapshot_time": snapshot_time,
            "ingestion_time": ingestion_time
        }
        rows.append(row)

    return rows
if __name__ == "__main__":
    data = fetch_crypto_data()
    validate_data(data)
    transformed = transform_data(data)
    for i in transformed:
        print(i)
    