import logging

from src.extract import fetch_crypto_data
from src.validate import validate_data
from src.transform import transform_data
from src.load import insert_crypto_prices
from src.report import generate_report


# Configure application-wide logging so pipeline runs show timestamps,
# severity levels, module names, and readable progress messages.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """
        Orchestrate the full crypto ETL pipeline.

        Pipeline order:
        1. Extract data from CoinGecko
        2. Validate the API response
        3. Transform nested JSON into database-ready rows
        4. Load rows into PostgreSQL
        5. Generate a report from stored database data
        """
    try:
        logger.info("Starting crypto ETL pipeline.")

        data = fetch_crypto_data()
        logger.info("Data extracted successfully.")

        validate_data(data)
        logger.info("Validation passed.")

        transformed_data = transform_data(data)
        logger.info("Data transformed successfully. Rows prepared: %s", len(transformed_data))

        insert_crypto_prices(transformed_data)
        logger.info("Data loaded successfully.")

        generate_report()
        logger.info("Report generated successfully.")

        logger.info("Crypto ETL pipeline completed successfully.")

    except Exception:
        logger.exception("Crypto ETL pipeline failed.")
        raise


if __name__ == "__main__":
    main()