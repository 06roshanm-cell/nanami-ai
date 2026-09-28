import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


# Load environment variables
load_dotenv()


# -----------------------------
# Hindsight configuration
# -----------------------------

API_KEY = os.getenv("HINDSIGHT_API_KEY")

BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "nanami-ai"
)


# -----------------------------
# Check API key
# -----------------------------

if not API_KEY:
    raise RuntimeError(
        "HINDSIGHT_API_KEY is missing. "
        "Check your .env file."
    )


# -----------------------------
# Create Hindsight client
# -----------------------------

client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)


# -----------------------------
# Test recall
# -----------------------------

def test_recall(query):

    print()
    print("--------------------------------")
    print(f"Searching: {query}")
    print("--------------------------------")

    try:

        result = client.recall(
            bank_id=BANK_ID,
            query=query
        )

        if not result.results:

            print("No memories found.")
            return

        print(
            f"Found {len(result.results)} relevant memories."
        )

        print()

        for index, memory in enumerate(
            result.results,
            start=1
        ):

            print(f"Memory {index}:")
            print(memory.text)
            print()

    except Exception as e:

        print("Recall failed:")
        print(e)


# -----------------------------
# Run verification
# -----------------------------

if __name__ == "__main__":

    print("================================")
    print("Nanami AI - Hindsight Verification")
    print("================================")

    # Test 1
    test_recall(
        "Galaxy S25 battery drains quickly"
    )

    # Test 2
    test_recall(
        "camera blurry after software update"
    )

    # Test 3
    test_recall(
        "WiFi disconnects frequently"
    )

    print("--------------------------------")
    print("Hindsight verification completed")
    print("--------------------------------")

    client.close()