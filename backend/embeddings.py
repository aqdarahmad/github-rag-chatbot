"""Build the vector database.

Run from the project root:
    python -m backend.embeddings

Reads the documents in data/, splits them into chunks, creates the embeddings
and stores everything in chroma_db/ (the old collection is replaced).
"""

from pathlib import Path

import chromadb
from chromadb.config import Settings

from .chunker import load_documents
from .embedder import embed


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "github_code"

BATCH_SIZE = 64


# ==========================================
# Store documents
# ==========================================

def build_database():

    print("\nLoading documents...")

    documents = load_documents()

    print(f"Loaded {len(documents)} chunks.")

    if not documents:

        raise RuntimeError(
            "No documents were found in data/. "
            "Run: python -m backend.github_documents"
        )

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH),
        settings=Settings(anonymized_telemetry=False)
    )

    # Start from an empty collection so no old chunks stay behind
    try:

        client.delete_collection(name=COLLECTION_NAME)

    except Exception:

        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "hnsw:space": "cosine"
        }
    )

    print("\nCreating embeddings and storing them in ChromaDB...")

    for start in range(0, len(documents), BATCH_SIZE):

        batch = documents[start:start + BATCH_SIZE]

        texts = [
            document["text"]
            for document in batch
        ]

        collection.add(

            ids=[
                f"chunk_{start + i}"
                for i in range(len(batch))
            ],

            documents=texts,

            embeddings=embed(texts),

            metadatas=[
                {
                    "source": document["source"],
                    "chunk_id": document["chunk_id"]
                }
                for document in batch
            ]
        )

        print(
            f"  {min(start + BATCH_SIZE, len(documents))}"
            f" / {len(documents)}"
        )

    print(f"\nStored {len(documents)} chunks.")


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    build_database()
