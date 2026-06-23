import requests


def fetch_crypto_data():
    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum"
        "&vs_currencies=usd"
        "&include_market_cap=true"
        "&include_24hr_vol=true"
        "&include_last_updated_at=true"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()