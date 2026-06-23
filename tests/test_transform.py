from datetime import datetime
import pytest
from src.transform import transform_data

@pytest.fixture
def valid_api_data():
    return {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692,
        },
        "ethereum": {
            "usd": 1700,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062693,
        },
    }

def test_transform_data_returns_list(valid_api_data):
    rows = transform_data(valid_api_data)

    assert isinstance(rows, list)

def test_transform_data_returns_two_rows(valid_api_data):
    rows = transform_data(valid_api_data)

    assert len(rows) == 2

def test_transform_data_bitcoin_row(valid_api_data):
    rows = transform_data(valid_api_data)
    bitcoin_row = next(row for row in rows if row["symbol"] =="BTC")

    assert bitcoin_row["coin_name"] == "Bitcoin"
    assert bitcoin_row["symbol"] == "BTC"
    assert bitcoin_row["price_usd"] == 65000
    assert bitcoin_row["market_cap"] == 1200000000000
    assert bitcoin_row["volume_24h"] == 25000000000
    assert isinstance(bitcoin_row["snapshot_time"], datetime)
    assert isinstance(bitcoin_row["ingestion_time"], datetime)

def test_transform_data_ethereum_row(valid_api_data):
    rows = transform_data(valid_api_data)
    ethereum_row = next(row for row in rows if row["symbol"] == "ETH")

    assert ethereum_row["coin_name"] == "Ethereum"
    assert ethereum_row["symbol"] == "ETH"
    assert ethereum_row["price_usd"] == 1700
    assert ethereum_row["market_cap"] == 200000000000
    assert ethereum_row["volume_24h"] == 10000000000
    assert isinstance(ethereum_row["snapshot_time"], datetime)
    assert isinstance(ethereum_row["ingestion_time"], datetime)
