import requests


def fetch_crypto_data():
    """
    Fetch Bitcoin and Ethereum market data from the CoinGecko API.

    The response includes USD price, market cap, 24-hour volume,
    and CoinGecko's last updated timestamp for each coin.
    """

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
        "?ids=bitcoin,ethereum"
        "&vs_currencies=usd"
        "&include_market_cap=true"
        "&include_24hr_vol=true"
        "&include_last_updated_at=true"
    )
   
    response = requests.get(url)
    
    #Stop the pipeline early if CoinGecko returns an unsuccessful HTTP response
    response.raise_for_status()

    return response.json()