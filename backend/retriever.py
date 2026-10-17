import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings

from .embedder import embed


logger = logging.getLogger("rag-chatbot")


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "github_code"


# ==========================================
# ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH),
    settings=Settings(anonymized_telemetry=False)
)

try:

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

except Exception as error:

    raise RuntimeError(
        f"ChromaDB collection '{COLLECTION_NAME}' was not "
        f"found in {CHROMA_PATH}. Build it first with: "
        f"python -m backend.embeddings"
    ) from error


# Load the embedding model now (not on the first question),
# so a problem shows up at startup and the first answer is fast.
embed(["warm up"])

logger.info(
    "Retriever ready: %d chunks in ChromaDB.",
    collection.count()
)


# ==========================================
# Semantic retrieval
# ==========================================

def retrieve(query, top_k=8):
    """Return the top_k chunks closest to the question (best first)."""

    query_embedding = embed([query])[0]

    results = collection.query(

        query_embeddings=[query_embedding],

        n_results=top_k,

        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    chunks = [

        {
            "document": document,
            "metadata": metadata,
            "distance": float(distance)
        }

        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        )
    ]

    for i, chunk in enumerate(chunks):

        logger.debug(
            "Result %d | %s | chunk %s | distance %.4f",
            i + 1,
            chunk["metadata"]["source"],
            chunk["metadata"]["chunk_id"],
            chunk["distance"]
        )

    return chunks


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nAsk a question about FastAPI: "
    )

    for i, chunk in enumerate(retrieve(question)):

        print(f"\nResult {i + 1}")

        print(
            f"Source: {chunk['metadata']['source']}"
        )

        print(
            f"Distance: {chunk['distance']:.4f}"
        )

        print()

        print(chunk["document"])

        print("\n" + "=" * 60)
