import copy

import pytest

from src.validate import validate_data


@pytest.fixture
def valid_data():
    """
    Return a valid CoinGecko-style API response used as the base case
    for validation tests.
    """
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
            "last_updated_at": 1782062692,
        },
    }

def test_validate_data_accepts_valid_data(valid_data):
    validate_data(valid_data)


def test_validate_data_rejects_non_dictionary():
    with pytest.raises(ValueError):
        validate_data(123)


def test_validate_data_rejects_unexpected_coin_keys(valid_data):
    """
    The pipeline only supports Bitcoin and Ethereum, so extra or replaced
    coin keys should fail validation.
    """
    bad_data = copy.deepcopy(valid_data)
    bad_data["dogecoin"] = bad_data.pop("ethereum")

    with pytest.raises(ValueError):
        validate_data(bad_data)


def test_validate_data_rejects_missing_coin_keys(valid_data):
    bad_data = copy.deepcopy(valid_data)
    del bad_data["ethereum"]
        
    with pytest.raises(ValueError):
        validate_data(bad_data)


def test_validate_data_rejects_coin_value_not_dictionary(valid_data):
    bad_data = copy.deepcopy(valid_data)
    bad_data["ethereum"] = 123
    
    with pytest.raises(ValueError):
        validate_data(bad_data)


def test_validate_data_rejects_missing_fields(valid_data):
    bad_data = copy.deepcopy(valid_data)
    del bad_data["bitcoin"]["last_updated_at"]

    with pytest.raises(ValueError):
        validate_data(bad_data)


def test_validate_data_rejects_non_numeric_field(valid_data):
    bad_data = copy.deepcopy(valid_data)
    bad_data["bitcoin"]["usd"] = "65000"

    with pytest.raises(ValueError):
        validate_data(bad_data)


def test_validate_data_rejects_negative_values(valid_data):
    bad_data = copy.deepcopy(valid_data)
    bad_data["ethereum"]["usd"] = -2
    
    with pytest.raises(ValueError):
        validate_data(bad_data)