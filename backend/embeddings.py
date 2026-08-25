import chromadb

from pathlib import Path

from sentence_transformers import SentenceTransformer

from .chunker import load_documents


# ==========================================
# Paths
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PATH = BASE_DIR / "chroma_db"


# ==========================================
# Embedding model
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(
    MODEL_NAME
)


# ==========================================
# ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)


collection = client.get_or_create_collection(
    name="github_code",
    metadata={
        "hnsw:space": "cosine"
    }
)


# ==========================================
# Create embeddings
# ==========================================

def create_embeddings(documents):

    texts = [
        document["text"]
        for document in documents
    ]

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    return embeddings


# ==========================================
# Store documents
# ==========================================

def build_database():

    print(
        "\nLoading documents..."
    )

    documents = load_documents()

    print(
        f"Loaded {len(documents)} chunks."
    )

    if not documents:

        raise RuntimeError(
            "No documents were found."
        )

    print(
        "\nCreating embeddings..."
    )

    embeddings = create_embeddings(
        documents
    )

    print(
        f"Embedding shape: "
        f"{embeddings.shape}"
    )

    ids = [
        f"chunk_{i}"
        for i in range(
            len(documents)
        )
    ]

    texts = [
        document["text"]
        for document in documents
    ]

    metadatas = [

        {
            "source": document["source"],
            "chunk_id": document["chunk_id"]
        }

        for document in documents
    ]

    print(
        "\nStoring documents in ChromaDB..."
    )

    collection.upsert(

        ids=ids,

        documents=texts,

        embeddings=embeddings.tolist(),

        metadatas=metadatas
    )

    print(
        f"\nStored "
        f"{len(documents)} chunks."
    )


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    build_database()