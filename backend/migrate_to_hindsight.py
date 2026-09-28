import csv
import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


# Load environment variables
load_dotenv()


# Hindsight configuration
API_KEY = os.getenv("HINDSIGHT_API_KEY")

BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "nanami-ai"
)


# Check API key
if not API_KEY:
    raise RuntimeError(
        "HINDSIGHT_API_KEY is missing. "
        "Check your .env file."
    )


# Create Hindsight client
client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)


# CSV location
CSV_PATH = os.path.join(
    "..",
    "data",
    "nanami_50_Customer_Feedback.csv"
)


def migrate_feedback():

    print("Starting Nanami feedback migration...")
    print(f"Reading CSV: {CSV_PATH}")
    print()

    # Check CSV exists
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"CSV file not found: {CSV_PATH}"
        )

    # Read CSV
    with open(
        CSV_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)
        rows = list(reader)

    print(f"Found {len(rows)} feedback records.")
    print()

    if not rows:
        print("No records found.")
        return

    successful = 0
    failed = 0

    # Store every feedback record
    for index, row in enumerate(rows, start=1):

        try:

            parts = []

            for key, value in row.items():

                if value is not None and str(value).strip():

                    parts.append(
                        f"{key}: {str(value).strip()}"
                    )

            content = (
                "Nanami AI customer feedback record. "
                + ". ".join(parts)
            )

            # Store in Hindsight Cloud
            client.retain(
                bank_id=BANK_ID,
                content=content,
                context="Nanami customer feedback",
                metadata={
                    "source": "nanami_customer_feedback_csv",
                    "record_number": str(index)
                }
            )

            successful += 1

            print(
                f"[{index}/{len(rows)}] "
                f"Stored successfully"
            )

        except Exception as e:

            failed += 1

            print(
                f"[{index}/{len(rows)}] "
                f"FAILED: {e}"
            )

    # Migration summary
    print()
    print("--------------------------------")
    print("Migration completed")
    print("--------------------------------")
    print(f"Total records : {len(rows)}")
    print(f"Successful    : {successful}")
    print(f"Failed        : {failed}")
    print("--------------------------------")


if __name__ == "__main__":

    try:
        migrate_feedback()

    finally:
        client.close()