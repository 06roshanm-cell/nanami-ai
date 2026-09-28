import os

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Try to import Hindsight Cloud
try:
    from .hindsight_cloud import search_memory
except ImportError:
    from hindsight_cloud import search_memory


# --------------------------------------------------
# ChromaDB fallback
# --------------------------------------------------

def search_chroma(query, n=5):

    print("Using ChromaDB fallback...")

    try:

        import chromadb
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        client = chromadb.PersistentClient(
            path="vector_db"
        )

        collection = client.get_or_create_collection(
            "customer_feedback"
        )

        embedding = model.encode(
            query
        ).tolist()

        results = collection.query(
            query_embeddings=[embedding],
            n_results=n
        )

        documents = results.get(
            "documents",
            [[]]
        )

        if documents and documents[0]:
            return documents[0]

        return []

    except Exception as e:

        print(
            f"ChromaDB fallback failed: {e}"
        )

        return []


# --------------------------------------------------
# Main feedback search
# --------------------------------------------------

def search_feedback(query, n=5):

    print(
        f"Searching Hindsight Cloud for: {query}"
    )

    try:

        # Hindsight Cloud is now the PRIMARY
        # retrieval system.
        memories = search_memory(query)

        if memories:

            print(
                f"Hindsight returned "
                f"{len(memories)} memories."
            )

            return memories[:n]

        print(
            "Hindsight returned no memories."
        )

        # If Hindsight has no result,
        # use ChromaDB as backup.
        return search_chroma(
            query,
            n
        )

    except Exception as e:

        print(
            f"Hindsight search failed: {e}"
        )

        # Hindsight failed completely,
        # so use ChromaDB backup.
        return search_chroma(
            query,
            n
        )