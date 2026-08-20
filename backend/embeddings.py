import chromadb
from sentence_transformers import SentenceTransformer

from .chunker import load_documents


# ==========================================
# Embedding model
# ==========================================

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


# ==========================================
# ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path="../chroma_db"
)


collection = client.get_or_create_collection(
    name="github_code"
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
        show_progress_bar=True
    )

    return embeddings


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    print("Loading chunks...")

    documents = load_documents()

    print(
        f"Loaded {len(documents)} chunks."
    )


    print(
        "Creating embeddings..."
    )

    embeddings = create_embeddings(
        documents
    )


    print(
        f"Embedding shape: {embeddings.shape}"
    )


    print(
        "Storing embeddings in ChromaDB..."
    )


    # IDs for each chunk
    ids = [
        f"chunk_{i}"
        for i in range(len(documents))
    ]


    # Text of each chunk
    texts = [
        document["text"]
        for document in documents
    ]


    # Metadata
    metadatas = [
        {
            "source": document["source"],
            "chunk_id": document["chunk_id"]
        }
        for document in documents
    ]


    # Store everything
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


    print(
        f"Stored {len(documents)} chunks in ChromaDB."
    )