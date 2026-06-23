def validate_data(data):
    required_coins = {"bitcoin", "ethereum"}
    required_fields = ["usd", "usd_market_cap", "usd_24h_vol", "last_updated_at"]

    if not isinstance(data, dict):
        raise ValueError("Invalid API response: expected top-level data to be a dictionary.")

    actual_coins = set(data.keys())

    if actual_coins != required_coins:
        raise ValueError(
            f"Invalid API response: expected coins {required_coins}\nreceived {actual_coins}."
        )

    for coin in required_coins:
        if not isinstance(data[coin], dict):
            raise ValueError(
                f"Invalid API response: expected '{coin}' data to be a dictionary."
            )

        for field in required_fields:
            if field not in data[coin]:
                raise ValueError(
                    f"Invalid API response: missing field '{field}' for '{coin}'."
                )

            if not isinstance(data[coin][field], (int, float)):
                raise ValueError(
                    f"Invalid API response: field '{field}' for '{coin}' must be numeric, "
                    f"but received {type(data[coin][field]).__name__}."
                )
            if data[coin][field] < 0:
                raise ValueError(
                    f"Invalid API response: field '{field}' for '{coin}' cannot be negative."
                )


