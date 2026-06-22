from extract import fetch_crypto_data
from validate import validate_data
from transform import transform_data
from load import insert_crypto_prices
from report import generate_report


def main():
    data = fetch_crypto_data()

    validate_data(data)
    print("Validation passed.")

    transformed_data = transform_data(data)

    insert_crypto_prices(transformed_data)
    print("Data loaded successfully.")

    generate_report()
    print("Report generated successfully.")


if __name__ == "__main__":
    main()