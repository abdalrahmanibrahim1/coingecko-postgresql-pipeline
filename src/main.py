from extract import fetch_crypto_data
from validate import validate_data


data = fetch_crypto_data()
validate_data(data)

print("Validation passed.")