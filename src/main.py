from extract import fetch_crypto_data
from validate import validate_data
from transform import transform_data


def main():
    data = fetch_crypto_data()

    validate_data(data)
    print("Validation passed.")

    transformed_data = transform_data(data)

    return transformed_data


if __name__ == "__main__":
    main()