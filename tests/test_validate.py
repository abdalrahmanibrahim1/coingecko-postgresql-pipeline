from src.validate import validate_data
import pytest

def test_validate_data_accepts_valid_data():
    test_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        },
        "ethereum": {
            "usd": 1700,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062692
        }
    }

    validate_data(test_data)

def test_validate_data_rejects_non_dictionary():
    with pytest.raises(ValueError):
        validate_data(123)

def test_validate_data_rejects_unexpected_coin_keys():
    bad_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        },
        "dogecoin": {
            "usd": 1700,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062692
        }
    }

    with pytest.raises(ValueError):
        validate_data(bad_data)

def test_validate_data_rejects_missing_coin_keys():
    bad_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        }
    }
        
    with pytest.raises(ValueError):
        validate_data(bad_data)

def test_validate_data_rejects_coin_value_not_dictionary():
    bad_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        },
        "ethereum": 123
    }

    with pytest.raises(ValueError):
        validate_data(bad_data)

def test_validate_data_rejects_missing_fields():
    bad_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
        },
        "ethereum": {
            "usd": 1700,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062692
        }
    }
    
    with pytest.raises(ValueError):
        validate_data(bad_data)

def test_validate_data_rejects_not_numeric():
    bad_data = {
        "bitcoin": {
            "usd": "65000",
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        },
        "ethereum": {
            "usd": 1700,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062692
        }
    }

    with pytest.raises(ValueError):
        validate_data(bad_data)

def test_validate_data_rejects_negative_values():
    bad_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1200000000000,
            "usd_24h_vol": 25000000000,
            "last_updated_at": 1782062692
        },
        "ethereum": {
            "usd": -2,
            "usd_market_cap": 200000000000,
            "usd_24h_vol": 10000000000,
            "last_updated_at": 1782062692
        }
    }
    
    with pytest.raises(ValueError):
        validate_data(bad_data)