import os
from dotenv import load_dotenv
from hindsight_client import Hindsight


# Load variables from .env
load_dotenv()


# -----------------------------
# Hindsight Cloud Configuration
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
# Check API Key
# -----------------------------

if not API_KEY:
    raise RuntimeError(
        "HINDSIGHT_API_KEY is missing. "
        "Please check your .env file."
    )


# -----------------------------
# Create Hindsight Client
# -----------------------------

client = Hindsight(
    base_url=BASE_URL,
    api_key=API_KEY
)


# -----------------------------
# Create Memory Bank
# -----------------------------

def setup_bank():

    try:

        bank = client.create_bank(
            bank_id=BANK_ID,
            name="Nanami AI"
        )

        print(f"Memory bank created: {bank.bank_id}")

    except Exception as e:

        print("Memory bank may already exist.")
        print(f"Details: {e}")


# -----------------------------
# Store Memory
# -----------------------------

def add_memory(content):

    result = client.retain(
        bank_id=BANK_ID,
        content=content
    )

    return result


# -----------------------------
# Search Memory
# -----------------------------

def search_memory(query):

    result = client.recall(
        bank_id=BANK_ID,
        query=query
    )

    memories = []

    for memory in result.results:

        memories.append(memory.text)

    return memories


# -----------------------------
# Test Connection
# -----------------------------

if __name__ == "__main__":

    print("Connecting to Hindsight Cloud...")

    setup_bank()

    print("Storing test memory...")

    add_memory(
        "Nanami AI received customer feedback "
        "that the Galaxy S25 battery drains quickly "
        "after a software update."
    )

    print("Searching Hindsight memory...")

    memories = search_memory(
        "Galaxy S25 battery problem"
    )

    print("\nRelevant memories:")

    if memories:

        for memory in memories:
            print("-", memory)

    else:

        print("No memories found.")

    print("\nHindsight Cloud connection test completed.")